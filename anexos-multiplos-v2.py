import os
import glob
import re
import json
from datetime import datetime
import smtplib
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email import encoders
import random
import time

def getRandom():
   return random.randint(100, 999) 

def getTimestampFmt2():
   now = datetime.now()
   return now.strftime("%Y-%m-%d-%H:%M:%S")


class Logger:
    def __init__( self, fileLogParam ):
        self.fileLog = fileLogParam
    
    def write( self, msg ):
        with open( self.fileLog, 'a') as logFile:
            logFile.write( f"{getTimestampFmt2()}: {msg}\n" )
            logFile.close()





#============================== DESTINO    ==============================

class Destino:
    def __init__(self, nome, email, chaveParam ):
        self.nome = nome
        self.email = email
        self.chave = chaveParam

    def __str__(self):
        return f"'destino':'chave':'{self.chave}','nome':'{self.nome}', 'email':'{self.email}'"

#============================== ENVIAR EMAIL   ==============================

def sendEmail( fileParam, destinoParam, server, logar ):
    # global server
    logar.write("-----------------------  INICIO DE ENVIO  ----------------------------")
    logar.write(f"Arquivo....: {fileParam}")
    logar.write(f"Chave......: {destinoParam.chave}")
    logar.write(f"Nome.......: {destinoParam.nome}")
    logar.write(f"Email......: {destinoParam.email}")

    from_address    = "juridico.publicacao@gruposouzalima.com"

    to_address = destinoParam.email 

    # arquivo JSON
    #================================================================
    jsonFile = re.sub(r'\.pdf$', '.json', fileParam )
    publicacao = None
    #print( jsonFile )
    with open(  jsonFile , "rb") as jsonConteudo:
        publicacao = json.loads(  jsonConteudo.read() )
        #print( publicacao['id'] )

    logar.write(f"Citados....: {publicacao['citados']}")
    logar.write(f"Reclamadas.: {publicacao['reclamadas']}")

 
    cc_address      = []
    if( destinoParam.chave == 'controle'):
        cc_address.append( 'mariana.gallo@gruposouzalima.com' )
    if( publicacao['horas48'] ):
        cc_address.append( 'neusa.sotana@gruposouzalima.com' )
        cc_address.append( 'mariana.gallo@gruposouzalima.com' )
    """
    if( not destinoParam.chave == 'dra-neusa'):
        cc_address.append( 'neusa.sotana@gruposouzalima.com' )
    if( not destinoParam.chave == 'dra-mariana'):
        cc_address.append( 'mariana.gallo@gruposouzalima.com' )
    """
    #cc_address.append( 'luis.bortoletti@gruposouzalima.com' )
    #cc_address.append( 'richard.bento@gruposouzalima.com' )

    # Configurar a mensagem

    subject = f"{destino.nome}"
    subject = f"{subject} - {publicacao['processo'].replace(':','')}"
    subject = f"{subject} - {publicacao['id']} - {getTimestampFmt2()}-{random.randint(1, 10)} "

    if( publicacao['horas48'] ):
        subject = f"*** 48 HORAS *** {subject}"

    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Cc'] = ', '.join(cc_address)  # Adicionando os endereços de Cc
    msg['Subject'] = subject

    # Anexando a imagem
    with open('/opt/bitnami/nginx/html/py-email-send/img/logo-souzalima.JPG', 'rb') as img:
        mime_image = MIMEImage(img.read())
        mime_image.add_header('Content-ID', '<logo>')
        msg.attach(mime_image)

    destinos = ''
    if( destinoParam.chave == 'controle'):
        destinos = publicacao['destino']

    html = f"""
    <html>
    <body>
        <p><b>{destinos}</b></p>
        <img src="cid:logo">
        <p>Olá, {destinoParam.nome}
        <br>Processo: {publicacao['processo']}
        </p>
        <hr>
        <pre style="font-size: 16px;">{publicacao['linha']}</pre>
    </body>
    </html>
    """

    #logar.write( f"{html}")

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
    text = msg.as_string()

    from_address    = "juridico.publicacao@gruposouzalima.com"
    

    logar.write( f"Assunto..: {subject}")
    logar.write( f"from.....: {from_address}" )
    logar.write( f"to.......:{[to_address] + cc_address}")

    #"""
    try:

        time.sleep(2)

        server.sendmail( from_address , [to_address] + cc_address, text)
        logar.write("****************************   EMAIL ENVIADO   ****************************")
        try:
            os.remove( fileParam )
            os.remove( jsonFile )
            logar.write(f"removido: {fileParam}")
        except Exception as e:
            logar.write( f"{e}")
            pass
        

    except Exception as e:
       logar.write( f"{e}")
       pass
    #"""
    
    





#============================================================
#                      MAIN
#============================================================

logar = Logger( f"/opt/bitnami/nginx/html/py-email-send/logs/enviar-email-{getTimestampFmt2()}-{getRandom()}")
logar.write("====================   INICIO   ========================")

logar.write("====================   CONECTAR SMTP   ========================")

"""
server = smtplib.SMTP('smtp-relay.gmail.com', 587)
server.starttls()  # Iniciar a conexão TLS

# Conectar ao servidor SMTP do Gmail e enviar o e-mail
conta_email = "luis.bortoletti@gruposouzalima.com"
password = "Borto!2024#01"
server.login( conta_email , password)
"""

server = smtplib.SMTP('smtplw.com.br', 587)
server.set_debuglevel(0)
#server.starttls()  # Iniciar a conexão TLS

user = 'gruposouzalima'
password = 'cTgqvpYm4961'
server.login(user, password)

logar.write("====================   INICIO   ========================")

destinos = {}
destinos["controle"] = Destino("controle", "neusa.sotana@gruposouzalima.com","controle")
destinos["dr-alecsandro"] = Destino("Dr Alecsandro", "alecsandro.silva@gruposouzalima.com","dr-alecsandro")
destinos["dra-ana"] = Destino("Dra Ana", "ana.takahashi@gruposouzalima.com","dra-ana")
destinos["dra-lais"] = Destino("Dra Lais", "lais.goncalves@gruposouzalima.com","dra-lais")
destinos["dra-mariana"] = Destino("Dra Mariana", "mariana.gallo@gruposouzalima.com","dra-mariana")
destinos["dra-maria-avelino"] = Destino("Dra Maria Avelino", "maria.avelino@gruposouzalima.com","dra-maria-avelino")
destinos["dra-nelia"] = Destino("Dra Nelia", "nelia.fernandes@gruposouzalima.com","dra-nelia")
destinos["dra-neusa"] = Destino("Dra Neusa", "neusa.sotana@gruposouzalima.com","dra-neusa")
destinos["dr-rafael"] = Destino("Dr Rafael", "rafael.santos@gruposouzalima.com","dr-rafael")
destinos["dra-raquel"] = Destino("Dra Raquel", "raquel.fonseca@gruposouzalima.com","dra-raquel")
destinos["dra-simone"] = Destino("Dra Simone", "simone.vieira@gruposouzalima.com","dra-simone")
destinos["dra-vania"] = Destino("Dra Vania", "vania.moura@gruposouzalima.com","dra-simone")



lista = []
lista.append( 'luis.bortoletti@gruposouzalima.com' )
"""
lista.append( 'brenno.cardoso@gruposouzalima.com' )
lista.append( 'flavia.coelho@gruposouzalima.com' )
lista.append( 'neusa.sotana@gruposouzalima.com' )
lista.append( 'mariana.gallo@gruposouzalima.com' )
"""


# Especificar o diretório
diretorio = "/opt/bitnami/nginx/html/py-ocr/src/publicacoes-v3/saida"
#diretorio = "/opt/bitnami/nginx/html/py-email-send/tmp"


for chave, destino in destinos.items():
    logar.write( f"{chave} - {destino}")

    # Listar todos os arquivos no diretório
    arquivos = os.listdir(diretorio)
    arquivos = glob.glob(os.path.join(diretorio, '*.pdf'))

    for arquivo in arquivos:
        if( re.search( chave, arquivo ) ):
            logar.write( f"{arquivo}")
            #destino.email = "luis.bortoletti@gruposouzalima.com"
            sendEmail( f"{arquivo}", destino, server, logar  )


server.quit()

logar.write("====================   FIM   ========================")
