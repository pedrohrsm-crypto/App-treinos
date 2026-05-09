"""
Email Service — Confirmação de Registro e Notificações
========================================================

Wrapper SMTP para enviar emails de confirmação após registro
e notificações diversas com fallback gracioso.
"""

import smtplib
import os
import threading
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


class EmailService:
    """Serviço de email com suporte a SMTP e fallback offline."""

    SMTP_HOST = os.getenv("SMTP_HOST", "")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USER = os.getenv("SMTP_USER", "")
    SMTP_PASS = os.getenv("SMTP_PASS", "")

    @staticmethod
    def _is_configured() -> bool:
        """Verifica se SMTP está configurado."""
        return all([
            EmailService.SMTP_HOST,
            EmailService.SMTP_USER,
            EmailService.SMTP_PASS,
        ])

    @staticmethod
    def send_confirmation_email(
        name: str,
        cpf: str,
        cref: str,
        email: str,
        registration_date: str = None,
    ) -> tuple[bool, str]:
        """
        Envia email de confirmação com dados de registro.

        Args:
            name: Nome do treinador
            cpf: CPF do treinador
            cref: CREF do treinador
            email: Email destinatário
            registration_date: Data de registro (ISO format)

        Returns:
            (success: bool, message: str)
        """
        if not EmailService._is_configured():
            return (False, "SMTP não configurado (envio offline)")

        if not registration_date:
            registration_date = datetime.now().isoformat()

        subject = "Confirmação de Registro — Velix"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f5f5f5; padding: 20px;">
                <div style="max-width: 600px; margin: 0 auto; background-color: white; border-radius: 8px; padding: 30px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <h1 style="color: #2e7a62; text-align: center; margin-bottom: 20px;">Velix</h1>
                    <p style="color: #333; font-size: 14px;">Olá <strong>{name}</strong>,</p>
                    <p style="color: #333; font-size: 14px;">Sua conta foi criada com sucesso! Aqui estão seus dados de registro:</p>

                    <div style="background-color: #f9f9f9; border-left: 4px solid #2e7a62; padding: 15px; margin: 20px 0; border-radius: 4px;">
                        <p style="margin: 8px 0; color: #333; font-size: 13px;"><strong>Nome:</strong> {name}</p>
                        <p style="margin: 8px 0; color: #333; font-size: 13px;"><strong>CPF:</strong> {cpf}</p>
                        <p style="margin: 8px 0; color: #333; font-size: 13px;"><strong>CREF:</strong> {cref}</p>
                        <p style="margin: 8px 0; color: #333; font-size: 13px;"><strong>Email:</strong> {email}</p>
                        <p style="margin: 8px 0; color: #999; font-size: 12px;"><strong>Data de Registro:</strong> {registration_date}</p>
                    </div>

                    <p style="color: #333; font-size: 14px;">Você pode agora fazer login no Velix usando sua CPF ou CREF com a senha cadastrada.</p>
                    <p style="color: #999; font-size: 12px; margin-top: 30px; border-top: 1px solid #ddd; padding-top: 15px;">
                        Este é um email automático. Não responda este mensagem. Se tiver dúvidas, acesse nosso menu de Ajuda dentro do aplicativo.
                    </p>
                </div>
            </body>
        </html>
        """

        text_body = f"""
Velix — Confirmação de Registro

Olá {name},

Sua conta foi criada com sucesso! Aqui estão seus dados de registro:

Nome: {name}
CPF: {cpf}
CREF: {cref}
Email: {email}
Data de Registro: {registration_date}

Você pode agora fazer login no Velix usando sua CPF ou CREF com a senha cadastrada.

---
Este é um email automático. Não responda este mensagem.
        """

        try:
            msg = MIMEMultipart("alternative")
            msg["Subject"] = subject
            msg["From"] = EmailService.SMTP_USER
            msg["To"] = email

            msg.attach(MIMEText(text_body, "plain", "utf-8"))
            msg.attach(MIMEText(html_body, "html", "utf-8"))

            with smtplib.SMTP(EmailService.SMTP_HOST, EmailService.SMTP_PORT) as server:
                server.starttls()
                server.login(EmailService.SMTP_USER, EmailService.SMTP_PASS)
                server.sendmail(EmailService.SMTP_USER, email, msg.as_string())

            return (True, "Email enviado com sucesso")
        except smtplib.SMTPException as e:
            return (False, f"Erro SMTP: {str(e)[:100]}")
        except Exception as e:
            return (False, f"Erro ao enviar email: {str(e)[:100]}")

    @staticmethod
    def send_confirmation_email_async(
        name: str,
        cpf: str,
        cref: str,
        email: str,
        callback=None,
    ):
        """
        Envia email de confirmação em thread separada (não bloqueia UI).

        Args:
            name: Nome do treinador
            cpf: CPF do treinador
            cref: CREF do treinador
            email: Email destinatário
            callback: Função(success: bool, message: str) chamada ao terminar
        """
        def _send():
            success, message = EmailService.send_confirmation_email(name, cpf, cref, email)
            if callback:
                callback(success, message)

        thread = threading.Thread(target=_send, daemon=True)
        thread.start()
