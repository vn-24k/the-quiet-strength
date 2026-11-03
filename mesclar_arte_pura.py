import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def blend_user_into_original():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem-silhueta-perfeita.png'
    out_brain = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/obra-final-1para1.jpg'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/obra-final-1para1.jpg'
    out_pub = '/root/apk-work/PROJETOS/landing-quiet-strength/public/obra-final-1para1.jpg'
    out_sd = '/sdcard/Download/the-quiet-strength/obra-final-1para1.jpg'

    # Carregar a arte de referência original pura (SEM nenhum círculo falso desenhado em cima!)
    ref_img = Image.open(ref_path).convert('RGBA')
    ref_w, ref_h = ref_img.size

    # Carregar silhueta do usuário
    user_img = Image.open(user_path).convert('RGBA')
    uw, uh = user_img.size

    # Contraste cinematográfico com pretos profundos
    enhancer_contrast = ImageEnhance.Contrast(user_img)
    user_treated = enhancer_contrast.enhance(1.25)
    enhancer_brightness = ImageEnhance.Brightness(user_treated)
    user_treated = enhancer_brightness.enhance(0.96)

    # Escala para encaixe exato sobre a cabeça e busto do samurai
    target_w = 560
    target_h = int(target_w * (uh / uw)) # ~992px
    user_scaled = user_treated.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Posicionamento milimétrico para cobrir o rosto e cabelos do samurai antigo
    pos_x = 75
    pos_y = 55

    # Fade out suave na base do peito
    char_arr = np.array(user_scaled)
    alpha = char_arr[:,:,3].astype(float)
    fade_start = int(target_h * 0.50)
    for y in range(fade_start, target_h):
        factor = max(0.0, (target_h * 0.75 - y) / (target_h * 0.25))
        alpha[y, :] *= factor
    char_arr[:,:,3] = alpha.astype(np.uint8)
    user_scaled = Image.fromarray(char_arr)

    # Compor diretamente sobre a arte original pura
    composite = ref_img.copy()
    composite.paste(user_scaled, (pos_x, pos_y), user_scaled)

    # Salvar resultado final
    final_rgb = composite.convert('RGB')
    final_rgb.save(out_brain, quality=98)
    final_rgb.save(out_dist, quality=98)
    final_rgb.save(out_pub, quality=98)
    try:
        final_rgb.save(out_sd, quality=98)
    except:
        pass

    print("Composição 100% sobre arte original pura concluída!")

if __name__ == '__main__':
    blend_user_into_original()
