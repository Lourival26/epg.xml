import urllib.request
import xml.etree.ElementTree as ET

# Link de uma fonte confiável de programação (exemplo de uma grade geral)
URL_PROGRAMACAO_EXTERNA = "https://raw.githubusercontent.com/diego-vidal/epg-brasil/main/epg.xml"
ARQUIVO_MAPEAMENTO = "epg-brasil.xml"

def atualizar_epg():
    # 1. Carrega seu arquivo base (canais)
    tree_base = ET.parse(ARQUIVO_MAPEAMENTO)
    root_base = tree_base.getroot()
    
    # 2. Baixa a programação externa
    print("Baixando grade de programação...")
    req = urllib.request.Request(URL_PROGRAMACAO_EXTERNA, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        xml_data = response.read()
        root_externo = ET.fromstring(xml_data)

    # 3. Cria uma nova estrutura para o EPG final
    root_final = ET.Element("tv", {"generator-info-name": "Lourival26"})
    
    # Adiciona seus canais
    for channel in root_base.findall("channel"):
        root_final.append(channel)
        
    # Adiciona a programação da fonte externa
    for programme in root_externo.findall("programme"):
        root_final.append(programme)

    # 4. Salva o arquivo final
    tree_final = ET.ElementTree(root_final)
    tree_final.write("epg-completo.xml", encoding="utf-8", xml_declaration=True)
    print("epg-completo.xml gerado com sucesso!")

if __name__ == "__main__":
    atualizar_epg()
