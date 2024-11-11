import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


sender     = 'juridico.publicacao@gruposouzalima.com'
recipients = ['luis.bortoletti@gruposouzalima.com', 'richard.bento@gruposouzalima.com']

msg = MIMEMultipart()

msg['Subject'] = 'JURIDICO: teste'
msg['From']    = sender
msg['To']      = sender

msg.attach(MIMEText( "<h1>Teste</h1>", 'html'))

message = msg.as_string()

user = 'gruposouzalima'
password = 'cTgqvpYm4961'
s = smtplib.SMTP('smtplw.com.br', 587)
s.set_debuglevel(0)
s.login(user, password)
s.sendmail(sender, recipients, message )
s.quit()
