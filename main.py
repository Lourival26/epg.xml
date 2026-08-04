import requests
import xml.etree.ElementTree as ET

# Informações do usuário
nome_usuario = "Lourival26"

# Links dos EPGs
url_br = "https://iptv-epg.org/files/epg-br.xml"
url_pluto = "https://i.mjh.nz/PlutoTV/all.xml"

print(f"Olá, {nome_usuario}! Baixando EPG oficial do Brasil...")
root_br = None
try:
    response_br = requests.get(url_br, timeout=30)
    if response_br.status_code == 200:
        root_br = ET.fromstring(response_br.content)
        print(f"{nome_usuario}, EPG do Brasil baixado com sucesso!")
    else:
        print(f"{nome_usuario}, erro ao baixar EPG do Brasil: Código {response_br.status_code}")
except Exception as e:
    print(f"{nome_usuario}, erro ao conectar ao EPG do Brasil: {e}")

print(f"Olá, {nome_usuario}! Baixando EPG da Pluto TV...")
root_pluto = None
try:
    response_pluto = requests.get(url_pluto, timeout=30)
    if response_pluto.status_code == 200:
        root_pluto = ET.fromstring(response_pluto.content)
        print(f"{nome_usuario}, EPG da Pluto TV baixado com sucesso!")
    else:
        print(f"{nome_usuario}, erro ao baixar EPG da Pluto TV: Código {response_pluto.status_code}")
except Exception as e:
    print(f"{nome_usuario}, erro ao conectar ao EPG da Pluto TV: {e}")

# Se pelo menos um dos dois foi baixado com sucesso, fazemos a mesclagem
if root_br is not None or root_pluto is not None:
    print(f"Atenção, {nome_usuario}! Mesclando os arquivos EPG...")
    
    base_root = root_br if root_br is not None else ET.Element("tv")
    base_root.set("generator-info-name", f"{nome_usuario} - Custom EPG")
    
    if root_pluto is not None:
        for child in root_pluto:
            if child.tag in ("channel", "programme"):
                base_root.append(child)
                
    try:
        tree = ET.ElementTree(base_root)
        tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
        print(f"Parabéns, {nome_usuario}! EPG atualizado com sucesso!")
    except Exception as e:
        print(f"{nome_usuario}, erro ao salvar o arquivo EPG: {e}")
else:
    print(f"{nome_usuario}, falha ao baixar ambos os EPGs. Nenhum arquivo foi alterado.")
