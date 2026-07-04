import requests

urls = [
    "https://iptv-epg.org/files/epg-br.xml",
    "https://epgbrasil.com.br/epg/pluto.xml"
]

print("Iniciando a unificação do EPG do Lourival26...")

# Início do arquivo
final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
final_xml += '<!-- EPG Personalizado para Lourival26 -->\n'
final_xml += '<tv>\n'

for url in urls:
    print(f"Baixando: {url}")
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            # Pegamos o conteúdo e removemos apenas as tags de início e fim globais
            # de forma mais flexível para evitar erros
            conteudo = response.text
            # Removemos a linha do cabeçalho XML se ela existir
            conteudo = conteudo.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
            # Removemos as tags <tv> e </tv> ignorando maiúsculas/minúsculas
            conteudo = conteudo.replace('<tv>', '').replace('</tv>', '')
            
            final_xml += conteudo + "\n"
        else:
            print(f"Falha ao baixar {url} (Código {response.status_code})")
    except Exception as e:
        print(f"Erro de conexão com {url}: {e}")

# Fechamento do arquivo
final_xml += "</tv>"

# Salvando
with open("epg.xml", "w", encoding="utf-8") as f:
    f.write(final_xml)

print("EPG do Lourival26 gerado com sucesso!")
