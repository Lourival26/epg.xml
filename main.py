import gzip
import urllib.request
import xml.etree.ElementTree as ET

# Ordem atualizada: iptv-epg.org primeiro, Pluto TV embaixo
URLS = [
    "https://iptv-epg.org/files/epg-br.xml",
    "https://i.mjh.nz/PlutoTV/br.xml.gz",
]

output_file = "epg.completo.xml"

print("Baixando e unificando os arquivos EPG de forma leve...")

root = ET.Element("tv")
elementos_adicionados = set()

for url in URLS:
  print(f"Processando: {url}")
  try:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as response:
      content = response.read()

      if url.endswith(".gz"):
        content = gzip.decompress(content)

      # Usando iterparse para economizar muita memória RAM
      from io import BytesIO

      for event, elem in ET.iterparse(BytesIO(content), events=("end",)):
        if elem.tag in ("channel", "programme"):
          # Evita duplicar canais ou programas repetidos se houver sobreposição
          elem_id = elem.get("id") or (
              elem.get("channel")
              + elem.get("start", "")
              + elem.get("stop", "")
          )

          if elem_id not in elementos_adicionados:
            elementos_adicionados.add(elem_id)
            root.append(elem)
          else:
            elem.clear()  # Descarta duplicados da memória
        elif elem.tag == "tv":
          elem.clear()

  except Exception as e:
    print(f"Erro ao processar {url}: {e}")

# Salva o XML otimizado
tree = ET.ElementTree(root)
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print(
    f"EPG leve gerado com sucesso por Escritor Lourival26 em"
    f" '{output_file}'!"
)
