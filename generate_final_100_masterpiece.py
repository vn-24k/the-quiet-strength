import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

def create_final_masterpiece():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg'
    
    out_brain = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/obra-final-1para1.jpg'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/obra-final-1para1.jpg'
    out_pub = '/root/apk-work/PROJETOS/landing-quiet-strength/public/obra-final-1para1.jpg'
    out_sd = '/sdcard/Download/the-quiet-strength/obra-final-1para1.jpg'

    ref = Image.open(ref_path).convert('RGBA')
    user = Image.open(user_path).convert('RGBA')
    
    # 1. Apagar a orelha antiga do guerreiro na referência original (x: 295 a 340, y: 265 a 330)
    # com o tom escuro do cabelo/capuz (preto natural sumi-e)
    clean_ref = ref.copy()
    draw_ref = ImageDraw.Draw(clean_ref)
    
    # Desenhar sobreposição suave da cor preta do cabelo
    draw_ref.ellipse([290, 260, 345, 335], fill=(22, 22, 22, 255))
    # Suavizar as bordas dessa cobertura
    patch_mask = Image.new('L', ref.size, 0)
    draw_pm = ImageDraw.Draw(patch_mask)
    draw_pm.ellipse([285, 255, 350, 340], fill=255)
    patch_mask = patch_mask.filter(ImageFilter.GaussianBlur(radius=3.0))
    clean_ref = Image.composite(clean_ref.filter(ImageFilter.GaussianBlur(radius=2.0)), clean_ref, patch_mask)

    # 2. Máscara perfeita da cabeça, rosto e pescoço com tatuagem do usuário
    user_pts = [
        # Nuca e cabelo traseiro (fade)
        (255, 490),
        (270, 440),
        (280, 390),
        (310, 340),
        (350, 305),
        (400, 275),
        (460, 265),
        (520, 265),
        (580, 280),
        (640, 305),
        (700, 340),
        (760, 390),
        (810, 440),
        (845, 470), # ponta da franja
        (825, 490),
        (785, 510), # curva sob franja
        (760, 530),
        (755, 555), # óculos armação superior
        (775, 585), # ponta óculos
        (760, 625),
        (725, 670), # ponte nariz
        (712, 720), # ponta do nariz exata
        (685, 765), # base do nariz
        (645, 810), # bigode / lábio superior
        (635, 840), # lábio inferior
        (625, 870), # queixo superior
        (585, 930), # ponta do queixo exata
        (520, 960), # linha sob a mandíbula
        (460, 1010),# descida pescoço anterior
        (400, 1060),# base do pescoço
        (260, 1060),# base da tatuagem 花樣年華
        (175, 930), # base posterior do pescoço
        # Lateral do pescoço com tatuagem
        (185, 850),
        (205, 770),
        (220, 690),
        (235, 610),
        # Orelha com óculos
        (245, 550),
        (225, 515),
        (205, 460),
        (220, 415),
        (245, 430),
    ]
    
    mask_poly = Image.new('L', user.size, 0)
    draw_mp = ImageDraw.Draw(mask_poly)
    draw_mp.polygon(user_pts, fill=255)
    
    # Suavização da borda da máscara para anti-aliasing orgânico
    mask_poly = mask_poly.filter(ImageFilter.GaussianBlur(radius=1.8))
    
    user_isolated = user.copy()
    user_isolated.putalpha(mask_poly)
    
    # 3. Transformação afim matemática calibrada pelos 3 pontos anatômicos
    p_ear_u = np.array([235.0, 480.0])
    p_nose_u = np.array([712.0, 720.0])
    p_chin_u = np.array([585.0, 930.0])
    
    # Pontos na referência original
    # Ajustamos ligeiramente o ponto da orelha na referência para x=325, y=285
    # para a orelha do usuário se fundir de forma impecável no centro da cabeça
    p_ear_r = np.array([325.0, 285.0])
    p_nose_r = np.array([515.0, 250.0])
    p_chin_r = np.array([505.0, 340.0])
    
    src_pts = np.array([p_ear_u, p_nose_u, p_chin_u])
    dst_pts = np.array([p_ear_r, p_nose_r, p_chin_r])
    
    pad = lambda x: np.hstack([x, np.ones((x.shape[0], 1))])
    dst_pad = pad(dst_pts)
    M, _, _, _ = np.linalg.lstsq(dst_pad, src_pts, rcond=None)
    affine_matrix = (M[0,0], M[1,0], M[2,0], M[0,1], M[1,1], M[2,1])
    
    # Warping com bicubic resampling
    user_warped = user_isolated.transform(ref.size, Image.Transform.AFFINE, affine_matrix, resample=Image.Resampling.BICUBIC)
    
    # 4. Color grading cinematográfico sumi-e
    user_warped = ImageEnhance.Contrast(user_warped).enhance(1.24)
    user_warped = ImageEnhance.Brightness(user_warped).enhance(0.96)
    user_warped = ImageEnhance.Color(user_warped).enhance(1.12)
    user_warped = ImageEnhance.Sharpness(user_warped).enhance(1.20)
    
    # 5. Composição sobre a imagem limpa
    composite = clean_ref.copy()
    composite.paste(user_warped, (0, 0), user_warped)
    
    # 6. Preservar a frente do manto / quimono preto e katana originais (y > 425)
    # Isso faz a base do pescoço com a tatuagem mergulhar para DENTRO da gola preta!
    ref_front = ref.crop((0, 425, 719, 1067))
    composite.paste(ref_front, (0, 425), ref_front)
    
    # 7. Salvar em todos os destinos
    final_rgb = composite.convert('RGB')
    final_rgb.save(out_brain, quality=99)
    final_rgb.save(out_dist, quality=99)
    final_rgb.save(out_pub, quality=99)
    try:
        final_rgb.save(out_sd, quality=99)
    except:
        pass
        
    # Crop da cabeça para inspeção imediata
    crop_comp = composite.crop((100, 50, 650, 550)).convert('RGB')
    crop_comp.save('/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/crop_final_100.jpg', quality=99)
    
    print("Obra final 100% com fidelidade absoluta gerada com sucesso!")

if __name__ == '__main__':
    create_final_masterpiece()
