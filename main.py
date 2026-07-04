import requests

# Lista com os links que você quer unificar
urls = [
    "https://iptv-epg.org/files/epg-br.xml",
    "https://epgbrasil.com.br/epg/pluto.xml"
]

print("Iniciando a unificação do EPG do Lourival26...")

# Adicionamos um comentário no topo do XML para identificar quem é o dono
final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
final_xml += '<!-- EPG Personalizado para Lourival26 -->\n'
final_xml += '<tv>\n'

for url in urls:
    print(f"Lourival26 - Baixando de: {url}")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Remove as tags de cabeçalho e fechamento para não quebrar o arquivo final
            conteudo = response.text
            conteudo = conteudo.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            conteudo = conteudo.replace('<!DOCTYPE tv SYSTEM "xmltv.dtd">', '')
            conteudo = conteudo.replace('<tv>', '').replace('</tv>', '')
            
            final_xml += conteudo + "\n"
        else:
            print(f"Lourival26 - Erro ao baixar {url}: Código {response.status_code}")
    except Exception as e:
        print(f"Lourival26 - Erro ao conectar com {url}: {e}")

# Fecha a tag principal
final_xml += "</tv>"

# Salva o resultado final no seu epg.xml
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(final_xml)

print("EPG do Lourival26 unificado com sucesso!")
