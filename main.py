import xml.etree.ElementTree as ET
import requests
import gzip
import io

nome_usuario = "Lourival26"
url_br = "https://iptv-epg.org/files/epg-br.xml"
# Substituído pelo link do EPGShare01 (Brasil)
url_epgshare = "https://epgshare01.online/epgshare01/epg_ripper_BR1.xml.gz"

print(f"Olá, {nome_usuario}! Iniciando o download e unificação dos EPGs...")

# --- 1. Baixando e processando o EPG do Brasil ---
try:
  response_br = requests.get(url_br, timeout=30)
  if response_br.status_code == 200:
    root_br = ET.fromstring(response_br.content)
    root_br.set("generator-info-name", f"{nome_usuario} - EPG Brasil Separado")
    print("EPG do Brasil baixado com sucesso!")
  else:
    root_br = None
except Exception as e:
  print(f"Erro ao conectar ao EPG do Brasil: {e}")
  root_br = None

# --- 2. Baixando e processando o EPG do EPGShare01 ---
try:
  response_share = requests.get(url_epgshare, timeout=30)
  if response_share.status_code == 200:
    # Como o arquivo é .gz, descompactamos o conteúdo binário antes de ler com o ET
    with gzip.open(io.BytesIO(response_share.content), "rb") as f_in:
      xml_content = f_in.read()
    
    root_share = ET.fromstring(xml_content)
    root_share.set("generator-info-name", f"{nome_usuario} - EPG Share Separado")
    print("EPG do EPGShare01 baixado e descompactado com sucesso!")
  else:
    root_share = None
except Exception as e:
  print(f"Erro ao conectar ao EPG do EPGShare01: {e}")
  root_share = None

# --- 3. Unificando e salvando apenas o completo ---
if root_br is not None and root_share is not None:
  print("Unificando os EPGs...")
  root_br.set("generator-info-name", f"{nome_usuario} - EPG Completo Unificado")

  existing_channels = {ch.get("id"): ch for ch in root_br.findall("channel")}

  for channel in root_share.findall("channel"):
    ch_id = channel.get("id")
    if ch_id not in existing_channels:
      root_br.append(channel)
      existing_channels[ch_id] = channel

  for programme in root_share.findall("programme"):
    root_br.append(programme)

  arquivo_final = "epg.completo.xml"
  tree_final = ET.ElementTree(root_br)
  tree_final.write(arquivo_final, encoding="utf-8", xml_declaration=True)

  print(f"Sucesso! Arquivo '{arquivo_final}' gerado.")
else:
  print("Erro na unificação, um dos arquivos falhou.")
