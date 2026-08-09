import requests
import xml.etree.ElementTree as ET

# Informações do usuário
nome_usuario = "Lourival26"

# Links dos EPGs (Mudança: Pluto TV agora focada no Brasil)
url_br = "https://iptv-epg.org/files/epg-br.xml"
url_pluto = "https://i.mjh.nz/PlutoTV/br.xml" 

# Cabeçalho para fingir que somos um navegador (evita bloqueios)
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

print(f"Olá, {nome_usuario}! Iniciando atualização...")

def baixar_xml(url):
    try:
        response = requests.get(url, headers=headers, timeout=60)
        if response.status_code == 200:
            return ET.fromstring(response.content)
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
    return None

root_br = baixar_xml(url_br)
root_pluto = baixar_xml(url_pluto)

if root_br is not None or root_pluto is not None:
    # Cria a base do XML
    base_root = root_br if root_br is not None else ET.Element("tv")
    
    # Se baixou a Pluto, adiciona os canais e a grade
    if root_pluto is not None:
        for child in root_pluto:
            # Adiciona apenas canais e programas, ignorando o cabeçalho duplicado
            if child.tag in ("channel", "programme"):
                base_root.append(child)
                
    # Salva o arquivo final
    try:
        tree = ET.ElementTree(base_root)
        tree.write("epg.xml", encoding="utf-8", xml_declaration=True)
        print(f"Parabéns, {nome_usuario}! EPG atualizado e pronto para uso!")
    except Exception as e:
        print(f"Erro ao salvar: {e}")
else:
    print("Falha total na conexão. Tente novamente mais tarde.")
