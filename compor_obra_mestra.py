import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def compose_character_into_original():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg'
    out_brain = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/obra-final-1para1.jpg'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/obra-final-1para1.jpg'
    out_pub = '/root/apk-work/PROJETOS/landing-quiet-strength/public/obra-final-1para1.jpg'
    out_sd = '/sdcard/Download/the-quiet-strength/obra-final-1para1.jpg'

    # 1. Carregar arte de referência original em resolução total
    ref_img = Image.open(ref_path).convert('RGBA')
    ref_w, ref_h = ref_img.size
    print(f"Referência original carregada: {ref_w}x{ref_h}")

    # 2. Carregar foto do usuário
    user_img = Image.open(user_path).convert('RGBA')
    uw, uh = user_img.size

    # 3. Tratamento editorial de alto nível na foto do usuário:
    # Aumentar contraste e diminuir levemente brilho para casar com o nanquim da referência
    enhancer_contrast = ImageEnhance.Contrast(user_img)
    user_treated = enhancer_contrast.enhance(1.22)
    enhancer_brightness = ImageEnhance.Brightness(user_treated)
    user_treated = enhancer_brightness.enhance(0.96)
    
    # 4. Ajustar escala e posição para casar exatamente com o busto do samurai
    # Na referência (720x1080 aprox), a cabeça do samurai fica entre y: 150 e 400, x: 180 e 500
    target_char_w = int(ref_w * 0.62)
    target_char_h = int(target_char_w * (uh / uw))
    user_resized = user_treated.resize((target_char_w, target_char_h), Image.Resampling.LANCZOS)
    
    # Posição exata do busto
    pos_x = int(ref_w * 0.16)
    pos_y = int(ref_h * 0.14)

    # 5. Criar máscara de transição suave orgânica para o busto
    # Preserva o rosto, óculos, pescoço com tatuagem e gola da camisa,
    # enquanto desvanece suavemente as bordas externas no fundo e no círculo vermelho
    mask = Image.new('L', (target_char_w, target_char_h), 0)
    arr_mask = np.zeros((target_char_h, target_char_w), dtype=float)
    
    Y, X = np.ogrid[:target_char_h, :target_char_w]
    
    # Elipse central suave englobando cabeça, óculos, pescoço e peito
    cx = target_char_w * 0.52
    cy = target_char_h * 0.45
    rx = target_char_w * 0.42
    ry = target_char_h * 0.48
    
    dist_norm = ((X - cx) / rx)**2 + ((Y - cy) / ry)**2
    arr_mask = np.clip((1.0 - dist_norm) * 2.2, 0.0, 1.0) * 255.0
    
    # Fade gradual na base da camisa
    fade_y = int(target_char_h * 0.65)
    for y in range(fade_y, target_char_h):
        factor = (target_char_h - y) / (target_char_h - fade_y)
        arr_mask[y, :] *= factor
        
    mask_img = Image.fromarray(arr_mask.astype(np.uint8), mode='L')
    mask_smooth = mask_img.filter(ImageFilter.GaussianBlur(radius=8))

    # 6. Composição com mesclagem sobre o pôster original
    # Usar blend que integra o personagem na textura original
    composite = ref_img.copy()
    composite.paste(user_resized, (pos_x, pos_y), mask_smooth)

    # 7. Preservar o título monumental "THE QUIET STRENGTH" na frente do corpo
    # Recortar o texto original de 'THE QUIET STRENGTH' da referência e sobrepor na frente com transparência de preto
    text_box = (int(ref_w * 0.02), int(ref_h * 0.38), int(ref_w * 0.72), int(ref_h * 0.62))
    ref_text_crop = ref_img.crop(text_box)
    
    # Extrair apenas os pixels pretos do texto original
    text_arr = np.array(ref_text_crop, dtype=float)
    is_black_text = (text_arr[:,:,0] < 60) & (text_arr[:,:,1] < 60) & (text_arr[:,:,2] < 60)
    text_alpha = np.where(is_black_text, 255, 0).astype(np.uint8)
    text_mask = Image.fromarray(text_alpha, mode='L').filter(ImageFilter.GaussianBlur(radius=0.5))
    
    # Sobrepor o título original na frente para tridimensionalidade perfeita
    composite.paste(ref_text_crop, text_box, text_mask)

    # 8. Converter para RGB e salvar com qualidade máxima
    final_rgb = composite.convert('RGB')
    final_rgb.save(out_brain, quality=98)
    final_rgb.save(out_dist, quality=98)
    final_rgb.save(out_pub, quality=98)
    try:
        final_rgb.save(out_sd, quality=98)
    except:
        pass

    print("Composição de fidelidade absoluta 1:1 finalizada com sucesso!")

if __name__ == '__main__':
    compose_character_into_original()
