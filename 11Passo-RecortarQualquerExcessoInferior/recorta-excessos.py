"""
Propósito: recortar excessos inferiores que possam ter ficado nas imagens, usando a faixa como referência
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "questoes" do passo anteriores para este passo 11
OBS2: atualize a linha 146 para o RGB 0a255 da cor da faixa do seu caderno, usando o GIMP para descobrir o RGB
OBS4: você precisa analisar o padrão de faixa inferior. Ás vezes, nem vai ter faixa inferior. 
ATUALIZE A LINHA 25 COM O PADRÃO DA SUA PROVA. Se precisar, use IA para analisar o padrão da faixa inferior
OBS5: se estiver muito difícil para recortar os excessos inferiores, você pode simplesmente fazer um recorte manualmente, usando o GIM
"""
from PIL import Image
import os
import shutil

def encontrar_faixa_inferior(imagem, cor_alvo, tolerancia=15):
    """
    Encontra a faixa descrita de baixo para cima
    Retorna a posição Y onde deve ser feito o corte (acima da faixa) ou None se não encontrar
    """
    largura, altura = imagem.size
    pixels = imagem.load()
    
    # Percorre a imagem de baixo para cima
    for y in range(altura - 1, 15, -1):  # Começa do fundo, precisa de pelo menos 12 pixels
        # Verifica o padrão da faixa: 4px azul, 4px branco, 4px azul
        faixa_encontrada = True
        
        # Verifica os 4 pixels azuis inferiores (y-11 até y-8)
        for dy in range(5):
            pixel_y = y - 14 + dy
            if pixel_y < 0:
                faixa_encontrada = False
                break
                
            pixel = pixels[largura // 2, pixel_y]
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é azul (dentro da tolerância)
            if (abs(r - cor_alvo[0]) > tolerancia or 
                abs(g - cor_alvo[1]) > tolerancia or 
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break
        
        if not faixa_encontrada:
            continue
            
        # Verifica os 4 pixels brancos do meio (y-7 até y-4)
        for dy in range(5):
            pixel_y = y - 9 + dy
            pixel = pixels[largura // 2, pixel_y]
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é branco (dentro da tolerância)
            if (abs(r - 255) > tolerancia or 
                abs(g - 255) > tolerancia or 
                abs(b - 255) > tolerancia):
                faixa_encontrada = False
                break
        
        if not faixa_encontrada:
            continue
            
        # Verifica os 4 pixels azuis superiores (y-3 até y)
        for dy in range(5):
            pixel_y = y - 4 + dy
            pixel = pixels[largura // 2, pixel_y]
            if len(pixel) == 4:  # RGBA
                r, g, b, a = pixel
            else:  # RGB
                r, g, b = pixel[:3]
            
            # Verifica se é azul (dentro da tolerância)
            if (abs(r - cor_alvo[0]) > tolerancia or 
                abs(g - cor_alvo[1]) > tolerancia or 
                abs(b - cor_alvo[2]) > tolerancia):
                faixa_encontrada = False
                break
        
        if faixa_encontrada:
            print(f"Faixa encontrada! Cortando na posição y={y-43}")
            return y - 43  # Retorna a posição acima da faixa completa
    
    return None

def processar_imagens(pasta_origem, pasta_destino, cor_alvo):
    """
    Processa todas as imagens da pasta origem, recortando as que têm faixa azul inferior
    e copiando todas para a pasta destino
    """
    # Cria a pasta de destino se não existir
    os.makedirs(pasta_destino, exist_ok=True)
    
    # Lista todos os arquivos da pasta origem
    arquivos = [f for f in os.listdir(pasta_origem) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
    
    print(f"Encontrados {len(arquivos)} arquivos para processar")
    
    for arquivo in arquivos:
        caminho_origem = os.path.join(pasta_origem, arquivo)
        caminho_destino = os.path.join(pasta_destino, arquivo)
        
        try:
            # Abre a imagem
            with Image.open(caminho_origem) as imagem:
                print(f"\nProcessando: {arquivo} ({imagem.width}x{imagem.height})")
                
                # Procura pela faixa inferior
                posicao_corte = encontrar_faixa_inferior(imagem, cor_alvo)
                
                if posicao_corte is not None and posicao_corte > 0:
                    # Se encontrou a faixa, recorta a imagem
                    area_corte = (0, 0, imagem.width, posicao_corte)
                    imagem_recortada = imagem.crop(area_corte)
                    imagem_recortada.save(caminho_destino)
                    print(f"✓ Imagem recortada: {imagem_recortada.width}x{imagem_recortada.height}")
                else:
                    # Se não encontrou faixa, copia a imagem original
                    shutil.copy2(caminho_origem, caminho_destino)
                    print(f"✓ Imagem mantida original (sem faixa detectada)")
                    
        except Exception as e:
            print(f"✗ Erro ao processar {arquivo}: {e}")
            # Tenta copiar o arquivo mesmo com erro
            try:
                shutil.copy2(caminho_origem, caminho_destino)
                print(f"✓ Arquivo copiado mesmo com erro")
            except:
                print(f"✗ Não foi possível copiar o arquivo")

# Função principal
if __name__ == "__main__":
    # Configurações
    pasta_origem = "./questoes"
    pasta_destino = "finalizadas"
    cor_alvo = (255, 252, 191)  # RGB 0a255 da cor da faixa do caderno (atualize com o RGB correto usando o GIMP)
    
    print("Iniciando processamento de imagens...")
    print(f"Pasta origem: {pasta_origem}")
    print(f"Pasta destino: {pasta_destino}")
    print(f"Cor alvo: RGB{cor_alvo}")
    
    # Verifica se a pasta origem existe
    if not os.path.exists(pasta_origem):
        print(f"Erro: A pasta '{pasta_origem}' não existe!")
        exit(1)
    
    # Executa o processamento
    processar_imagens(pasta_origem, pasta_destino, cor_alvo)
    
    print("\n" + "="*50)
    print("Processamento concluído!")
    print(f"Todas as imagens foram salvas em: {pasta_destino}")