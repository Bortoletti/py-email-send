import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# Especificar o diretório
diretorio = "/opt/bitnami/nginx/html/py-ocr/src/publicacoes/saida"

# Listar todos os arquivos no diretório
arquivos = os.listdir(diretorio)

#for arquivo in arquivos:
#  print( f"{arquivo}")






# Informações do remetente e destinatário
sender_email = "lbortoletti@gmail.com"
receiver_email = "lbortoletti@gmail.com"
password = "erfk nddl dqqj xabr"

# Configurar a mensagem
subject = "Assunto do E-mail"


body = f"""<h1>Teste de e-mail</h1>
<p>Material em anexo
<a href='https://www.gruposouzalima.com' >Grupo</a>
"""

msg = MIMEMultipart()
msg['From'] = sender_email
msg['To'] = receiver_email
msg['Subject'] = subject

# Anexar o corpo da mensagem
msg.attach(MIMEText(body, 'html'))


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
