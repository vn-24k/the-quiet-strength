import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def transplant_face_full():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg'
    out_brain = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/obra-final-1para1.jpg'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/obra-final-1para1.jpg'
    out_pub = '/root/apk-work/PROJETOS/landing-quiet-strength/public/obra-final-1para1.jpg'
    out_sd = '/sdcard/Download/the-quiet-strength/obra-final-1para1.jpg'

    ref = Image.open(ref_path).convert('RGBA')
    user = Image.open(user_path).convert('RGBA')
    
    # 1. Recorte incluindo cabeça, óculos, rosto E O PESCOÇO COMPLETO COM A TATUAGEM 花樣年華
    face_box = (140, 220, 850, 1150)
    user_face = user.crop(face_box)
    fw, fh = user_face.size
    
    char_arr = np.array(user_face, dtype=float)
    cr, cg, cb = char_arr[:,:,0], char_arr[:,:,1], char_arr[:,:,2]
    
    # Parede branca fora da silhueta
    is_wall = (cr > 195) & (cg > 190) & (cb > 180) & (abs(cr - cb) < 26)
    is_wall_shadow = (cr < 190) & (cb >= cr - 8) & (abs(cr - cg) < 18)
    wall = is_wall | is_wall_shadow
    
    # Preservar o humano (pele, óculos dourados, tatuagem, cabelo, barba)
    is_human = (cr - cb > 20) & (cr > 90)
    is_dark = (cr < 135) & (cg < 120) & (cb < 110)
    wall = wall & ~(is_human | is_dark)
    
    alpha = np.where(wall, 0.0, 255.0)
    
    # Suavização oval com foco anatômico
    Y, X = np.ogrid[:fh, :fw]
    cx, cy = fw * 0.52, fh * 0.46
    rx, ry = fw * 0.46, fh * 0.50
    oval = ((X - cx) / rx)**2 + ((Y - cy) / ry)**2
    feather = np.clip((1.18 - oval) * 4.0, 0.0, 1.0)
    alpha *= feather
    
    # Fade out suave na base do pescoço para transição perfeita com o quimono
    fade_y = int(fh * 0.76)
    for y in range(fade_y, fh):
        alpha[y, :] *= (fh - y) / (fh - fade_y)
        
    mask_img = Image.fromarray(alpha.astype(np.uint8), mode='L').filter(ImageFilter.GaussianBlur(radius=2.2))
    user_face.putalpha(mask_img)

    # 2. Rotação anatômica (18 graus)
    user_face_rot = user_face.rotate(18, resample=Image.Resampling.BICUBIC, expand=True)

    # 3. Tratamento de contraste e tonalidade cinematográfica
    enhancer_contrast = ImageEnhance.Contrast(user_face_rot)
    user_face_rot = enhancer_contrast.enhance(1.26)
    enhancer_brightness = ImageEnhance.Brightness(user_face_rot)
    user_face_rot = enhancer_brightness.enhance(0.93)

    # 4. Escala para cobrir exatamente a cabeça, orelha e queixo do guerreiro original
    target_face_w = 380
    target_face_h = int(target_face_w * (user_face_rot.height / user_face_rot.width))
    user_face_scaled = user_face_rot.resize((target_face_w, target_face_h), Image.Resampling.LANCZOS)

    # 5. Posicionamento para encaixe 100% sobre o rosto antigo e conexão com o quimono
    pos_x = 245
    pos_y = 100

    # 6. Composição limpa
    composite = ref.copy()
    composite.paste(user_face_scaled, (pos_x, pos_y), user_face_scaled)

    # Salvar resultado final
    final_rgb = composite.convert('RGB')
    final_rgb.save(out_brain, quality=98)
    final_rgb.save(out_dist, quality=98)
    final_rgb.save(out_pub, quality=98)
    try:
        final_rgb.save(out_sd, quality=98)
    except:
        pass

    print("Transplante completo com tatuagem e quimono finalizado com sucesso!")

if __name__ == '__main__':
    transplant_face_full()
