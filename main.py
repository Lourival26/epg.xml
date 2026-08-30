import gzip
import io
import xml.etree.ElementTree as ET
import requests

nome_usuario = "Lourival26"
url_br = "https://iptv-epg.org/files/epg-br.xml"
url_share = "https://epgshare01.online/epgshare01/epg_ripper_BR2.xml.gz"

print(f"Olá, {nome_usuario}! Iniciando o download e unificação (Brasil + EPG.share)...")

# --- 1. Baixando e processando o EPG do Brasil ---
try:
  response_br = requests.get(url_br, timeout=30)
  if response_br.status_code == 200:
    root_br = ET.fromstring(response_br.content)
    root_br.set("generator-info-name", f"{nome_usuario} - EPG Brasil Principal")
    print("EPG do Brasil baixado com sucesso!")
  else:
    root_br = None
except Exception as e:
  print(f"Erro ao conectar ao EPG do Brasil: {e}")
  root_br = None

# --- 2. Baixando e processando o EPG.share01 (.gz) ---
try:
  print("Baixando EPG.share01 (Brasil)...")
  response_share = requests.get(url_share, timeout=60)
  if response_share.status_code == 200:
    with gzip.open(io.BytesIO(response_share.content), "rb") as f_in:
      conteudo_xml = f_in.read()
    root_share = ET.fromstring(conteudo_xml)
    print("EPG.share01 baixado e descompactado com sucesso!")
  else:
    root_share = None
except Exception as e:
  print(f"Erro ao conectar ao EPG.share01: {e}")
  root_share = None

# --- 3. Unificando e salvando o completo ---
if root_br is not None:
  print("Unificando os EPGs...")
  root_br.set("generator-info-name", f"{nome_usuario} - EPG Unificado (BR + Share)")
  
  # Mapeia os canais que já existem para evitar duplicatas
  existing_channels = {ch.get('id'): ch for ch in root_br.findall('channel')}

  # Adiciona EPG.share01 se houver
  if root_share is not None:
    for channel in root_share.findall('channel'):
      ch_id = channel.get('id')
      if ch_id not in existing_channels:
        root_br.append(channel)
        existing_channels[ch_id] = channel
    for programme in root_share.findall('programme'):
      root_br.append(programme)
      
  arquivo_final = "epg.completo.xml"
  tree_final = ET.ElementTree(root_br)
  tree_final.write(arquivo_final, encoding="utf-8", xml_declaration=True)
  
  print(f"Sucesso! Arquivo '{arquivo_final}' gerado com Brasil + Share.")
else:
  print("Erro crítico: A base principal do Brasil falhou.")
