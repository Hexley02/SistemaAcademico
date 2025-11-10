import json

with open("teste.json", "r", encoding="utf-8") as arquivos:
    dados = json.load(arquivos)
    for item in dados:
        print(item)
    


