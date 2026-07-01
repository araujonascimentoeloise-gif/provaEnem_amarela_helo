"""
Propósito: Remover a bordinha interna que fica entre as colunas
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025
Atualização: 03/06/2026

OBS1: puxe a pasta "divididas-com-bordas-do-meio" do passo 3 para essa pasta do passo 4
OBS2: As imagens da coluna da esquerda tem uma bordinha no lado direito
OBS3: As imagens da coluna da direita tem uma bordinha no lado esquerdo
OBS4: tive que contar pixels usando o GIMP para saber quanto pixels cortar de borda interna

"""
from PIL import Image
import os

pasta_imagens = "divididas-com-bordas-do-meio"
pasta_saida = "divididas-sem-bordas-do-meio"

os.makedirs(pasta_saida, exist_ok=True)

for nome_arquivo in os.listdir(pasta_imagens):
    if nome_arquivo.lower().endswith(".png"):
        caminho_entrada = os.path.join(pasta_imagens, nome_arquivo)
        imagem = Image.open(caminho_entrada)
        
        largura, altura = imagem.size
        
        # Aplica o corte original das bordas totais
        caixa_corte = (0, 0, largura, altura)
        
        # Aplica cortes adicionais baseados no nome do arquivo
        if nome_arquivo.endswith("_esquerda.png"):
            # Remove 10 pixels da borda direita
            caixa_corte = (caixa_corte[0], caixa_corte[1], 
                          caixa_corte[2] - 25, caixa_corte[3])
        
        elif nome_arquivo.endswith("_direita.png"):
            # Remove 10 pixels da borda esquerda
            caixa_corte = (caixa_corte[0] + 25, caixa_corte[1], 
                          caixa_corte[2], caixa_corte[3])
        
        imagem_cortada = imagem.crop(caixa_corte)
        
        caminho_saida = os.path.join(pasta_saida, nome_arquivo)
        imagem_cortada.save(caminho_saida)

print("Recorte das bordas concluído.")