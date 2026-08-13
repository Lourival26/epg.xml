import xml.etree.ElementTree as ET
import requests

# Informações do usuário
nome_usuario = "Lourival26"

# Links dos EPGs
url_br = "https://iptv-epg.org/files/epg-br.xml"
url_pluto = "https://i.mjh.nz/PlutoTV/all.xml"

print(f"Olá, {nome_usuario}! Iniciando o download e unificação dos EPGs...")

# --- 1. Baixando e processando o EPG do Brasil ---
try:
  print(f"Baixando EPG oficial do Brasil...")
  response_br = requests.get(url_br, timeout=30)
  if response_br.status_code == 200:
    root_br = ET.fromstring(response_br.content)
    root_br.set("generator-info-name", f"{nome_usuario} - EPG Brasil Separado")
    
    tree_br = ET.ElementTree(root_br)
    tree_br.write("epg.br.xml", encoding="utf-8", xml_declaration=True)
    print(f"EPG do Brasil salvo como 'epg.br.xml'!")
  else:
    print(f"Erro ao baixar EPG do Brasil: Código {response_br.status_code}")
    root_br = None
except Exception as e:
  print(f"Erro ao conectar ao EPG do Brasil: {e}")
  root_br = None

# --- 2. Baixando e processando o EPG da Pluto TV ---
try:
  print(f"Baixando EPG da Pluto TV...")
  response_pluto = requests.get(url_pluto, timeout=30)
  if response_pluto.status_code == 200:
    root_pluto = ET.fromstring(response_pluto.content)
    root_pluto.set("generator-info-name", f"{nome_usuario} - EPG Pluto Separado")
    
    tree_pluto = ET.ElementTree(root_pluto)
    tree_pluto.write("epg.pluto.xml", encoding="utf-8", xml_declaration=True)
    print(f"EPG da Pluto TV salvo como 'epg.pluto.xml'!")
  else:
    print(f"Erro ao baixar EPG da Pluto TV: Código {response_pluto.status_code}")
    root_pluto = None
except Exception as e:
  print(f"Erro ao conectar ao EPG da Pluto TV: {e}")
  root_pluto = None

# --- 3. Unificando os EPGs em um arquivo único ---
if root_br is not None and root_pluto is not None:
  print(f"Unificando os EPGs em um arquivo completo...")
  
  # Atualiza o nome do gerador do arquivo final unificado
  root_br.set("generator-info-name", f"{nome_usuario} - EPG Completo Unificado")
  
  # Mapeia os IDs dos canais já existentes no EPG do Brasil para evitar duplicatas
  existing_channels = {ch.get('id'): ch for ch in root_br.findall('channel')}
  
  # Adiciona os canais do EPG da Pluto TV que não existirem no do Brasil
  for channel in root_pluto.findall('channel'):
    ch_id = channel.get('id')
    if ch_id not in existing_channels:
      root_br.append(channel)
      existing_channels[ch_id] = channel
      
  # Adiciona todos os programas do EPG da Pluto TV ao arquivo unificado
  for programme in root_pluto.findall('programme'):
    root_br.append(programme)
    
  # Salva o arquivo final combinado
  arquivo_final = "epg_completo.xml"
  tree_final = ET.ElementTree(root_br)
  tree_final.write(arquivo_final, encoding="utf-8", xml_declaration=True)
  
  print(f"Parabéns, {nome_usuario}! EPG completo unificado salvo com sucesso como '{arquivo_final}'!")
else:
  print(f"{nome_usuario}, não foi possível realizar a unificação porque um dos arquivos falhou ao baixar.")
