"""
Widgets Modernos com Animações e Efeitos Visuais
================================================

Componentes customizados com:
- Bordas arredondadas
- Animações suaves
- Efeitos hover
- Transições fluidas
"""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional
import math


class AnimatedButton(tk.Canvas):
    """Botão com animações de hover e clique."""
    
    def __init__(self, parent, text: str, command: Optional[Callable] = None,
                 bg_color: str = "#2563eb", hover_color: str = "#1d4ed8",
                 text_color: str = "#ffffff", width: int = 200, height: int = 50,
                 corner_radius: int = 12, **kwargs):
        super().__init__(parent, width=width, height=height, 
                        highlightthickness=0, bg=parent['bg'], **kwargs)
        
        self.text = text
        self.command = command
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.corner_radius = corner_radius
        self.width = width
        self.height = height
        
        # Estado de animação
        self.is_hovering = False
        self.is_pressing = False
        self.current_color = bg_color
        self.animation_id = None
        self._scale_factor = 1.0
        
        # Criar elementos
        self._draw_button()
        
        # Bindings
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
        
        # Tornar focável para acessibilidade
        self.bind('<Return>', lambda e: self._on_release(e))
        self.bind('<space>', lambda e: self._on_release(e))
    
    def _draw_button(self):
        """Desenha o botão com bordas arredondadas."""
        self.delete('all')
        
        # Calcular dimensões com escala
        w = self.width * self._scale_factor
        h = self.height * self._scale_factor
        r = self.corner_radius
        
        # Centralizar
        offset_x = (self.width - w) / 2
        offset_y = (self.height - h) / 2
        
        # Desenhar retângulo com cantos arredondados
        x0, y0 = offset_x, offset_y
        x1, y1 = offset_x + w, offset_y + h
        
        self.create_rounded_rect(x0, y0, x1, y1, r, fill=self.current_color, outline='')
        
        # Texto centralizado
        self.create_text(
            self.width / 2, self.height / 2,
            text=self.text,
            fill=self.text_color,
            font=('Segoe UI', 11, 'bold'),
            tags='text'
        )
    
    def create_rounded_rect(self, x0, y0, x1, y1, r, **kwargs):
        """Cria retângulo com bordas arredondadas."""
        points = [
            x0 + r, y0,
            x1 - r, y0,
            x1, y0,
            x1, y0 + r,
            x1, y1 - r,
            x1, y1,
            x1 - r, y1,
            x0 + r, y1,
            x0, y1,
            x0, y1 - r,
            x0, y0 + r,
            x0, y0
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
    
    def _interpolate_color(self, color1: str, color2: str, factor: float) -> str:
        """Interpola entre duas cores."""
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def _animate_color(self, target_color: str, steps: int = 10, duration: int = 150):
        """Anima transição de cor."""
        if self.animation_id:
            self.after_cancel(self.animation_id)
        
        start_color = self.current_color
        step_delay = duration // steps
        
        def step(current_step):
            if current_step <= steps:
                factor = current_step / steps
                # Easing suave (ease-out)
                factor = 1 - (1 - factor) ** 3
                
                self.current_color = self._interpolate_color(start_color, target_color, factor)
                self._draw_button()
                
                self.animation_id = self.after(step_delay, lambda: step(current_step + 1))
            else:
                self.current_color = target_color
                self._draw_button()
        
        step(0)
    
    def _animate_scale(self, target_scale: float, steps: int = 8, duration: int = 120):
        """Anima mudança de escala."""
        start_scale = self._scale_factor
        step_delay = duration // steps
        
        def step(current_step):
            if current_step <= steps:
                factor = current_step / steps
                # Easing bounce
                factor = 1 - (1 - factor) ** 2
                
                self._scale_factor = start_scale + (target_scale - start_scale) * factor
                self._draw_button()
                
                self.after(step_delay, lambda: step(current_step + 1))
            else:
                self._scale_factor = target_scale
                self._draw_button()
        
        step(0)
    
    def _on_enter(self, event):
        """Quando o mouse entra no botão."""
        if not self.is_hovering:
            self.is_hovering = True
            self._animate_color(self.hover_color, steps=8, duration=120)
            self._animate_scale(1.03, steps=6, duration=100)
            self.config(cursor='hand2')
    
    def _on_leave(self, event):
        """Quando o mouse sai do botão."""
        if self.is_hovering:
            self.is_hovering = False
            self.is_pressing = False
            self._animate_color(self.bg_color, steps=8, duration=120)
            self._animate_scale(1.0, steps=6, duration=100)
            self.config(cursor='')
    
    def _on_press(self, event):
        """Quando o botão é pressionado."""
        self.is_pressing = True
        self._animate_scale(0.95, steps=4, duration=60)
    
    def _on_release(self, event):
        """Quando o botão é liberado."""
        if self.is_pressing and self.command:
            self.command()
        
        if self.is_hovering:
            self._animate_scale(1.03, steps=4, duration=60)
        else:
            self._animate_scale(1.0, steps=4, duration=60)
        
        self.is_pressing = False


class RoundedFrame(tk.Canvas):
    """Frame com bordas arredondadas e sombra."""
    
    def __init__(self, parent, bg_color: str = "#ffffff", 
                 corner_radius: int = 16, shadow: bool = True,
                 shadow_color: str = "#00000015", **kwargs):
        super().__init__(parent, highlightthickness=0, bg=parent['bg'], **kwargs)
        
        self.bg_color = bg_color
        self.corner_radius = corner_radius
        self.shadow = shadow
        self.shadow_color = shadow_color
        
        self.bind('<Configure>', self._on_resize)
    
    def _on_resize(self, event=None):
        """Redesenha quando o tamanho muda."""
        self.delete('all')
        w = self.winfo_width()
        h = self.winfo_height()
        r = self.corner_radius
        
        if self.shadow:
            # Sombra
            offset = 4
            self._create_rounded_rect(
                offset, offset, w, h, r,
                fill=self.shadow_color, outline=''
            )
        
        # Frame principal
        self._create_rounded_rect(
            0, 0, w - (4 if self.shadow else 0), h - (4 if self.shadow else 0),
            r, fill=self.bg_color, outline=''
        )
    
    def _create_rounded_rect(self, x0, y0, x1, y1, r, **kwargs):
        """Cria retângulo com bordas arredondadas."""
        points = [
            x0 + r, y0,
            x1 - r, y0,
            x1, y0,
            x1, y0 + r,
            x1, y1 - r,
            x1, y1,
            x1 - r, y1,
            x0 + r, y1,
            x0, y1,
            x0, y1 - r,
            x0, y0 + r,
            x0, y0
        ]
        return self.create_polygon(points, smooth=True, **kwargs)


class AnimatedCard(tk.Frame):
    """Card com animação de hover e clique."""
    
    def __init__(self, parent, title: str, subtitle: str = "",
                 icon: str = "", bg_color: str = "#ffffff",
                 command: Optional[Callable] = None, **kwargs):
        super().__init__(parent, bg=parent['bg'], **kwargs)
        
        self.title_text = title
        self.subtitle_text = subtitle
        self.icon_text = icon
        self.bg_color = bg_color
        self.command = command
        
        # Estado
        self.is_hovering = False
        self.elevation = 2
        
        # Canvas para desenho
        self.canvas = RoundedFrame(
            self, bg_color=bg_color, corner_radius=16,
            shadow=True
        )
        self.canvas.pack(fill='both', expand=True)
        
        # Container interno
        self.content = tk.Frame(self.canvas, bg=bg_color)
        self.canvas.create_window(0, 0, window=self.content, anchor='nw')
        
        # Criar conteúdo
        self._create_content()
        
        # Bindings
        self._bind_events(self)
        self._bind_events(self.canvas)
        self._bind_events(self.content)
        
        # Atualizar após criação
        self.after(100, self._update_scroll_region)
    
    def _create_content(self):
        """Cria o conteúdo do card."""
        # Ícone
        if self.icon_text:
            icon = tk.Label(
                self.content,
                text=self.icon_text,
                font=('Segoe UI Emoji', 48),
                bg=self.bg_color,
                fg='#2563eb'
            )
            icon.pack(pady=(30, 15))
            self._bind_events(icon)
        
        # Título
        title = tk.Label(
            self.content,
            text=self.title_text,
            font=('Segoe UI', 18, 'bold'),
            bg=self.bg_color,
            fg='#1f2937'
        )
        title.pack(pady=(0, 5))
        self._bind_events(title)
        
        # Subtítulo
        if self.subtitle_text:
            subtitle = tk.Label(
                self.content,
                text=self.subtitle_text,
                font=('Segoe UI', 11),
                bg=self.bg_color,
                fg='#6b7280',
                wraplength=220
            )
            subtitle.pack(pady=(0, 30), padx=20)
            self._bind_events(subtitle)
    
    def _bind_events(self, widget):
        """Aplica eventos ao widget."""
        widget.bind('<Enter>', self._on_enter)
        widget.bind('<Leave>', self._on_leave)
        if self.command:
            widget.bind('<Button-1>', self._on_click)
            widget.config(cursor='hand2')
    
    def _update_scroll_region(self):
        """Atualiza região de scroll do canvas."""
        self.content.update_idletasks()
        self.canvas.config(
            width=self.content.winfo_reqwidth(),
            height=self.content.winfo_reqheight()
        )
    
    def _on_enter(self, event):
        """Animação de hover."""
        if not self.is_hovering:
            self.is_hovering = True
            self._animate_lift()
    
    def _on_leave(self, event):
        """Animação de saída."""
        if self.is_hovering:
            self.is_hovering = False
            self._animate_lower()
    
    def _on_click(self, event):
        """Executa comando ao clicar."""
        if self.command:
            # Animação de clique
            self.after(50, lambda: self.config(bg=self['bg']))
            self.command()
    
    def _animate_lift(self):
        """Anima elevação do card."""
        # Aumentar levemente o tamanho
        self.canvas.config(highlightthickness=0)
        # Atualizar sombra seria feito aqui (simplificado)
    
    def _animate_lower(self):
        """Anima descida do card."""
        self.canvas.config(highlightthickness=0)


class FadeTransition:
    """Gerencia transições suaves entre telas."""
    
    @staticmethod
    def fade_out(widget, callback: Optional[Callable] = None, duration: int = 200):
        """Fade out suave."""
        steps = 10
        step_delay = duration // steps
        
        def step(current_step):
            if current_step < steps:
                alpha = 1 - (current_step / steps)
                # Simular fade com cor de fundo
                widget.update()
                widget.after(step_delay, lambda: step(current_step + 1))
            else:
                if callback:
                    callback()
        
        step(0)
    
    @staticmethod
    def fade_in(widget, duration: int = 200):
        """Fade in suave."""
        widget.update()
        # Implementação simplificada - Tkinter tem limitações nativas para fade


class ModernEntry(tk.Frame):
    """Campo de entrada moderno com label flutuante."""
    
    def __init__(self, parent, label: str = "", show: str = "", **kwargs):
        super().__init__(parent, bg=parent['bg'])
        
        self.label_text = label
        self.show_char = show
        
        # Container com borda arredondada
        self.container = RoundedFrame(
            self, bg_color='#f3f4f6', corner_radius=10, shadow=False
        )
        self.container.pack(fill='both', expand=True)
        
        # Label
        self.label = tk.Label(
            self.container,
            text=label,
            font=('Segoe UI', 9),
            bg='#f3f4f6',
            fg='#6b7280'
        )
        self.label.place(x=15, y=5)
        
        # Entry
        self.entry = tk.Entry(
            self.container,
            font=('Segoe UI', 11),
            bg='#f3f4f6',
            fg='#1f2937',
            relief='flat',
            bd=0,
            show=show,
            insertbackground='#2563eb'
        )
        self.entry.place(x=15, y=25, relwidth=0.9, height=25)
        
        # Bindings para animação
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
    
    def _on_focus_in(self, event):
        """Animação ao focar."""
        self.container.config(highlightthickness=2, highlightbackground='#2563eb')
    
    def _on_focus_out(self, event):
        """Animação ao desfocar."""
        self.container.config(highlightthickness=0)
    
    def get(self):
        """Obtém valor."""
        return self.entry.get()
    
    def delete(self, first, last=None):
        """Deleta conteúdo."""
        self.entry.delete(first, last)
    
    def insert(self, index, string):
        """Insere texto."""
        self.entry.insert(index, string)
