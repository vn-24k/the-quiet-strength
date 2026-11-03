import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageEnhance

def render_perfection():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_cutout_path = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/user_true_cutout.png'
    
    out_brain = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/obra-final-1para1.jpg'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/obra-final-1para1.jpg'
    out_pub = '/root/apk-work/PROJETOS/landing-quiet-strength/public/obra-final-1para1.jpg'
    out_sd = '/sdcard/Download/the-quiet-strength/obra-final-1para1.jpg'

    ref = Image.open(ref_path).convert('RGBA')
    user_cut = Image.open(user_cutout_path).convert('RGBA')
    
    # 1. Rotação anatômica: 36.5 graus anti-horário
    rot_angle = 36.5
    user_rot = user_cut.rotate(rot_angle, resample=Image.Resampling.BICUBIC, expand=True)
    
    # 2. Color grading cinematográfico
    # Contraste cinema (+20%)
    user_rot = ImageEnhance.Contrast(user_rot).enhance(1.20)
    # Brilho
    user_rot = ImageEnhance.Brightness(user_rot).enhance(0.96)
    # Cores quentes e dourado dos óculos (+10%)
    user_rot = ImageEnhance.Color(user_rot).enhance(1.10)
    # Nitidez (+15%)
    user_rot = ImageEnhance.Sharpness(user_rot).enhance(1.15)
    
    # 3. Escala para coincidir exatamente com a face do guerreiro na referência (719 x 1067)
    rw, rh = user_rot.size
    target_h = 355
    target_w = int(rw * (target_h / rh))
    user_scaled = user_rot.resize((target_w, target_h), Image.Resampling.LANCZOS)
    
    # 4. Imagem base limpa: cobrir com preto a orelha antiga e sombra residual do guerreiro (x: 290-345, y: 260-340)
    clean_base = ref.copy()
    draw_cb = ImageDraw.Draw(clean_base)
    # Cobrir a orelha antiga com a cor escura do cabelo
    draw_cb.ellipse([290, 260, 345, 335], fill=(24, 24, 24, 255))
    
    # Suavizar o patch preto para fundir com o cabelo
    patch_mask = Image.new('L', ref.size, 0)
    draw_pm = ImageDraw.Draw(patch_mask)
    draw_pm.ellipse([285, 255, 350, 340], fill=255)
    patch_mask = patch_mask.filter(ImageFilter.GaussianBlur(radius=3.0))
    clean_base = Image.composite(clean_base.filter(ImageFilter.GaussianBlur(radius=1.8)), clean_base, patch_mask)
    
    # 5. Colar a cabeça do usuário na posição exata:
    # Onde a orelha do usuário cobre a orelha antiga e o nariz/queixo ficam no perfil exato do guerreiro
    pos_x = 238
    pos_y = 92
    
    clean_base.paste(user_scaled, (pos_x, pos_y), user_scaled)
    
    # 6. Preservar o manto preto / quimono inferior e katana autênticos da referência (y > 425)
    # Isso faz a base do pescoço com a tatuagem oriental的花樣年華 mergulhar organicamente para dentro do manto!
    ref_front = ref.crop((0, 425, 719, 1067))
    clean_base.paste(ref_front, (0, 425), ref_front)
    
    # 7. Salvar obra-prima definitiva em todos os caminhos
    final_rgb = clean_base.convert('RGB')
    final_rgb.save(out_brain, quality=99)
    final_rgb.save(out_dist, quality=99)
    final_rgb.save(out_pub, quality=99)
    try:
        final_rgb.save(out_sd, quality=99)
    except:
        pass
        
    crop_comp = clean_base.crop((100, 50, 650, 550)).convert('RGB')
    crop_comp.save('/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/crop_absolute_perfection.jpg', quality=99)
    print(f"Obra de fidelidade absoluta 1:1 renderizada com sucesso! Escala: {target_w}x{target_h} em pos: ({pos_x}, {pos_y})")

if __name__ == '__main__':
    render_perfection()
