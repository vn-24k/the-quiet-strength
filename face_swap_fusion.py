import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

def blend_face():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg'
    
    ref = Image.open(ref_path).convert('RGBA')
    user = Image.open(user_path).convert('RGBA')
    
    # 1. Recorte focado estritamente no ROSTO, ÓCULOS e PESCOÇO COM TATUAGEM
    # Na imagem do usuário (903 x 1600):
    # Vamos usar uma máscara precisa desenhada exatamente sobre as características faciais do usuário:
    # Orelha, têmpora, armação do óculos, nariz, lábio, queixo, mandíbula, pescoço com tatuagem
    face_pts = [
        # Início na frente da orelha / têmpora
        (320, 390),
        (380, 340),
        (460, 310),
        (540, 310),
        (620, 330),
        (700, 370),
        (760, 420),
        (780, 460), # início da testa/têmpora
        (750, 500), # descida têmpora
        (765, 540), # armação óculos dourada
        (775, 580), # ponta óculos
        (745, 625),
        (715, 670), # ponte nariz
        (710, 715), # ponta do nariz (calibrada no pixel 712)
        (680, 760), # base do nariz
        (645, 805), # lábio superior
        (635, 835), # lábio inferior
        (625, 865), # queixo superior
        (585, 925), # ponta do queixo (calibrada no pixel 590)
        (520, 950), # mandíbula sob o queixo
        (460, 1000),# garganta / pescoço anterior
        (380, 1050),# descida pescoço
        (250, 1050),# base da tatuagem
        (175, 930), # base posterior do pescoço
        # Lateral do pescoço com a tatuagem 花樣年華
        (185, 850),
        (205, 770),
        (220, 690),
        (235, 610),
        # Orelha com haste do óculos
        (245, 550),
        (225, 515),
        (205, 460),
        (220, 415),
        (250, 425),
        (280, 410),
    ]
    
    mask = Image.new('L', user.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(face_pts, fill=255)
    
    # Suavizar as bordas da máscara para uma fusão gradual e orgânica
    mask_soft = mask.filter(ImageFilter.GaussianBlur(radius=3.5))
    
    user_face = user.copy()
    user_face.putalpha(mask_soft)
    
    bbox = mask.getbbox()
    user_face = user_face.crop(bbox)
    
    # 2. Rotação anatômica
    # O guerreiro da referência tem a mandíbula inclinada para cima
    # Girar 32 graus no sentido anti-horário
    user_rot = user_face.rotate(32.0, resample=Image.Resampling.BICUBIC, expand=True)
    
    # 3. Color grading para igualar a estética editorial da referência
    # Contraste cinematográfico
    user_rot = ImageEnhance.Contrast(user_rot).enhance(1.22)
    # Brilho
    user_rot = ImageEnhance.Brightness(user_rot).enhance(0.95)
    # Saturação dos óculos dourados
    user_rot = ImageEnhance.Color(user_rot).enhance(1.10)
    # Nitidez
    user_rot = ImageEnhance.Sharpness(user_rot).enhance(1.20)
    
    # 4. Escala para casar com a anatomia do guerreiro da referência (719 x 1067)
    # Distância orelha-nariz no guerreiro é ~205px
    rw, rh = user_rot.size
    target_h = 310
    target_w = int(rw * (target_h / rh))
    user_scaled = user_rot.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # 5. Composição na referência original
    # Na referência original (sem manchas e sem borrões):
    composite = ref.copy()
    
    # Vamos testar o posicionamento para a ponta do nariz bater em (515, 250)
    # e a orelha bater em (310, 290)
    pos_x = 245
    pos_y = 105
    
    composite.paste(user_scaled, (pos_x, pos_y), user_scaled)
    
    # Crop da cabeça para inspeção imediata
    crop_comp = composite.crop((100, 50, 650, 550)).convert('RGB')
    crop_comp.save('/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/crop_fusion_test.jpg', quality=98)
    
    # Salvar pôster completo
    final_rgb = composite.convert('RGB')
    final_rgb.save('/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/fusion_test_full.jpg', quality=98)
    
    print(f"Fusion test gerado com sucesso! Tamanho: {target_w}x{target_h} em pos: ({pos_x}, {pos_y})")

if __name__ == '__main__':
    blend_face()
