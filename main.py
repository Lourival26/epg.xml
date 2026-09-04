import gzip
import urllib.request
import xml.etree.ElementTree as ET

# URLs das fontes confiáveis (Brasil Geral + Pluto TV Oficial via iptv-org)
URLS = [
    "https://iptv-epg.org/files/epg-br.xml",
    "https://iptv-org.github.io/epg/guides/br/plutotv.com.br.epg.xml",
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

      # Se por acaso alguma fonte futura usar .gz, mantém a segurança
      if url.endswith(".gz"):
        content = gzip.decompress(content)

      temp_root = ET.fromstring(content)

      for child in temp_root:
        root.append(child)

  except Exception as e:
    print(f"Erro ao processar {url}: {e}")

# Salva o XML unificado limpo para o aplicativo IPTV
tree = ET.ElementTree(root)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(f"EPG unificado gerado com sucesso por Lourival26 em '{output_file}'!")
