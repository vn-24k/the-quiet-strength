import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

def create_true_clean():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem-silhueta-perfeita.png'
    out_brain = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/obra-final-1para1.jpg'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/obra-final-1para1.jpg'
    out_pub = '/root/apk-work/PROJETOS/landing-quiet-strength/public/obra-final-1para1.jpg'
    out_sd = '/sdcard/Download/the-quiet-strength/obra-final-1para1.jpg'

    ref_img = Image.open(ref_path).convert('RGBA')
    ref_w, ref_h = ref_img.size

    composite = ref_img.copy()
    draw_comp = ImageDraw.Draw(composite)
    
    # 1. Limpar a cabeça do samurai antigo no círculo vermelho com textura carmesim suave
    draw_comp.ellipse([110, 80, 560, 530], fill=(138, 16, 18, 255))
    
    # Texturas sutis no círculo vermelho
    np.random.seed(42)
    for _ in range(60):
        rx = np.random.randint(140, 530)
        ry = np.random.randint(100, 500)
        draw_comp.ellipse([rx, ry, rx + 16, ry + 16], fill=(95, 8, 10, 35))

    # 2. Carregar o usuário com silhueta perfeita
    user_img = Image.open(user_path).convert('RGBA')
    uw, uh = user_img.size

    # Ajuste de contraste para estética de estúdio
    enhancer_contrast = ImageEnhance.Contrast(user_img)
    user_treated = enhancer_contrast.enhance(1.20)
    
    # Escala para encaixe ideal no pôster
    target_w = 490
    target_h = int(target_w * (uh / uw)) # ~868px
    user_scaled = user_treated.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Posicionamento exato da cabeça dentro do sol carmesim
    pos_x = 105
    pos_y = 135

    # Fade out suave na base do peito
    char_arr = np.array(user_scaled)
    alpha = char_arr[:,:,3].astype(float)
    fade_start = int(target_h * 0.58)
    for y in range(fade_start, target_h):
        factor = max(0.0, (target_h * 0.88 - y) / (target_h * 0.30))
        alpha[y, :] *= factor
    char_arr[:,:,3] = alpha.astype(np.uint8)
    user_scaled = Image.fromarray(char_arr)

    # 3. Colar o usuário na frente do círculo vermelho (Sem cobrir o rosto dele com o quimono antigo!)
    composite.paste(user_scaled, (pos_x, pos_y), user_scaled)

    # 4. Salvar resultado final em alta definição
    final_rgb = composite.convert('RGB')
    final_rgb.save(out_brain, quality=98)
    final_rgb.save(out_dist, quality=98)
    final_rgb.save(out_pub, quality=98)
    try:
        final_rgb.save(out_sd, quality=98)
    except:
        pass

    print("Obra limpa gerada com sucesso!")

if __name__ == '__main__':
    create_true_clean()
