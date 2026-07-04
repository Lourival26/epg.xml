import requests
import gzip
import io

# Lista com todas as fontes que você selecionou
urls = [
    "https://iptv-epg.org/files/epg-br.xml",
    "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/PlutoTV/br.xml.gz",
    "https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/globo.xml",
    "https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/claro.xml"
]

def get_content(url):
    try:
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            # Verifica se o arquivo é comprimido (Gzip) pelo final da URL
            if url.endswith('.gz'):
                with gzip.GzipFile(fileobj=io.BytesIO(response.content)) as f:
                    return f.read().decode('utf-8')
            return response.text
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
    return ""

# Início do arquivo XML unificado
final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>'

print("Iniciando a unificação do EPG do Lourival26...")

for url in urls:
    print(f"Processando: {url}")
    content = get_content(url)
    if content:
        # Remove cabeçalhos e tags que poderiam corromper o arquivo final
        content = content.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        content = content.replace('<!DOCTYPE tv SYSTEM "xmltv.dtd">', '')
        content = content.replace('<tv>', '').replace('</tv>', '')
        final_xml += content + "\n"

# Finaliza o arquivo XML
final_xml += "</tv>"

# Salva o resultado no seu epg.xml
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(final_xml)

print("EPG do Lourival26 unificado com sucesso!")
