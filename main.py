import requests
import xml.etree.ElementTree as ET

# Informações do usuário
nome_usuario = "Lourival26"

# Links e nomes dos arquivos
configuracoes = [
    {"url": "https://iptv-epg.org/files/epg-br.xml", "arquivo": "epg-brasil.xml"},
    {"url": "https://i.mjh.nz/PlutoTV/br.xml", "arquivo": "epg-pluto.xml"}
]

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"}

print(f"Olá, {nome_usuario}! Iniciando a criação de EPGs separados...")

for config in configuracoes:
    try:
        response = requests.get(config["url"], headers=headers, timeout=60)
        if response.status_code == 200:
            # Tenta modificar o XML para incluir a assinatura do Lourival26
            try:
                root = ET.fromstring(response.content)
                root.set("generator-info-name", f"Gerado por {nome_usuario}")
                conteudo_xml = ET.tostring(root, encoding="utf-8", xml_declaration=True)
            except Exception:
                # Se houver qualquer falha no formato, salva o conteúdo original puro
                conteudo_xml = response.content

            # Salva o arquivo atualizado
            with open(config["arquivo"], "wb") as f:
                f.write(conteudo_xml)
            print(f"Sucesso: {config['arquivo']} gerado com assinatura!")
        else:
            print(f"Erro ao baixar {config['url']}: Código {response.status_code}")
    except Exception as e:
        print(f"Erro ao processar {config['url']}: {e}")

print(f"Parabéns, {nome_usuario}! Ambos os arquivos foram atualizados.")
