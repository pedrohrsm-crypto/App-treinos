"""
Encryption Manager — Gestão de encriptação de dados sensíveis
==============================================================

Fornece encriptação Fernet para credenciais do utilizador,
usando chave derivada do hash da password.
"""

import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64
from typing import Optional


class EncryptionManager:
    """Gestor de encriptação com suporte a Fernet."""

    @staticmethod
    def derive_master_key(password_hash: str) -> bytes:
        """
        Deriva uma chave de encriptação a partir do hash da password.

        Args:
            password_hash: Hash PBKDF2 da password (formato: pbkdf2$salt$hash)

        Returns:
            Chave de 32 bytes para uso com Fernet
        """
        # Usar apenas a hash (sem o salt) para derivar a chave
        hash_part = password_hash.split("$")[-1] if "$" in password_hash else password_hash

        # Derivar chave usando SHA256
        h = hashes.Hash(hashes.SHA256(), backend=default_backend())
        h.update(hash_part.encode())
        key_bytes = h.finalize()

        # Converter para base64 para uso com Fernet (requer chave base64-encoded)
        key = base64.urlsafe_b64encode(key_bytes)
        return key

    @staticmethod
    def encrypt_field(value: str, master_key: bytes) -> str:
        """
        Encripta um campo de texto.

        Args:
            value: Valor a encriptar
            master_key: Chave de encriptação (resultado de derive_master_key)

        Returns:
            String encriptada em formato base64
        """
        if not value:
            return ""

        try:
            cipher_suite = Fernet(master_key)
            encrypted_bytes = cipher_suite.encrypt(value.encode())
            # Retornar em base64 para armazenagem em BD
            return base64.b64encode(encrypted_bytes).decode()
        except Exception as e:
            raise ValueError(f"Erro ao encriptar: {str(e)}")

    @staticmethod
    def decrypt_field(encrypted_value: str, master_key: bytes) -> str:
        """
        Desencripta um campo de texto.

        Args:
            encrypted_value: Valor encriptado (em base64)
            master_key: Chave de encriptação (resultado de derive_master_key)

        Returns:
            String desencriptada
        """
        if not encrypted_value:
            return ""

        try:
            cipher_suite = Fernet(master_key)
            encrypted_bytes = base64.b64decode(encrypted_value)
            decrypted_bytes = cipher_suite.decrypt(encrypted_bytes)
            return decrypted_bytes.decode()
        except Exception as e:
            raise ValueError(f"Erro ao desencriptar: {str(e)}")

    @staticmethod
    def encrypt_dict(data: dict, master_key: bytes, fields_to_encrypt: list) -> dict:
        """
        Encripta campos específicos de um dicionário.

        Args:
            data: Dicionário com dados
            master_key: Chave de encriptação
            fields_to_encrypt: Lista de nomes de campos a encriptar

        Returns:
            Dicionário com campos indicados encriptados
        """
        result = data.copy()
        for field in fields_to_encrypt:
            if field in result and result[field]:
                result[field] = EncryptionManager.encrypt_field(
                    str(result[field]), master_key
                )
        return result

    @staticmethod
    def decrypt_dict(data: dict, master_key: bytes, fields_to_decrypt: list) -> dict:
        """
        Desencripta campos específicos de um dicionário.

        Args:
            data: Dicionário com dados encriptados
            master_key: Chave de encriptação
            fields_to_decrypt: Lista de nomes de campos a desencriptar

        Returns:
            Dicionário com campos indicados desencriptados
        """
        result = data.copy()
        for field in fields_to_decrypt:
            if field in result and result[field]:
                result[field] = EncryptionManager.decrypt_field(
                    result[field], master_key
                )
        return result
