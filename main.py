import requests
import xml.etree.ElementTree as ET

urls = [
    "https://iptv-epg.org/files/epg-br.xml",
    "http://epgpainel.ddns.net/epg.xml"
]

# Cria o elemento raiz
root = ET.Element("tv")
root.set("generator-info-name", "MeuEPGCombinado")

for url in urls:
    try:
        print(f"Processando: {url}")
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Força o uso do conteúdo como texto para evitar erros de bytes
            temp_root = ET.fromstring(response.content)
            # Adiciona os elementos (canais e programas) ao root
            for child in temp_root:
                root.append(child)
    except Exception as e:
        print(f"Erro no link {url}: {e}")

# Salva de forma mais limpa
tree = ET.ElementTree(root)
# Usamos short_empty_elements=False para manter a compatibilidade com players antigos
tree.write("epg.xml", encoding="UTF-8", xml_declaration=True)
print("EPG combinado com sucesso e salvo como epg.xml!")
