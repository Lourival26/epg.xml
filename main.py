import requests
import xml.etree.ElementTree as ET

# Lista de links de EPG (apenas o segundo link)
urls = [
    "http://epgpainel.ddns.net/epg.xml"
]

# Cria o elemento raiz do novo arquivo XML
root = ET.Element("tv")
root.set("generator-info-name", "MeuEPGCombinado")

for url in urls:
    try:
        print(f"Processando: {url}")
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Faz o parse do conteúdo baixado
            temp_root = ET.fromstring(response.content)
            # Adiciona todos os canais e programas encontrados ao root principal
            for child in temp_root:
                root.append(child)
        else:
            print(f"Erro ao acessar {url}: Status {response.status_code}")
    except Exception as e:
        print(f"Erro ao conectar em {url}: {e}")

# Salva o arquivo final com a declaração XML correta
tree = ET.ElementTree(root)
tree.write("epg.xml", encoding="UTF-8", xml_declaration=True)

print("EPG salvo como epg.xml!")
