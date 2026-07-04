import requests

urls = [
    "https://iptv-epg.org/files/epg-br.xml",
    "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/PlutoTV/br.xml",
    "https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/globo.xml",
    "https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/claro.xml"
]

# Início do arquivo
final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>'

for url in urls:
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            content = response.text
            # Remove o cabeçalho e as tags de abertura/fechamento
            content = content.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            content = content.replace('<!DOCTYPE tv SYSTEM "xmltv.dtd">', '')
            content = content.replace('<tv>', '').replace('</tv>', '')
            final_xml += content
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")

final_xml += "</tv>"

# Salva o arquivo
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(final_xml)
