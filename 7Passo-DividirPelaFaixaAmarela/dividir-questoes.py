from PIL import Image
import os

def converter_cor_gimp_para_rgb(gimp_r, gimp_g, gimp_b):
    """
    Converte valores do GIMP (0-100) para RGB (0-255)
    """
    r = int((gimp_r / 100) * 255)
    g = int((gimp_g / 100) * 255)
    b = int((gimp_b / 100) * 255)
    return (r, g, b)


def encontrar_faixa_amarela(imagem, cor_alvo=(255, 252, 191), tolerancia=30, altura_faixa=5):
    """
    Encontra posições onde há uma faixa horizontal da cor especificada
    """

    largura, altura = imagem.size
    pixels = imagem.load()

    posicoes_corte = []

    y = 0
    while y < altura - altura_faixa:

        faixa_encontrada = True

        for dy in range(altura_faixa):

            # Verifica o penúltimo pixel da direita
            pixel = pixels[largura - 2, y + dy]

            if len(pixel) == 4:
                r, g, b, a = pixel
            else:
                r, g, b = pixel[:3]

            if (
                abs(r - cor_alvo[0]) > tolerancia or
                abs(g - cor_alvo[1]) > tolerancia or
                abs(b - cor_alvo[2]) > tolerancia
            ):
                faixa_encontrada = False
                break

        if faixa_encontrada:

            posicao_corte = y - 42

            if posicao_corte < 0:
                posicao_corte = 0

            posicoes_corte.append(posicao_corte)

            print(f"Faixa amarela encontrada em y={y}, cortando em y={posicao_corte}")

            y += altura_faixa

        else:
            y += 1

    return posicoes_corte


def dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_alvo=(255, 252, 191)):
    """
    Divide a imagem verticalmente cortando ANTES das faixas amarelas
    """

    imagem = Image.open(caminho_imagem)

    largura, altura = imagem.size

    print(f"Imagem carregada: {largura}x{altura} pixels")

    posicoes_corte = encontrar_faixa_amarela(imagem, cor_alvo)

    if not posicoes_corte:
        print("Nenhuma faixa amarela encontrada!")
        return

    print(f"Encontradas {len(posicoes_corte)} faixas amarelas.")

    os.makedirs(pasta_saida, exist_ok=True)

    posicao_anterior = 0

    for i, posicao_corte in enumerate(posicoes_corte):

        if posicao_corte <= posicao_anterior:
            continue

        area_corte = (0, posicao_anterior, largura, posicao_corte)

        secao = imagem.crop(area_corte)

        nome_arquivo = f"parte_{i+1:03d}.png"

        caminho_completo = os.path.join(pasta_saida, nome_arquivo)

        secao.save(caminho_completo)

        print(f"Salvo: {nome_arquivo}")

        posicao_anterior = posicao_corte + 5

    if posicao_anterior < altura:

        area_corte = (0, posicao_anterior, largura, altura)

        secao = imagem.crop(area_corte)

        nome_arquivo = f"parte_{len(posicoes_corte)+1:03d}.png"

        caminho_completo = os.path.join(pasta_saida, nome_arquivo)

        secao.save(caminho_completo)

        print(f"Salvo: {nome_arquivo}")


if __name__ == "__main__":

    # ============================
    # ESCOLHA APENAS UMA IMAGEM
    # ============================

    caminho_imagem = "colunas_concatenadas_verticalmente.png"
    # caminho_imagem = "./inteiras/pagina_enem_15.png"
    # caminho_imagem = "./inteiras/pagina_enem_28.png"

    pasta_saida = "questoes_colunas"
    # pasta_saida = "pagina_15"
    # pasta_saida = "pagina_28"

    # Cor da faixa amarela (#FFFCBF)
    cor_amarela = (255, 252, 191)

    print(f"Cor utilizada: RGB{cor_amarela}")

    dividir_imagem_por_faixas(caminho_imagem, pasta_saida, cor_amarela)

    print("Divisão concluída!")