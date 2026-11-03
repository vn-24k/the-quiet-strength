import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from scipy import ndimage

def create_masterpiece():
    W, H = 1200, 1800
    
    # 1. Fundo Papel Washi Texturizado Clássico
    base_color = (239, 236, 228)
    poster = Image.new('RGB', (W, H), base_color)
    noise = np.random.normal(0, 3.2, (H, W, 3))
    poster = Image.fromarray(np.clip(np.array(poster, dtype=float) + noise, 0, 255).astype(np.uint8))
    draw = ImageDraw.Draw(poster)

    # 2. Sol Carmesim Monumental (Hinomaru / Ensō)
    sun_size = 720
    sun_cx, sun_cy = 460, 520
    sun_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sun_draw = ImageDraw.Draw(sun_img)
    
    sun_draw.ellipse(
        [sun_cx - sun_size//2, sun_cy - sun_size//2, sun_cx + sun_size//2, sun_cy + sun_size//2],
        fill=(145, 12, 12, 255)
    )
    
    # Texturas orgânicas de nanquim dentro do círculo
    np.random.seed(42)
    for _ in range(80):
        rx = np.random.randint(sun_cx - 310, sun_cx + 310)
        ry = np.random.randint(sun_cy - 310, sun_cy + 310)
        if (rx - sun_cx)**2 + (ry - sun_cy)**2 < (sun_size//2 - 25)**2:
            sun_draw.ellipse([rx, ry, rx + np.random.randint(8, 25), ry + np.random.randint(8, 25)], fill=(85, 6, 6, 45))
            
    sun_img = sun_img.filter(ImageFilter.GaussianBlur(radius=2.5))
    poster.paste(sun_img, (0, 0), sun_img)

    # 3. Personagem com Recorte Limpo de Silhueta
    char_raw = Image.open('/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg').convert('RGBA')
    cw_orig, ch_orig = char_raw.size
    
    # Tratar a imagem original para separar a pessoa da parede:
    char_arr = np.array(char_raw, dtype=float)
    r, g, b = char_arr[:,:,0], char_arr[:,:,1], char_arr[:,:,2]
    Y, X = np.ogrid[:ch_orig, :cw_orig]
    
    # Parede branca:
    is_wall_white = (r > 210) & (g > 205) & (b > 195) & (abs(r - b) < 25)
    # Sombra da parede à esquerda:
    is_wall_shadow = (r < 190) & (b >= r - 8) & (X < 280) & (Y < 750)
    # Topo acima da cabeça:
    is_wall_top = Y < 190
    
    wall = is_wall_white | is_wall_shadow | is_wall_top
    
    # Proteção do sujeito (cabeça, rosto, óculos, pescoço e camisa):
    # Nunca remover pixels do rosto do usuário
    prot_head = (Y >= 210) & (Y <= 500) & (X >= 310) & (X <= 820)
    prot_face = (Y > 500) & (Y <= 750) & (X >= 270) & (X <= 810) # Preservar nariz e óculos
    prot_neck = (Y > 750) & (Y <= 960) & (X >= 170) & (X <= 560) # Preservar pescoço com tatuagem
    prot_torso = (Y > 960) & (X >= 0) & (X <= 750) # Preservar camisa
    
    wall = wall & ~(prot_head | prot_face | prot_neck | prot_torso)
    
    # Flood fill
    labeled, num_features = ndimage.label(wall)
    corners = {labeled[0, 0], labeled[0, cw_orig-1], labeled[0, cw_orig//2], labeled[10, 10], labeled[10, cw_orig-10]}
    corners.discard(0)
    bg = np.isin(labeled, list(corners))
    
    person_mask = ~bg
    person_mask = ndimage.binary_fill_holes(person_mask)
    struct = ndimage.generate_binary_structure(2, 2)
    person_mask = ndimage.binary_closing(person_mask, structure=struct, iterations=3)
    
    alpha = np.where(person_mask, 255.0, 0.0)
    
    # Fade out suave na base da camisa (últimos 15%)
    fade_start = int(ch_orig * 0.80)
    for y in range(fade_start, ch_orig):
        alpha[y, :] *= (ch_orig - y) / (ch_orig - fade_start)
        
    alpha_img = Image.fromarray(alpha.astype(np.uint8), mode='L')
    alpha_smooth = alpha_img.filter(ImageFilter.GaussianBlur(radius=2.0))
    char_raw.putalpha(alpha_smooth)
    
    # Redimensionar para o pôster
    char_w = 640
    char_h = int(char_w * (ch_orig / cw_orig))
    char_final = char_raw.resize((char_w, char_h), Image.Resampling.LANCZOS)
    
    # Aumentar contraste cinematográfico
    char_arr_f = np.array(char_final, dtype=float)
    char_arr_f[:,:,:3] = np.clip((char_arr_f[:,:,:3] - 128) * 1.15 + 128, 0, 255)
    char_final = Image.fromarray(char_arr_f.astype(np.uint8))
    
    char_x = 130
    char_y = 210
    poster.paste(char_final, (char_x, char_y), char_final)

    # 4. Tipografia Monumental de Alto Nível
    draw = ImageDraw.Draw(poster)
    
    font_path_serif = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
    font_path_italic = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf"
    font_path_mono = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
    font_path_mono_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
    font_path_kanji = "/root/apk-work/PROJETOS/landing-quiet-strength/NotoSerifJP-Bold.otf"

    font_serif_huge = ImageFont.truetype(font_path_serif, 114)
    font_serif_med = ImageFont.truetype(font_path_serif, 36)
    font_mono = ImageFont.truetype(font_path_mono, 14)
    font_mono_bold = ImageFont.truetype(font_path_mono_bold, 16)
    font_italic = ImageFont.truetype(font_path_italic, 18)
    font_kanji = ImageFont.truetype(font_path_kanji, 26)
    font_kanji_seal = ImageFont.truetype(font_path_kanji, 30)

    # KANJIS VERTICAIS NO LADO ESQUERDO: 静けさの中の強さ
    kanji_text = "静けさの中の強さ"
    ky = 300
    for char in kanji_text:
        draw.text((45, ky), char, fill=(20, 20, 20), font=font_kanji)
        ky += 42

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

    # Citação e Selo Hanko Autêntico com Kanji 道
    draw.text((880, 440), '"Not the absence of fear,', fill=(50, 50, 50), font=font_italic)
    draw.text((880, 465), 'but the choice to move', fill=(50, 50, 50), font=font_italic)
    draw.text((880, 490), 'forward anyway."', fill=(50, 50, 50), font=font_italic)
    
    draw.rectangle([1080, 475, 1135, 530], fill=(145, 12, 12), outline=(90, 7, 7), width=2)
    draw.text((1092, 483), "道", fill=(245, 242, 235), font=font_kanji_seal)

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
    draw.polygon([(950, 1450), (970, 1470), (990, 1435), (1010, 1470), (1030, 1450), (1020, 1485), (960, 1485)], fill=(10, 10, 10))
    draw.text((950, 1495), "SHADOW", fill=(10, 10, 10), font=font_serif_med)
    draw.text((950, 1540), "VISUAL ARCHIVE", fill=(100, 100, 100), font=font_mono)

    out_file = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/poster-fidelidade-absoluta.jpg'
    poster.save(out_file, quality=96)
    poster.save('/root/apk-work/PROJETOS/landing-quiet-strength/public/poster-render.jpg', quality=96)
    poster.save('/root/apk-work/PROJETOS/landing-quiet-strength/dist/poster-render.jpg', quality=96)
    print("Masterpiece gerada com sucesso!")

if __name__ == '__main__':
    create_masterpiece()
