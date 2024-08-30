import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Informações do remetente e destinatário
sender_email = "lbortoletti@gmail.com"
receiver_email = "lbortoletti@gmail.com"
password = "erfk nddl dqqj xabr"

# Configurar a mensagem
subject = "Assunto do E-mail - teste"

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
