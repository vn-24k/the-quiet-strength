import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def align_character_cover_samurai():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg'
    out_brain = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/obra-final-1para1.jpg'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/obra-final-1para1.jpg'
    out_pub = '/root/apk-work/PROJETOS/landing-quiet-strength/public/obra-final-1para1.jpg'
    out_sd = '/sdcard/Download/the-quiet-strength/obra-final-1para1.jpg'

    ref_img = Image.open(ref_path).convert('RGBA')
    ref_w, ref_h = ref_img.size

    user_img = Image.open(user_path).convert('RGBA')
    uw, uh = user_img.size

    # Ajuste de tom para contraste cinematográfico
    enhancer_contrast = ImageEnhance.Contrast(user_img)
    user_treated = enhancer_contrast.enhance(1.22)
    enhancer_brightness = ImageEnhance.Brightness(user_treated)
    user_treated = enhancer_brightness.enhance(0.96)

    # Escala para cobrir completamente a cabeça e cabelo do samurai
    target_w = 660
    target_h = int(target_w * (uh / uw)) # ~1170px
    user_scaled = user_treated.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Posição calculada para alinhar a testa e o cabelo cobrindo todo o samurai
    pos_x = 65
    pos_y = -40

    # Máscara precisa da pessoa
    char_arr = np.array(user_scaled, dtype=float)
    cr, cg, cb = char_arr[:,:,0], char_arr[:,:,1], char_arr[:,:,2]
    
    # Parede branca da foto
    is_wall = (cr > 200) & (cg > 195) & (cb > 185) & (abs(cr - cb) < 25)
    is_wall_shadow = (cr < 190) & (cb >= cr - 8) & (abs(cr - cg) < 18)
    wall = is_wall | is_wall_shadow
    
    # Proteger humano (pele, óculos dourados, tatuagem, cabelo, camisa)
    is_human = (cr - cb > 22) & (cr > 95)
    is_hair = (cr < 135) & (cg < 120) & (cb < 110)
    is_dark_shirt = (cr < 60) & (cg < 60) & (cb < 60)
    
    wall = wall & ~(is_human | is_hair | is_dark_shirt)
    
    alpha = np.where(wall, 0.0, 255.0)
    
    # Fade out suave na altura do peito para fundir no quimono escuro original
    fade_start = int(target_h * 0.42)
    fade_end = int(target_h * 0.60)
    for y in range(fade_start, target_h):
        if y < fade_end:
            alpha[y, :] *= (fade_end - y) / (fade_end - fade_start)
        else:
            alpha[y, :] = 0.0
            
    mask_img = Image.fromarray(alpha.astype(np.uint8), mode='L')
    mask_smooth = mask_img.filter(ImageFilter.GaussianBlur(radius=3.0))

    # Compor
    composite = ref_img.copy()
    composite.paste(user_scaled, (pos_x, pos_y), mask_smooth)

    # Salvar resultado
    final_rgb = composite.convert('RGB')
    final_rgb.save(out_brain, quality=98)
    final_rgb.save(out_dist, quality=98)
    final_rgb.save(out_pub, quality=98)
    try:
        final_rgb.save(out_sd, quality=98)
    except:
        pass

    print("Cobertura total concluída!")

if __name__ == '__main__':
    align_character_cover_samurai()
