import numpy as np
from PIL import Image, ImageFilter

def refine_character():
    src_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg'
    out_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem-recortado.png'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/personagem-recortado.png'

    img = Image.open(src_path).convert('RGBA')
    arr = np.array(img, dtype=float)
    h, w, _ = arr.shape
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

    # Criar grade de coordenadas Y, X
    Y, X = np.ogrid[:h, :w]

    # Máscara de parede
    # 1. Toda área à direita do rosto/ombro onde o fundo é a parede branca
    # O contorno do rosto termina em torno de x=750 nos olhos, x=650 na boca/queixo, x=750 no ombro
    is_wall_top = Y < 220
    is_wall_far_right = (X > 730) & (Y < 600)
    is_wall_right_mid = (X > 700) & (Y >= 600) & (Y < 950)
    is_wall_right_low = (X > 680) & (Y >= 950)
    
    # Parede branca clara por intensidade (R, G, B altos e próximos)
    is_bright_wall = (r > 200) & (g > 195) & (b > 185) & (abs(r - g) < 22) & (abs(r - b) < 25)
    
    # Sombra da parede à esquerda (fora da orelha e fora do pescoço)
    is_wall_left_high = (X < 260) & (Y < 500)
    is_wall_left_mid = (X < 150) & (Y >= 500) & (Y < 750)
    is_wall_shadow = (b >= r - 8) & (g >= r - 12) & (r < 195) & (X < 300)

    # Combinar tudo que é parede garantida
    wall_mask = is_wall_top | is_wall_far_right | is_wall_right_mid | is_wall_right_low | is_wall_left_high | is_wall_left_mid
    wall_mask = wall_mask | ((X > 600) & is_bright_wall)
    wall_mask = wall_mask | ((X < 280) & is_wall_shadow & (Y < 750))

    # Definir o sujeito
    subject = ~wall_mask

    # Garantir que a cabeça, óculos, rosto, pescoço e camisa estejam totalmente preservados
    # Limites anatômicos da pessoa:
    # Cabeça e cabelo: Y entre 220 e 550, X entre 280 e 850
    # Rosto e óculos: Y entre 330 e 750, X entre 280 e 750
    # Pescoço e tatuagem: Y entre 700 e 1050, X entre 160 e 500
    # Camisa: Y >= 950, X entre 0 e 700
    is_person_core = (
        ((Y >= 230) & (Y <= 550) & (X >= 280) & (X <= 840) & (r < 220)) |
        ((Y > 550) & (Y <= 750) & (X >= 260) & (X <= 720)) |
        ((Y > 750) & (Y <= 1000) & (X >= 160) & (X <= 550)) |
        ((Y > 950) & (X >= 0) & (X <= 700) & ~(is_wall_right_low))
    )
    subject = subject | is_person_core

    # Refinar corte fino da parede na direita (a parede branca na direita encosta no rosto)
    # Qualquer pixel com brilho excessivo na direita é parede
    subject = subject & ~((X > 650) & (r > 215) & (g > 215) & (b > 210))
    subject = subject & ~((X < 230) & (Y < 650))

    # Converter para canal alfa [0..255]
    alpha = np.where(subject, 255.0, 0.0)

    # Fade out orgânico na base (últimos 18% da altura)
    fade_start = int(h * 0.80)
    for y in range(fade_start, h):
        factor = (h - y) / (h - fade_start)
        alpha[y, :] *= factor

    # Suavizar as bordas com Gaussian Blur para transição fotográfica ultra-realista
    alpha_img = Image.fromarray(alpha.astype(np.uint8), mode='L')
    alpha_smooth = alpha_img.filter(ImageFilter.GaussianBlur(radius=2.0))

    # Aplicar novo canal alfa
    img.putalpha(alpha_smooth)

    img.save(out_path, format='PNG')
    img.save(out_dist, format='PNG')
    img.save('/root/.gemini/antigravity-cli/brain/69d939c5-e16a-423b-88ad-af3acd5ee745/personagem-recortado.png', format='PNG')
    print("Recorte refinado com sucesso!")

if __name__ == '__main__':
    refine_character()
