import requests

# URLs das fontes
url_principal = "https://iptv-epg.org/files/epg-br.xml"
url_pluto = "https://raw.githubusercontent.com/matthuisman/i.mjh.nz/refs/heads/master/PlutoTV/cl.xml"

def baixar_epg():
    print("Baixando EPGs...")
    
    try:
        # Baixa o primeiro
        resp1 = requests.get(url_principal, timeout=30)
        # Baixa o segundo
        resp2 = requests.get(url_pluto, timeout=30)
        
        if resp1.status_code == 200 and resp2.status_code == 200:
            # Pega o conteúdo dos dois
            conteudo1 = resp1.text
            conteudo2 = resp2.text
            
            # Remove a tag de fechamento do primeiro e o cabeçalho do segundo
            # Isso "funde" os dois arquivos em um só XML válido
            conteudo_final = conteudo1.replace("</tv>", "") + "\n" + \
                             conteudo2.replace("<?xml version=\"1.0\" encoding=\"UTF-8\"?>", "").replace("<!DOCTYPE tv SYSTEM \"xmltv.dtd\">", "").replace("<tv>", "")
            
            with open("epg.xml", "w", encoding="utf-8") as f:
                f.write(conteudo_final)
                
            print("EPG fundido e atualizado com sucesso!")
        else:
            print(f"Erro ao baixar: Status {resp1.status_code} e {resp2.status_code}")
            
    except Exception as e:
        print(f"Erro ao conectar: {e}")

baixar_epg()
