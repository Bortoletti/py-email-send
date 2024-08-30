import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class Destino:
    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def __str__(self):
        return f"Destino(nome={self.nome}, email={self.email})"


destinos = {}
destinos["dra-ana"] = Destino( "Dr Ana", "lbortoletti@gmail.com" )
destinos["dra-mariana"] = Destino( "Dr Mariana", "lbortoletti@gmail.com" )
destinos["dra-nelia"] = Destino( "Dr Nelia", "lbortoletti@gmail.com" )
destinos["dra-neusa"] = Destino( "Dr Neusa", "lbortoletti@gmail.com" )
destinos["dra-simone"] = Destino( "Dr Simone", "lbortoletti@gmail.com" )


"""
Flavia Coelho da Silva <flavia.coelho@gruposouzalima.com>
cc:	Neusa Aparecida Sotana De Souza <neusa.sotana@gruposouzalima.com>,
Mariana Pizzitola Gallo <mariana.gallo@gruposouzalima.com>
"""


for arquivo, destino in destinos.items():

    # Informações do remetente e destinatário
    sender_email = "lbortoletti@gmail.com"
    password = "erfk nddl dqqj xabr"
    receiver_email = destino.email

    # Configurar a mensagem
    subject = f"Assunto do E-mail - {destino.nome}" 


    body = f"""<h1>Publicações de hoje</h1>
    <p>Material em anexo
    """

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Anexar o corpo da mensagem
    msg.attach(MIMEText(body, 'html'))


    #==============================================

 
    # Especificar o caminho do arquivo que você deseja anexar
    filename = f"/opt/bitnami/nginx/html/py-ocr/src/publicacoes/saida/{arquivo}.pdf"
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

        #=========================================================
    # Conectar ao servidor SMTP do Gmail e enviar o e-mail
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Iniciar a conexão TLS
        server.login(sender_email, password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao enviar o e-mail: {e}")
    finally:
        server.quit()
