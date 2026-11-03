import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

def process_character():
    src_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem.jpg'
    out_path = '/root/apk-work/PROJETOS/landing-quiet-strength/public/personagem-recortado.png'
    out_dist = '/root/apk-work/PROJETOS/landing-quiet-strength/dist/personagem-recortado.png'

    img = Image.open(src_path).convert('RGBA')
    arr = np.array(img, dtype=float)
    h, w, _ = arr.shape
    r, g, b = arr[:,:,0], arr[:,:,1], arr[:,:,2]

    # Identificar parede de fundo clara (direita) e parede sombreada (esquerda)
    is_wall_right = (r > 218) & (g > 215) & (b > 210) & (abs(r - g) < 20) & (abs(r - b) < 25)
    is_wall_left = (b >= r - 8) & (g >= r - 12) & (r < 195)
    bg_mask = is_wall_right | is_wall_left

    # Flood fill a partir dos cantos para garantir que apenas o fundo conectado seja removido
    labeled, num_features = ndimage.label(bg_mask)
    # Cantos
    corner_labels = {
        labeled[0, 0], labeled[0, w-1], labeled[0, w//2],
        labeled[10, 10], labeled[10, w-10], labeled[h//4, w-1]
    }
    corner_labels.discard(0)

    true_bg = np.isin(labeled, list(corner_labels))

    # Inverter para obter o sujeito
    subject_mask = ~true_bg

    # Limpeza morfológica: preencher buracos internos no sujeito
    subject_mask = ndimage.binary_fill_holes(subject_mask)
    # Suavização com fechamento morfológico leve
    struct = ndimage.generate_binary_structure(2, 2)
    subject_mask = ndimage.binary_closing(subject_mask, structure=struct, iterations=3)

    # Converter máscara booleana para float [0..255]
    alpha = np.where(subject_mask, 255.0, 0.0)

    # Fade out gradual na base da imagem (últimos 15% de altura) para efeito orgânico sumi-e
    fade_start = int(h * 0.82)
    for y in range(fade_start, h):
        factor = (h - y) / (h - fade_start)
        alpha[y, :] *= factor

    # Aplicar suavização gaussiana na máscara para bordas perfeitas e naturais
    alpha_img = Image.fromarray(alpha.astype(np.uint8), mode='L')
    alpha_blurred = alpha_img.filter(ImageFilter.GaussianBlur(radius=2.5))

    # Atribuir canal alfa ao PNG
    img.putalpha(alpha_blurred)

    # Aumentar contraste e tom cinematográfico do sujeito para casar com o estilo editorial da referência
    img.save(out_path, format='PNG')
    img.save(out_dist, format='PNG')
    print("Personagem recortado com sucesso salvo em:", out_path)

if __name__ == '__main__':
    process_character()
