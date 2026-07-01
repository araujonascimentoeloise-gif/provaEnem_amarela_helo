import os

def renomear_questoes():
    pasta = r"mat_tec_136_a_180\161_a_180"

    primeira_questao = 161
    ultima_questao = 180

    if not os.path.exists(pasta):
        print("Pasta não encontrada!")
        return

    # Lista apenas os arquivos parte_XXX.png e ordena pelo número
    arquivos = sorted(
        [f for f in os.listdir(pasta) if f.startswith("parte_") and f.endswith(".png")],
        key=lambda x: int(x[6:9])
    )

    quantidade_esperada = ultima_questao - primeira_questao + 1

    if len(arquivos) != quantidade_esperada:
        print(f"Atenção! Esperava {quantidade_esperada} imagens, mas encontrei {len(arquivos)}.")

    numero_questao = primeira_questao

    for arquivo in arquivos:
        antigo = os.path.join(pasta, arquivo)
        novo = os.path.join(pasta, f"questao-{numero_questao}.png")

        os.rename(antigo, novo)
        print(f"{arquivo} -> questao-{numero_questao}.png")

        numero_questao += 1

    print("Renomeação concluída!")

if __name__ == "__main__":
    renomear_questoes()