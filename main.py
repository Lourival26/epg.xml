import gzip
import urllib.request
import xml.etree.ElementTree as ET

# URLs das fontes confiáveis (Brasil + Pluto TV Oficial)
URLS = [
    "https://iptv-epg.org/files/epg-br.xml",
    "https://i.mjh.nz/PlutoTV/br.xml.gz",
]

output_file = "epg.completo.xml"

print("Baixando e unificando os arquivos EPG...")

root = ET.Element("tv")

for url in URLS:
  print(f"Processando: {url}")
  try:
    req = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}
    )  # Evita bloqueios de requisição
    with urllib.request.urlopen(req) as response:
      content = response.read()

      # Se o arquivo for compactado (.gz), descompacta
      if url.endswith(".gz"):
        content = gzip.decompress(content)

      # Parse do XML baixado
      temp_root = ET.fromstring(content)

      # Adiciona os canais e programas na raiz principal
      for child in temp_root:
        root.append(child)

  except Exception as e:
    print(f"Erro ao processar {url}: {e}")

# Salva o XML unificado final
tree = ET.ElementTree(root)

# Abre o arquivo para escrita manual para injetar a assinatura do Lourival26 no topo
with open(output_file, "wb") as f:
  f.write(
      b'<!-- EPG Completo - Gerado e mantido por Lourival26 via GitHub'
      b" Actions -->\n"
  )
  tree.write(f, encoding="utf-8", xml_declaration=True)

print(f"EPG unificado gerado com sucesso por Lourival26 em '{output_file}'!")
