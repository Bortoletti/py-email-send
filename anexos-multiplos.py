import os
import re
from datetime import datetime
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import random


def getTimestampFmt2():
   now = datetime.now()
   return now.strftime("%Y-%m-%d-%H:%M")

class Destino:
    def __init__(self, nome, email ):
        self.nome = nome
        self.email = email

    def __str__(self):
        return f"Destino(nome={self.nome}, email={self.email})"


def sendEmail( fileParam, destinoParam, toAddressParam ):
    from_address    = "juridico.ia.gruposouzalima@gmail.com"
    to_address = toAddressParam 

    #to_address      = 'flavia.coelho@gruposouzalima.com'
    #to_address      = 'brenno.cardoso@gruposouzalima.com' 

    #cc_address      = []
    #cc_address.append( 'brenno.cardoso@gruposouzalima.com' )
    #cc_address.append( 'luis.bortoletti@gruposouzalima.com' )
    #cc_address.append( 'neusa.sotana@gruposouzalima.com' )
    #cc_address.append( 'mariana.gallo@gruposouzalima.com' )

    # Configurar a mensagem
    subject = f"Publicação - {destinoParam.nome} - {getTimestampFmt2()}-{random.randint(1, 10)}  "


    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    #msg['Cc'] = ', '.join(cc_address)  # Adicionando os endereços de Cc
    msg['Subject'] = subject

    # Anexando a imagem
    with open('img/logo-souzalima.JPG', 'rb') as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header('Content-ID', '<logo>')
        msg.attach(mime_image)

    html = f"""
    <html>
    <body>
        <img src="cid:logo">
        <p>Olá, {destinoParam.nome}
        <br>Teste de mensagens
        </p>
    </body>
    </html>
    """

    # Anexar o corpo da mensagem
    with open( fileParam, "rb") as attachment:
        msg.attach(MIMEText( html, 'html'))
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

        # Codificar o arquivo em base64
        encoders.encode_base64(part)
        
        # Adicionar o cabeçalho ao arquivo anexado
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {fileParam.split('/')[-1]}",  # Extrai apenas o nome do arquivo
        )
        
        # Anexar o arquivo à mensagem
        msg.attach(part)
    #=========================================================
    # Conectar ao servidor SMTP do Gmail e enviar o e-mail
    try:
        text = msg.as_string()

        account_address = "juridico.ia.gruposouzalima@gmail.com"
        password = "atbj yvro izgp edhc"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Iniciar a conexão TLS
        server.login(account_address , password)

        #server.sendmail( from_address , [to_address] + cc_address, text)
        # server.sendmail( from_address , to_address, text)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")
    finally:
        server.quit()


'''
    # Lista de arquivos a serem anexados


    # Iterar sobre a lista de arquivos e anexar cada um
    for arquivo in arquivos:
        filename = f"{diretorio}/{arquivo}"
        with open(filename, "rb") as attachment:
            # Criar uma instância MIMEBase e nomear o anexo
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        
            # Codificar o arquivo em base64
            encoders.encode_base64(part)
            
            # Adicionar o cabeçalho ao arquivo anexado
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {filename.split('/')[-1]}",  # Extrai apenas o nome do arquivo
            )
            
            # Anexar o arquivo à mensagem
            msg.attach(part)




    #==============================================

    """

    # Especificar o caminho do arquivo que você deseja anexar
    filename = "/opt/bitnami/nginx/html/py-email-send/README.md"  # Exemplo: "documento.pdf"
    filename2 = "/opt/bitnami/nginx/html/py-ocr/src/publicacoes/saida"
    # Abrir o arquivo no modo binário
    with open(filename, "rb") as attachment:
        # Criar uma instância MIMEBase e nomear o anexo
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Codificar o arquivo em base64
    encoders.encode_base64(part)

    # Adicionar o cabeçalho ao arquivo anexado
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    # Anexar o arquivo à mensagem
    msg.attach(part)

    """


'''






#============================================================
#                      MAIN
#============================================================

destinos = {}
destinos["dra-ana"] = Destino("Dra Ana", "flavia.coelho@gruposouzalima.com")
destinos["dra-mariana"] = Destino("Dra Mariana", "flavia.coelho@gruposouzalima.com")
destinos["dra-nelia"] = Destino("Dra Nelia", "flavia.coelho@gruposouzalima.com")
destinos["dra-neusa"] = Destino("Dra Neusa", "flavia.coelho@gruposouzalima.com")
destinos["dra-simone"] = Destino("Dra Simone", "flavia.coelho@gruposouzalima.com")
destinos["dra-alecsandro"] = Destino("Dra Simone", "flavia.coelho@gruposouzalima.com")

lista = []
lista.append( 'luis.bortoletti@gruposouzalima.com' )
lista.append( 'brenno.cardoso@gruposouzalima.com' )
lista.append( 'flavia.coelho@gruposouzalima.com' )
lista.append( 'neusa.sotana@gruposouzalima.com' )
lista.append( 'mariana.gallo@gruposouzalima.com' )



# Especificar o diretório
diretorio = "/opt/bitnami/nginx/html/py-ocr/src/publicacoes-v2/saida"

for chave, destino in destinos.items():
    print( f"{chave} - {destino}")

    # Listar todos os arquivos no diretório
    arquivos = os.listdir(diretorio)

    for arquivo in arquivos:
      if( re.search( chave, arquivo ) ):
        print( f"{arquivo}")
        for endereco in lista:
            sendEmail( f"{diretorio}/{arquivo}", destino, endereco  )


