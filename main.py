import xml.etree.ElementTree as ET
import requests

nome_usuario = "Lourival26"
url_br = "https://iptv-epg.org/files/epg-br.xml"
# Este link da Pluto TV traz todos os países/regiões do mundo inteiro de uma só vez
url_pluto_all = "https://i.mjh.nz/PlutoTV/all.xml"

print(f"Olá, {nome_usuario}! Iniciando o download e unificação dos EPGs...")

# --- 1. Baixando e processando o EPG do Brasil ---
try:
  response_br = requests.get(url_br, timeout=30)
  if response_br.status_code == 200:
    root_base = ET.fromstring(response_br.content)
    root_base.set("generator-info-name", f"{nome_usuario} - EPG Base Brasil")
    print("EPG do Brasil baixado com sucesso!")
  else:
    root_base = None
except Exception as e:
  print(f"Erro ao conectar ao EPG do Brasil: {e}")
  root_base = None

# --- 2. Baixando e processando o EPG Global da Pluto TV (Todos os países) ---
try:
  response_pluto_all = requests.get(url_pluto_all, timeout=45)
  if response_pluto_all.status_code == 200:
    root_pluto_all = ET.fromstring(response_pluto_all.content)
    print("EPG Global da Pluto TV (Todos os países) baixado com sucesso!")
  else:
    root_pluto_all = None
except Exception as e:
  print(f"Erro ao conectar ao EPG Global da Pluto TV: {e}")
  root_pluto_all = None

# --- 3. Unificando tudo em um único arquivo ---
if root_base is not None and root_pluto_all is not None:
  print("Unificando os EPGs...")
  root_base.set("generator-info-name", f"{nome_usuario} - EPG Completo Unificado")

  existing_channels = {ch.get("id"): ch for ch in root_base.findall("channel")}

  for channel in root_pluto_all.findall("channel"):
    ch_id = channel.get("id")
    if ch_id not in existing_channels:
      root_base.append(channel)
      existing_channels[ch_id] = channel

  for programme in root_pluto_all.findall("programme"):
    root_base.append(programme)

  arquivo_final = "epg.completo.xml"
  tree_final = ET.ElementTree(root_base)
  tree_final.write(arquivo_final, encoding="utf-8", xml_declaration=True)

  print(f"Sucesso! Arquivo '{arquivo_final}' gerado com o Brasil e a Pluto TV global.")
else:
  print("Erro na unificação, um dos arquivos falhou.")
