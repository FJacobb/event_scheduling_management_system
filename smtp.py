import smtplib, ssl

class Email():
    def __init__(self):
        self.email = "festusj53@gmail.com"
        self.password= 'sgnhecngtblnsgvj'
        self.port = 587

    def send_mail(self, to_addrs, message):
        with smtplib.SMTP('smtp.gmail.com', self.port) as mail:
           try:
               mail.starttls()
               mail.login(self.email, self.password)
               mail.sendmail(self.email, to_addrs, message)
               return True
           except:
               print("error in connecting to the mail server!")
