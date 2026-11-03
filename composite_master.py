import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

def make_composite():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg'
    
    ref = Image.open(ref_path).convert('RGBA')
    user = Image.open(user_path).convert('RGBA')
    
    # 1. Recorte dos traços faciais e pescoço com tatuagem
    # Pontos calibrados que preservam nariz, boca, queixo, mandíbula, óculos, orelha e tatuagem:
    pts = [
        # Topo da testa e cabelo
        (350, 310),
        (420, 280),
        (500, 275),
        (580, 290),
        (660, 320),
        (720, 360),
        (760, 400),
        (790, 440),
        (800, 470),
        (770, 500), # frente da têmpora
        (760, 530), # armação óculos
        (770, 570), # ponta óculos
        (750, 610),
        (720, 660), # descida nariz
        (725, 730), # ponta do nariz
        (695, 775), # base do nariz
        (660, 815), # lábio superior / bigode
        (645, 840), # lábio inferior
        (635, 870), # queixo superior
        (580, 930), # ponta do queixo
        (500, 960), # linha sob o queixo
        (450, 1010),# descida pescoço
        (390, 1050),# base pescoço
        (260, 1030),# base inferior da tatuagem
        (175, 920), # início da nuca/pescoço
        (185, 850), # pescoço com tatuagem
        (205, 770),
        (225, 690),
        (240, 610),
        # Orelha
        (245, 555),
        (225, 520),
        (205, 460),
        (220, 415),
        (255, 430),
        (280, 410),
        (310, 360),
    ]
    
    mask = Image.new('L', user.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.polygon(pts, fill=255)
    
    # Suavização da borda para não ter arestas duras
    mask_blurred = mask.filter(ImageFilter.GaussianBlur(radius=3.0))
    
    user_cut = user.copy()
    user_cut.putalpha(mask_blurred)
    
    bbox = mask.getbbox()
    user_cut = user_cut.crop(bbox)
    
    # 2. Rotação anatômica
    # Ângulo calculado: 37 graus no sentido anti-horário
    # para casar perfeitamente o perfil do guerreiro
    rot_angle = 37.0
    user_rot = user_cut.rotate(rot_angle, resample=Image.Resampling.BICUBIC, expand=True)
    
    # 3. Tratamento de cor e contraste de cinema:
    # Aumentar contraste, ajustar calor e nível de preto para bater com o pôster
    enhancer_con = ImageEnhance.Contrast(user_rot)
    user_rot = enhancer_con.enhance(1.22)
    enhancer_bri = ImageEnhance.Brightness(user_rot)
    user_rot = enhancer_bri.enhance(0.96)
    enhancer_col = ImageEnhance.Color(user_rot)
    user_rot = enhancer_col.enhance(1.08)
    
    # 4. Escala milimétrica para caber no rosto do guerreiro
    # O guerreiro tem ~210px da orelha até a ponta do nariz na imagem de 719x1067
    orig_w, orig_h = user_rot.size
    # Fator de escala
    scale_factor = 0.46
    target_w = int(orig_w * scale_factor)
    target_h = int(orig_h * scale_factor)
    user_scaled = user_rot.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # 5. Composição na referência original
    composite = ref.copy()
    
    # Posição de colagem para o nariz bater em x ~ 515, y ~ 250
    # e queixo bater em x ~ 505, y ~ 340
    # Vamos calcular a posição exata
    pos_x = 200
    pos_y = 100
    
    composite.paste(user_scaled, (pos_x, pos_y), user_scaled)
    
    # Salvar o pôster completo
    final_rgb = composite.convert('RGB')
    final_rgb.save('/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/test_composite_master.jpg', quality=98)
    
    # Salvar o crop da cabeça para inspecionar os detalhes
    crop_comp = composite.crop((100, 50, 650, 550)).convert('RGB')
    crop_comp.save('/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/test_crop_master.jpg', quality=98)
    
    print(f"Master composite gerado! Tamanho: {target_w}x{target_h} em pos: ({pos_x}, {pos_y})")

if __name__ == '__main__':
    make_composite()
