import urllib.request
import xml.etree.ElementTree as ET

# Seus links oficiais apontando para o seu repositório Lourival26/epg.xml
urls = [
    "https://raw.githubusercontent.com/Lourival26/epg.xml/refs/heads/main/epg-pluto.xml",
    "https://raw.githubusercontent.com/Lourival26/epg.xml/refs/heads/main/epg-brasil.xml"
]

root_element = None
all_channels = []
all_programmes = []

for url in urls:
    try:
        print(f"Baixando: {url}")
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_content = response.read()
            
            # Faz o parse do XML
            root = ET.fromstring(xml_content)
            
            if root_element is None:
                root_element = root
                
            # Coleta todos os canais e programações de dentro do arquivo
            for channel in root.findall('channel'):
                all_channels.append(channel)
            for programme in root.findall('programme'):
                all_programmes.append(programme)
    except Exception as e:
        print(f"Erro ao processar {url}: {e}")

if root_element is not None:
    # Remove os elementos antigos para evitar duplicatas ao reescrever
    for channel in root_element.findall('channel'):
        root_element.remove(channel)
    for programme in root_element.findall('programme'):
        root_element.remove(programme)
        
    # Adiciona todos os canais e programações unidos
    for channel in all_channels:
        root_element.append(channel)
    for programme in all_programmes:
        root_element.append(programme)
        
    # Salva o arquivo unificado
    tree = ET.ElementTree(root_element)
    tree.write("epg-completo.xml", encoding="utf-8", xml_declaration=True)
    print("Arquivo epg-completo.xml gerado com sucesso!")
else:
    print("Nenhum dado foi baixado.")
