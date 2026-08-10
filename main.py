import xml.etree.ElementTree as ET

# Arquivo com seu mapeamento fixo de canais
arquivo_mapeamento = "epg-brasil.xml"

try:
    # 1. Carrega o arquivo XML existente
    tree = ET.parse(arquivo_mapeamento)
    root = tree.getroot()
    
    # Define o nome do gerador
    root.set("generator-info-name", "Lourival26")

    # 2. Exemplo de como adicionar um programa (o que está passando agora)
    # Você pode duplicar essa parte para cada canal e programa desejado
    # Formato da data/hora: YYYYMMDDHHMMSS +0000
    novo_programa = ET.Element("programme")
    novo_programa.set("start", "20260704120000 -0300")  # Horário de início
    novo_programa.set("stop", "20260704130000 -0300")   # Horário de término
    novo_programa.set("channel", "GloboRJ.br")           # ID do canal correspondente
    
    # Título do programa (o que está passando)
    title = ET.SubElement(novo_programa, "title")
    title.set("lang", "pt")
    title.text = "Exemplo: Jornal da TV"
    
    # Descrição opcional
    desc = ET.SubElement(novo_programa, "desc")
    desc.set("lang", "pt")
    desc.text = "Resumo do que está passando neste horário."

    # Adiciona o programa na estrutura do XML
    root.append(novo_programa)

    # 3. Salva o arquivo atualizado
    tree.write("epg-brasil.xml", encoding="utf-8", xml_declaration=True)
    print("Programação e horários atualizados com sucesso!")

except Exception as e:
    print(f"Erro ao processar o arquivo: {e}")
