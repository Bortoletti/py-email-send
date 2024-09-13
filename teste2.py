import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
remetente = "helpdesk@gruposouzalima.com"
senha = "He03502@#$!"

conta_email = "luis.bortoletti@gruposouzalima.com"
senha     = "Lu@Souz@L1m@"
senha     = "Borto!2024#01"

remetente = 'juridico.publicacao@gruposouzalima.com'
#senha =  'SouzaLima@2024'

destinatario = "luis.bortoletti@gruposouzalima.com"

assunto      = "Teste de envio de e-mail"
mensagem     = "Este é um teste de envio de e-mail via Python."




smtp_server = "smtp-relay.gmail.com"
smtp_port = 587

msg = MIMEMultipart()
msg['From'] = remetente
msg['To'] = destinatario
msg['Subject'] = assunto
msg.attach(MIMEText(mensagem, 'plain'))

try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Inicia uma conexão segura (TLS)

    server.login( conta_email, senha )

    server.sendmail(remetente, destinatario, msg.as_string())
    print("E-mail enviado com sucesso!")

except Exception as e:
    print(f"Erro ao enviar e-mail: {e}")