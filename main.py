import requests

# Link único e estável
url = "https://iptv-epg.org/files/epg-br.xml"

print("Baixando EPG oficial...")

try:
    response = requests.get(url, timeout=30)
    if response.status_code == 200:
        # Salva exatamente o que foi baixado no seu epg.xml
        with open("epg.xml", "w", encoding="utf-8") as f:
            f.write(response.text)
        print("EPG atualizado com sucesso!")
    else:
        print(f"Erro ao baixar: Código {response.status_code}")
except Exception as e:
    print(f"Erro ao conectar: {e}")
