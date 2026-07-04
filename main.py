import requests

# Script do Lourival26 - Unificador de EPG
# Lista das 4 fontes de EPG selecionadas
urls = [
    "https://iptv-epg.org/files/epg-br.xml",
    "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/PlutoTV/br.xml",
    "https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/globo.xml",
    "https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/claro.xml"
]

# Estrutura inicial do arquivo XML unificado
merged_data = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>'

print("Iniciando a atualização do EPG do Lourival26...")

for url in urls:
    try:
        print(f"Processando: {url}")
        response = requests.get(url)
        if response.status_code == 200:
            # Removemos cabeçalhos e tags de abertura/fechamento para unir os conteúdos
            data = response.text.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            data = data.replace('<!DOCTYPE tv SYSTEM "xmltv.dtd">', '')
            data = data.replace('<tv>', '').replace('</tv>', '')
            merged_data += data + "\n"
        else:
            print(f"Erro ao acessar {url}: Código {response.status_code}")
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

# Finaliza o arquivo XML com a tag de fechamento
merged_data += "</tv>"

# Salva o arquivo epg.xml final na raiz do repositório
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(merged_data)

print("EPG do Lourival26 unificado com sucesso!")
