import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_pure_poster_v3():
    W, H = 1200, 1800
    
    # 1. Fundo Washi
    base_color = (239, 236, 228)
    poster = Image.new('RGB', (W, H), base_color)
    noise = np.random.normal(0, 3.0, (H, W, 3))
    poster = Image.fromarray(np.clip(np.array(poster, dtype=float) + noise, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(poster)

    # 2. Sol Carmesim Monumental ATRÁS do Personagem (Hinomaru)
    sun_size = 720
    sun_cx, sun_cy = 470, 520
    sun_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sun_draw = ImageDraw.Draw(sun_img)
    
    # Círculo vermelho imperial
    sun_draw.ellipse(
        [sun_cx - sun_size//2, sun_cy - sun_size//2, sun_cx + sun_size//2, sun_cy + sun_size//2],
        fill=(145, 12, 12, 255)
    )
    # Textura interna sutil de pincel sumi-e
    for _ in range(60):
        rx = np.random.randint(sun_cx - 300, sun_cx + 300)
        ry = np.random.randint(sun_cy - 300, sun_cy + 300)
        if (rx - sun_cx)**2 + (ry - sun_cy)**2 < (sun_size//2 - 20)**2:
            sun_draw.ellipse([rx, ry, rx + 15, ry + 15], fill=(90, 6, 6, 40))
            
    sun_img = sun_img.filter(ImageFilter.GaussianBlur(radius=2.0))
    poster.paste(sun_img, (0, 0), sun_img)

    # 3. Personagem SÓLIDO (Cores Naturais + Óculos Dourados + Tatuagem Nítida)
    char_raw = Image.open('/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg').convert('RGBA')
    
    char_w = 660
    char_h = int(char_w * (char_raw.height / char_raw.width))
    char_resized = char_raw.resize((char_w, char_h), Image.Resampling.LANCZOS)
    
    # Criar máscara oval com borda suave e fade na base
    char_mask = Image.new('L', (char_w, char_h), 0)
    draw_cm = ImageDraw.Draw(char_mask)
    # Elipse cobrindo cabeça, óculos, pescoço e camisa
    draw_cm.ellipse([50, 30, char_w - 30, char_h - 20], fill=255)
    char_mask = char_mask.filter(ImageFilter.GaussianBlur(radius=16))
    
    # Fade out suave na base da camisa
    mask_arr = np.array(char_mask, dtype=float)
    fade_start = int(char_h * 0.72)
    for y in range(fade_start, char_h):
        mask_arr[y, :] *= (char_h - y) / (char_h - fade_start)
    char_mask = Image.fromarray(mask_arr.astype(np.uint8))

    char_x = 140
    char_y = 210
    
    # Colar o personagem sobreposto ao sol vermelho
    poster.paste(char_resized, (char_x, char_y), char_mask)

    # 4. Tipografia Monumental
    draw = ImageDraw.Draw(poster)
    
    try:
        font_serif_huge = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 112)
        font_serif_med = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", 36)
        font_mono = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14)
        font_mono_bold = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", 16)
        font_italic = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf", 18)
    except:
        font_serif_huge = font_serif_med = font_mono = font_mono_bold = font_italic = ImageFont.load_default()

    # Título Monumental THE QUIET STRENGTH
    draw.text((70, 680), "THE", fill=(10, 10, 10), font=font_serif_huge)
    draw.text((70, 785), "QUIET", fill=(10, 10, 10), font=font_serif_huge)
    draw.text((70, 895), "STRENGTH", fill=(10, 10, 10), font=font_serif_huge)
    draw.text((75, 1030), "A STUDY IN RESILIENCE.", fill=(10, 10, 10), font=font_mono_bold)

    # Header Superior
    draw.text((60, 45), "SHADOW  /  VISUAL ARCHIVE", fill=(10, 10, 10), font=font_mono_bold)
    
    poem_lines = [
        "STRENGTH", "IS NOT ALWAYS", "LOUD.", "SOMETIMES",
        "IT LIVES IN", "THE SILENCE", "BETWEEN", "TWO BREATHS."
    ]
    py = 85
    for line in poem_lines:
        color = (145, 12, 12) if line in ["LOUD.", "TWO BREATHS."] else (60, 60, 60)
        draw.text((60, py), line, fill=color, font=font_mono)
        py += 18

    # Kanjis Verticais no Lado Esquerdo: 静けさの中の強さ
    kanji_chars = ["静", "け", "さ", "の", "中", "の", "強", "さ"]
    ky = 320
    for char in kanji_chars:
        draw.text((36, ky), char, fill=(20, 20, 20), font=font_serif_med)
        ky += 42

    # Canto Superior Direito: Series 01 & Virtudes
    draw.text((920, 45), "SERIES 01", fill=(10, 10, 10), font=font_mono_bold)
    draw.text((920, 65), "HUMAN INSTINCTS", fill=(80, 80, 80), font=font_mono)
    draw.rectangle([1140, 45, 1148, 120], fill=(145, 12, 12))
    
    virtues = ["DISCIPLINE", "FOCUS", "PATIENCE", "RESILIENCE", "FREEDOM"]
    vy = 95
    for v in virtues:
        color = (10, 10, 10) if v == "RESILIENCE" else (100, 100, 100)
        draw.text((1000, vy), v, fill=color, font=font_mono)
        vy += 18

    # Encarte Direito: Montanhas & Selo Hanko
    enc_x, enc_y, enc_w, enc_h = 880, 240, 260, 180
    draw.rectangle([enc_x, enc_y, enc_x + enc_w, enc_y + enc_h], fill=(20, 20, 20))
    draw.polygon([(enc_x, enc_y + 120), (enc_x + 80, enc_y + 60), (enc_x + 160, enc_y + 110), (enc_x + 260, enc_y + 80), (enc_x + 260, enc_y + enc_h), (enc_x, enc_y + enc_h)], fill=(40, 40, 40))
    draw.ellipse([enc_x + 180, enc_y + 40, enc_x + 210, enc_y + 70], fill=(145, 12, 12))
    draw.text((enc_x + 10, enc_y + 10), "SERIES 01 // ARCHIVE", fill=(180, 180, 180), font=font_mono)

    # Citação e Selo Hanko
    draw.text((880, 440), '"Not the absence of fear,', fill=(50, 50, 50), font=font_italic)
    draw.text((880, 465), 'but the choice to move', fill=(50, 50, 50), font=font_italic)
    draw.text((880, 490), 'forward anyway."', fill=(50, 50, 50), font=font_italic)
    
    draw.rectangle([1080, 480, 1130, 530], fill=(145, 12, 12), outline=(90, 7, 7), width=2)
    draw.text((1095, 488), "道", fill=(245, 242, 235), font=font_serif_med)

    # Bloco The Journey & Metadados
    draw.text((880, 560), "THE JOURNEY", fill=(10, 10, 10), font=font_mono_bold)
    draw.text((880, 590), "Not a destination, but a", fill=(70, 70, 70), font=font_italic)
    draw.text((880, 612), "continuous becoming —", fill=(70, 70, 70), font=font_italic)
    draw.text((880, 634), "stronger, calmer, truer.", fill=(70, 70, 70), font=font_italic)
    
    draw.line([(880, 670), (1140, 670)], fill=(200, 195, 185), width=1)
    draw.text((880, 685), "LOCATION: KYOTO, JP", fill=(80, 80, 80), font=font_mono)
    draw.text((880, 710), "DATE: APR 12, 2026", fill=(80, 80, 80), font=font_mono)
    draw.rectangle([1130, 685, 1138, 725], fill=(145, 12, 12))

    # Encarte Inferior Esquerdo: Pagode + Swatches
    pag_x, pag_y = 80, 1380
    draw.rectangle([pag_x, pag_y, pag_x + 220, pag_y + 140], fill=(15, 15, 15))
    draw.ellipse([pag_x + 130, pag_y + 30, pag_x + 175, pag_y + 75], fill=(145, 12, 12))
    draw.polygon([(pag_x + 60, pag_y + 130), (pag_x + 110, pag_y + 70), (pag_x + 160, pag_y + 130)], fill=(5, 5, 5))
    draw.text((pag_x + 10, pag_y + 10), "PAGODA // 04", fill=(160, 160, 160), font=font_mono)

    # Swatches carmesim
    swatches = [(196, 30, 30), (160, 20, 20), (145, 12, 12), (90, 10, 10)]
    for i, col in enumerate(swatches):
        draw.rectangle([pag_x + 240 + i*24, pag_y + 20, pag_x + 258 + i*24, pag_y + 55], fill=col)
    draw.text((pag_x + 240, pag_y + 65), "CRIMSON PALETTE", fill=(100, 100, 100), font=font_mono)

    # Poema inferior
    draw.text((pag_x + 240, pag_y + 100), "SOME PEOPLE CARRY STORMS", fill=(70, 70, 70), font=font_mono)
    draw.text((pag_x + 240, pag_y + 120), "AND STILL LOOK LIKE THEY ARE AT PEACE.", fill=(10, 10, 10), font=font_mono_bold)

    # Logotipo Final: SHADOW VISUAL ARCHIVE com Coroa
    # Desenhar coroa geométrica
    draw.polygon([(950, 1450), (970, 1470), (990, 1435), (1010, 1470), (1030, 1450), (1020, 1485), (960, 1485)], fill=(10, 10, 10))
    draw.text((950, 1495), "SHADOW", fill=(10, 10, 10), font=font_serif_med)
    draw.text((950, 1540), "VISUAL ARCHIVE", fill=(100, 100, 100), font=font_mono)

    out_file = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/poster-fidelidade-absoluta.jpg'
    poster.save(out_file, quality=96)
    poster.save('/root/apk-work/PROJETOS/landing-quiet-strength/public/poster-render.jpg', quality=96)
    poster.save('/root/apk-work/PROJETOS/landing-quiet-strength/dist/poster-render.jpg', quality=96)
    print("Versão 3 com paridade total gerada com sucesso!")

if __name__ == '__main__':
    create_pure_poster_v3()
