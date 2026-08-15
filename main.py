import xml.etree.ElementTree as ET
import requests

nome_usuario = "Lourival26"
url_br = "https://iptv-epg.org/files/epg-br.xml"
url_pluto = "https://i.mjh.nz/PlutoTV/all.xml"

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

# --- 2. Baixando e processando o EPG da Pluto TV ---
try:
  response_pluto = requests.get(url_pluto, timeout=30)
  if response_pluto.status_code == 200:
    root_pluto = ET.fromstring(response_pluto.content)
    root_pluto.set("generator-info-name", f"{nome_usuario} - EPG Pluto Separado")
    print("EPG da Pluto TV baixado com sucesso!")
  else:
    root_pluto = None
except Exception as e:
  print(f"Erro ao conectar ao EPG da Pluto TV: {e}")
  root_pluto = None

# --- 3. Unificando e salvando apenas o completo ---
if root_br is not None and root_pluto is not None:
  print("Unificando os EPGs...")
  root_br.set("generator-info-name", f"{nome_usuario} - EPG Completo Unificado")
  
  existing_channels = {ch.get('id'): ch for ch in root_br.findall('channel')}
  
  for channel in root_pluto.findall('channel'):
    ch_id = channel.get('id')
    if ch_id not in existing_channels:
      root_br.append(channel)
      existing_channels[ch_id] = channel
      
  for programme in root_pluto.findall('programme'):
    root_br.append(programme)
    
  arquivo_final = "epg.completo.xml"
  tree_final = ET.ElementTree(root_br)
  tree_final.write(arquivo_final, encoding="utf-8", xml_declaration=True)
  
  print(f"Sucesso! Arquivo '{arquivo_final}' gerado.")
else:
  print("Erro na unificação, um dos arquivos falhou.")
