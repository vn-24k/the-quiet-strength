import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def transplant_face():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg'
    out_brain = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/obra-final-1para1.jpg'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/obra-final-1para1.jpg'
    out_pub = '/root/apk-work/PROJETOS/landing-quiet-strength/public/obra-final-1para1.jpg'
    out_sd = '/sdcard/Download/the-quiet-strength/obra-final-1para1.jpg'

    ref = Image.open(ref_path).convert('RGBA')
    user = Image.open(user_path).convert('RGBA')
    
    # 1. Extrair APENAS a região do rosto e pescoço do usuário (sem corpo, sem parede externa)
    # Na foto original 903x1600:
    # Rosto e pescoço ficam em x: 160..820, y: 320..1050
    face_box = (150, 300, 830, 1080)
    user_face = user.crop(face_box)
    fw, fh = user_face.size
    
    # Criar máscara precisa para o rosto e pescoço
    char_arr = np.array(user_face, dtype=float)
    cr, cg, cb = char_arr[:,:,0], char_arr[:,:,1], char_arr[:,:,2]
    
    # Parede branca fora do rosto:
    is_wall = (cr > 195) & (cg > 190) & (cb > 180) & (abs(cr - cb) < 26)
    is_wall_shadow = (cr < 190) & (cb >= cr - 8) & (abs(cr - cg) < 18)
    wall = is_wall | is_wall_shadow
    
    # Preservar pele, óculos, bigode, tatuagem e cabelo
    is_human = (cr - cb > 22) & (cr > 95)
    is_dark = (cr < 135) & (cg < 120) & (cb < 110)
    wall = wall & ~(is_human | is_dark)
    
    alpha = np.where(wall, 0.0, 255.0)
    
    # Suavização oval nas bordas para blend perfeito com cabelo e quimono do guerreiro
    Y, X = np.ogrid[:fh, :fw]
    cx, cy = fw * 0.50, fh * 0.45
    rx, ry = fw * 0.46, fh * 0.48
    oval_mask = ((X - cx) / rx)**2 + ((Y - cy) / ry)**2
    feather = np.clip((1.15 - oval_mask) * 4.0, 0.0, 1.0)
    alpha *= feather
    
    mask_img = Image.fromarray(alpha.astype(np.uint8), mode='L').filter(ImageFilter.GaussianBlur(radius=3.0))
    user_face.putalpha(mask_img)

    # 2. Rotacionar ligeiramente (+12 graus) para casar o ângulo do queixo do guerreiro
    user_face_rot = user_face.rotate(14, resample=Image.Resampling.BICUBIC, expand=True)

    # 3. Ajuste de contraste e tom para estética cinematográfica do guerreiro
    enhancer_contrast = ImageEnhance.Contrast(user_face_rot)
    user_face_rot = enhancer_contrast.enhance(1.28)
    enhancer_brightness = ImageEnhance.Brightness(user_face_rot)
    user_face_rot = enhancer_brightness.enhance(0.92)

    # 4. Redimensionar para a escala exata da cabeça do guerreiro na referência
    # Rosto do guerreiro tem ~160px de largura e ~220px de altura
    target_face_w = 265
    target_face_h = int(target_face_w * (user_face_rot.height / user_face_rot.width))
    user_face_scaled = user_face_rot.resize((target_face_w, target_face_h), Image.Resampling.LANCZOS)

    # 5. Posicionar exatamente sobre o rosto do guerreiro
    # Nariz do guerreiro fica em torno de x=505, y=265
    # Queixo fica em torno de x=465, y=345
    # Ajustar para encaixe milimétrico:
    pos_x = 280
    pos_y = 150

    # 6. Compor sobre a referência original
    composite = ref.copy()
    composite.paste(user_face_scaled, (pos_x, pos_y), user_face_scaled)

    # Salvar resultado
    final_rgb = composite.convert('RGB')
    final_rgb.save(out_brain, quality=98)
    final_rgb.save(out_dist, quality=98)
    final_rgb.save(out_pub, quality=98)
    try:
        final_rgb.save(out_sd, quality=98)
    except:
        pass

    print("Transplante de rosto executado com sucesso!")

if __name__ == '__main__':
    transplant_face()
