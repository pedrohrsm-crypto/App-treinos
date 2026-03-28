#!/usr/bin/env python3
"""
Gerador de ícone — App Treinos
================================

Cria ícone profissional .ico (Windows) e .png (multiplataforma)
para empacotamento do executável.

Uso: python scripts/generate_icon.py
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

ROOT = Path(__file__).parent.parent
ASSETS_DIR = ROOT / "assets"
ASSETS_DIR.mkdir(exist_ok=True)

# Tamanhos para ICO (todas as resoluções padrão Windows)
ICO_SIZES = [16, 24, 32, 48, 64, 128, 256]


def draw_icon(size: int) -> Image.Image:
    """Desenha o ícone do App Treinos num dado tamanho."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Cores do tema App Treinos
    bg_gradient_top = (13, 71, 161)       # Azul escuro
    bg_gradient_bottom = (25, 118, 210)   # Azul médio
    accent = (255, 167, 38)               # Laranja (destaque)
    white = (255, 255, 255)

    pad = max(1, size // 32)
    corner = max(2, size // 8)

    # Fundo: retângulo arredondado com gradiente vertical
    for y in range(size):
        t = y / max(1, size - 1)
        r = int(bg_gradient_top[0] * (1 - t) + bg_gradient_bottom[0] * t)
        g = int(bg_gradient_top[1] * (1 - t) + bg_gradient_bottom[1] * t)
        b = int(bg_gradient_top[2] * (1 - t) + bg_gradient_bottom[2] * t)
        draw.line([(pad, y), (size - pad - 1, y)], fill=(r, g, b))

    # Máscara para cantos arredondados
    mask = Image.new("L", (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(
        [pad, pad, size - pad - 1, size - pad - 1],
        radius=corner,
        fill=255,
    )
    img.putalpha(mask)

    # Redesenhar o gradiente dentro da máscara
    img2 = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw2 = ImageDraw.Draw(img2)

    for y in range(size):
        t = y / max(1, size - 1)
        r = int(bg_gradient_top[0] * (1 - t) + bg_gradient_bottom[0] * t)
        g = int(bg_gradient_top[1] * (1 - t) + bg_gradient_bottom[1] * t)
        b = int(bg_gradient_top[2] * (1 - t) + bg_gradient_bottom[2] * t)
        draw2.line([(0, y), (size - 1, y)], fill=(r, g, b, 255))

    img2.putalpha(mask)
    draw = ImageDraw.Draw(img2)

    # Ícone central: figura de corredor estilizado
    cx, cy = size // 2, size // 2

    if size >= 48:
        # Figura humana em corrida (estilizada)
        head_r = max(2, size // 10)
        head_cx = cx - size // 12
        head_cy = cy - size // 4

        # Cabeça
        draw.ellipse(
            [head_cx - head_r, head_cy - head_r,
             head_cx + head_r, head_cy + head_r],
            fill=white,
        )

        lw = max(2, size // 20)  # espessura de linha

        # Tronco (inclinado para frente)
        trunk_top = (head_cx + size // 20, head_cy + head_r)
        trunk_bot = (cx + size // 16, cy + size // 8)
        draw.line([trunk_top, trunk_bot], fill=white, width=lw)

        # Braço traseiro (atrás)
        arm1_end = (trunk_top[0] + size // 5, trunk_top[1] + size // 7)
        draw.line([trunk_top, arm1_end], fill=white, width=lw)

        # Braço dianteiro (à frente)
        arm2_end = (trunk_top[0] - size // 6, trunk_top[1] + size // 10)
        draw.line([trunk_top, arm2_end], fill=white, width=lw)

        # Perna traseira (esticada para trás)
        knee1 = (trunk_bot[0] - size // 8, trunk_bot[1] + size // 7)
        foot1 = (knee1[0] - size // 7, knee1[1] + size // 8)
        draw.line([trunk_bot, knee1], fill=white, width=lw)
        draw.line([knee1, foot1], fill=white, width=lw)

        # Perna dianteira (à frente, dobrada)
        knee2 = (trunk_bot[0] + size // 6, trunk_bot[1] + size // 8)
        foot2 = (knee2[0] + size // 16, knee2[1] + size // 7)
        draw.line([trunk_bot, knee2], fill=white, width=lw)
        draw.line([knee2, foot2], fill=white, width=lw)

        # Detalhes laranja: linhas de movimento
        for i in range(3):
            y_off = cy - size // 6 + i * (size // 8)
            x_start = cx + size // 4 + i * (size // 20)
            dash_len = max(3, size // 10 - i * 2)
            draw.line(
                [(x_start, y_off), (x_start + dash_len, y_off)],
                fill=accent,
                width=max(1, lw - 1),
            )

    elif size >= 24:
        # Versão simplificada: silhueta + traços
        head_r = max(2, size // 8)
        draw.ellipse(
            [cx - head_r - 2, cy - size // 3 - head_r,
             cx - 2 + head_r, cy - size // 3 + head_r],
            fill=white,
        )
        lw = max(1, size // 12)
        # Corpo simplificado em V (corrida)
        draw.line([(cx - 2, cy - size // 3 + head_r), (cx, cy + size // 6)],
                  fill=white, width=lw)
        draw.line([(cx, cy + size // 6), (cx - size // 5, cy + size // 3)],
                  fill=white, width=lw)
        draw.line([(cx, cy + size // 6), (cx + size // 5, cy + size // 3)],
                  fill=white, width=lw)
        # Traço laranja
        draw.line([(cx + size // 4, cy - 2), (cx + size // 3, cy - 2)],
                  fill=accent, width=max(1, lw - 1))

    else:
        # Tamanho mínimo (16px): apenas um ponto + traço
        r = max(2, size // 5)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=white)
        draw.line([(cx + r + 1, cy), (size - pad - 2, cy)],
                  fill=accent, width=max(1, size // 10))

    return img2


def main():
    print("🎨 Gerando ícone do App Treinos...\n")

    # Gerar PNG 512x512 (alta resolução para stores e docs)
    icon_512 = draw_icon(512)
    png_path = ASSETS_DIR / "icon.png"
    icon_512.save(str(png_path), "PNG")
    print(f"  ✅ {png_path.relative_to(ROOT)}  (512×512)")

    # Gerar PNG 192x192 (Flet web manifest)
    icon_192 = draw_icon(192)
    png_192 = ASSETS_DIR / "icon-192.png"
    icon_192.save(str(png_192), "PNG")
    print(f"  ✅ {png_192.relative_to(ROOT)}  (192×192)")

    # Gerar ICO com todas as resoluções
    ico_images = [draw_icon(s) for s in ICO_SIZES]
    ico_path = ASSETS_DIR / "icon.ico"
    ico_images[0].save(
        str(ico_path),
        format="ICO",
        sizes=[(s, s) for s in ICO_SIZES],
        append_images=ico_images[1:],
    )
    print(f"  ✅ {ico_path.relative_to(ROOT)}  ({', '.join(str(s) for s in ICO_SIZES)})")

    print(f"\n  📂 Ícones salvos em: {ASSETS_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
