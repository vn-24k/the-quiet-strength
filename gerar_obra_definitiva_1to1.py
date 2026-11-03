import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageDraw

def create_true_1to1_masterpiece():
    ref_path = '/root/apk-work/REFERENCIAS-VISUAIS/b06d9948-87d9-4350-a005-8e1f970af038.jpg'
    user_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem-silhueta-perfeita.png'
    out_brain = '/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/obra-final-1para1.jpg'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/obra-final-1para1.jpg'
    out_pub = '/root/apk-work/PROJETOS/landing-quiet-strength/public/obra-final-1para1.jpg'
    out_sd = '/sdcard/Download/the-quiet-strength/obra-final-1para1.jpg'

    ref_img = Image.open(ref_path).convert('RGBA')
    ref_w, ref_h = ref_img.size

    # 1. Limpar a cabeça do samurai original preenchendo o círculo vermelho
    # O círculo vermelho da referência tem centro em torno de x=330, y=300, raio ~230
    composite = ref_img.copy()
    draw_comp = ImageDraw.Draw(composite)
    
    # Preencher a área da cabeça antiga com a cor do círculo carmesim da referência
    # Círculo carmesim: [142, 18, 20] com textura sumi-e
    draw_comp.ellipse([110, 80, 560, 530], fill=(140, 18, 20, 255))
    
    # Textura nanquim dentro do círculo
    np.random.seed(108)
    for _ in range(80):
        rx = np.random.randint(150, 520)
        ry = np.random.randint(120, 490)
        draw_comp.ellipse([rx, ry, rx + np.random.randint(10, 30), ry + np.random.randint(10, 30)], fill=(85, 10, 12, 40))

    # Suavizar as bordas do círculo carmesim restaurado
    composite = composite.filter(ImageFilter.GaussianBlur(radius=1.0))

    # 2. Carregar a silhueta pura do usuário (onde o fundo da parede já é 100% transparente)
    user_img = Image.open(user_path).convert('RGBA')
    uw, uh = user_img.size

    # Ajuste fino de contraste cinematográfico e nitidez
    enhancer_contrast = ImageEnhance.Contrast(user_img)
    user_treated = enhancer_contrast.enhance(1.18)
    
    # Redimensionar para encaixar no círculo vermelho (largura ~480px)
    target_w = 480
    target_h = int(target_w * (uh / uw)) # ~850px
    user_scaled = user_treated.resize((target_w, target_h), Image.Resampling.LANCZOS)

    # Posição perfeita: cabeça centralizada no círculo carmesim
    pos_x = 110
    pos_y = 120

    # Fade out suave na base da camisa para fundir com o quimono escuro original
    char_arr = np.array(user_scaled)
    alpha = char_arr[:,:,3].astype(float)
    fade_start = int(target_h * 0.55)
    for y in range(fade_start, target_h):
        factor = max(0.0, (target_h * 0.85 - y) / (target_h * 0.30))
        alpha[y, :] *= factor
    char_arr[:,:,3] = alpha.astype(np.uint8)
    user_scaled = Image.fromarray(char_arr)

    # 3. Colar o usuário na frente do círculo vermelho
    composite.paste(user_scaled, (pos_x, pos_y), user_scaled)

    # 4. Sobrepor a tipografia original de 'THE QUIET STRENGTH' na frente
    # Recortar o texto original da referência original e aplicar na frente
    text_crop_box = (0, int(ref_h * 0.35), int(ref_w * 0.72), int(ref_h * 0.65))
    orig_text_crop = ref_img.crop(text_crop_box)
    
    # Extrair apenas as letras pretas do título
    t_arr = np.array(orig_text_crop, dtype=float)
    is_letter = (t_arr[:,:,0] < 60) & (t_arr[:,:,1] < 60) & (t_arr[:,:,2] < 60)
    letter_mask = Image.fromarray(np.where(is_letter, 255, 0).astype(np.uint8), mode='L')
    letter_mask = letter_mask.filter(ImageFilter.GaussianBlur(radius=0.5))

    composite.paste(orig_text_crop, text_crop_box, letter_mask)

    # 5. Salvar resultado final com qualidade máxima
    final_rgb = composite.convert('RGB')
    final_rgb.save(out_brain, quality=98)
    final_rgb.save(out_dist, quality=98)
    final_rgb.save(out_pub, quality=98)
    try:
        final_rgb.save(out_sd, quality=98)
    except:
        pass

    print("Obra final com paridade absoluta gerada!")

if __name__ == '__main__':
    create_true_1to1_masterpiece()
