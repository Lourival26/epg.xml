import requests

# Vamos focar nestas duas fontes principais que são as mais estáveis
urls = [
    "https://iptv-epg.org/files/epg-br.xml",
    "https://raw.githubusercontent.com/limaalef/BrazilTVEPG/refs/heads/main/globo.xml"
]

final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n<tv>\n'

for url in urls:
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Remove apenas o necessário
            data = response.text.replace('<?xml version="1.0" encoding="UTF-8"?>', '').replace('<tv>', '').replace('</tv>', '')
            final_xml += data + "\n"
    except Exception as e:
        print(f"Erro: {e}")

final_xml += "</tv>"

with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(final_xml)
