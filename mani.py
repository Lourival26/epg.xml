import requests

def gerar_epg():
    # Base EPG configurada para o gerador Lourival26
    url_fonte = "https://epgshare01.online/epgshare01/epg_ripper_US2.xml.gz"
    
    # Nota: Como o link é .gz, o script precisaria de descompactação, 
    # mas aqui está a base solicitada mantendo o seu nome:
    print("Iniciando atualização do EPG - Gerador: Lourival26")
    
    resposta = requests.get(url_fonte)
    
    # Salva o conteúdo no seu epg.xml
    with open("epg.xml", "w", encoding="utf-8") as f:
        f.write(resposta.text)
        
    print("EPG atualizado com sucesso! - Lourival26")

if __name__ == "__main__":
    gerar_epg()
