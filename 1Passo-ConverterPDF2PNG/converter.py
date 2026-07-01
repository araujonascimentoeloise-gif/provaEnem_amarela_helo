"""
Propósito: converter o arquivo PDF em imagens PNG
Autor: Alexandre Nassar de Peder
Criação: 02/10/2025.
Atualização: 03/06/2026

OBS1: coloque o arquivo PDF na mesma pasta deste script
OBS2: na linha 16, especifique o nome do arquivo PDF que deseja converter.
OBS3: depois de executar, tem que excluir as imagens com nome de código estranho da pasta de saída, deixando só os nomes que fazem sentido
OBS4: exclua as páginas 1 (capa), 19 (proposta de redação) e 32 (rascunho da redação)
"""

from pdf2image import convert_from_path
import os

arquivo = "2024_PV_reaplicacao_PPL_D2_CD5.pdf"
pasta_saida = "imagens-convertidas"

if not os.path.exists(pasta_saida):
    os.makedirs(pasta_saida)

resolucao_dpi = 300

print (f"Convertendo '{arquivo}' para imagens com {resolucao_dpi} DPI...")

try:
    images = convert_from_path(
        arquivo,
        dpi = resolucao_dpi,
        output_folder = pasta_saida,
        fmt = "png",
        paths_only = False,
    )

    for i, image in enumerate(images):
        image_filename = os.path.join(pasta_saida, f"pagina_enem_{i+1}.png")
        image.save(image_filename)
        print(f"Página {i+1} salva como '{image_filename}'")

    print(f"\nConversão concluída! As imagens foram salvas na pasta '{pasta_saida}'.")

except Exception as e:
    print (f"Ocorreu um erro durante a conversão: {e}")
    print("Verifique se o Poppler está instalado corretamente, se o caminho do PDF está correto ou se o PDF não está corrompido.")