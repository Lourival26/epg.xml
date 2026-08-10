import xml.etree.ElementTree as ET
import requests

# Informações do usuário
nome_usuario = "Lourival26"

# Links dos EPGs
url_br = "https://iptv-epg.org/files/epg-br.xml"
url_pluto = "https://i.mjh.nz/PlutoTV/all.xml"

# --- Baixando e salvando o EPG do Brasil ---
print(f"Olá, {nome_usuario}! Baixando EPG oficial do Brasil...")
try:
  response_br = requests.get(url_br, timeout=30)
  if response_br.status_code == 200:
    root_br = ET.fromstring(response_br.content)

    # Atualiza a info do gerador opcionalmente
    root_br.set(
        "generator-info-name", f"{nome_usuario} - EPG Brasil Separado"
    )

    tree_br = ET.ElementTree(root_br)
    tree_br.write("epg.br.xml", encoding="utf-8", xml_declaration=True)
    print(f"Parabéns, {nome_usuario}! EPG do Brasil salvo como 'epg.br.xml'!")
  else:
    print(
        f"{nome_usuario}, erro ao baixar EPG do Brasil: Código"
        f" {response_br.status_code}"
    )
except Exception as e:
  print(f"{nome_usuario}, erro ao conectar ao EPG do Brasil: {e}")


# --- Baixando e salvando o EPG da Pluto TV ---
print(f"Olá, {nome_usuario}! Baixando EPG da Pluto TV...")
try:
  response_pluto = requests.get(url_pluto, timeout=30)
  if response_pluto.status_code == 200:
    root_pluto = ET.fromstring(response_pluto.content)

    # Atualiza a info do gerador opcionalmente
    root_pluto.set(
        "generator-info-name", f"{nome_usuario} - EPG Pluto Separado"
    )

    tree_pluto = ET.ElementTree(root_pluto)
    tree_pluto.write("epg.pluto.xml", encoding="utf-8", xml_declaration=True)
    print(
        f"Parabéns, {nome_usuario}! EPG da Pluto TV salvo como 'epg.pluto.xml'!"
    )
  else:
    print(
        f"{nome_usuario}, erro ao baixar EPG da Pluto TV: Código"
        f" {response_pluto.status_code}"
    )
except Exception as e:
  print(f"{nome_usuario}, erro ao conectar ao EPG da Pluto TV: {e}")
