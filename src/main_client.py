import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




class MailClient:
    def __init__(self, subjectParam, toParam, messageParam ):
        self.subject = subjectParam
        self.to = toParam
        self.message = messageParam
        
    def send( self ):
        sender = 'juridico.publicacao@gruposouzalima.com'
        user = 'gruposouzalima'
        password = 'cTgqvpYm4961'
        s = smtplib.SMTP('smtplw.com.br', 587)
        s.set_debuglevel(0)
        s.login(user, password)
        s.sendmail(sender, self.to, self.message )
        s.quit()

#===================================================================
sender = 'juridico.publicacao@gruposouzalima.com'

msg = MIMEMultipart()

msg['Subject'] = 'teste'
msg['From'] = sender
msg['To'] = 'luis.bortoletti@gruposouzalima.com' # recipients

msg.attach(MIMEText( "<h1>inicio</h1>", 'html'))

message = msg.as_string()

mail = MailClient( "titulo de testes", 'luis.bortoletti@gruposouzalima.com', message )
mail.send()

print("*******************  Fim  *******************")