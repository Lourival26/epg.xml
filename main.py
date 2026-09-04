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
    )
    with urllib.request.urlopen(req) as response:
      content = response.read()

      if url.endswith(".gz"):
        content = gzip.decompress(content)

      temp_root = ET.fromstring(content)

      for child in temp_root:
        root.append(child)

  except Exception as e:
    print(f"Erro ao processar {url}: {e}")

# Salva o XML unificado limpo, exatamente como o aplicativo IPTV espera
tree = ET.ElementTree(root)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"EPG unificado gerado com sucesso por Lourival26 em '{output_file}'!")
