from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr


class Mail:

    SERVER_ADDRESS: str = "http://localhost"

    DISPLAY_NAME: str = "MayFly Automated Bot"
    EMAIL: str = "mayflybackend@gmail.com"
    PASSWORD: str = "mwpt lztu daer cnri"

    session: SMTP

    def __init__(self) -> None:
        """
        Initializes SMTP Server to Send Emails.
        """

        self.session = SMTP("smtp.gmail.com", 587)

        self.session.starttls()
        self.session.login(self.EMAIL, self.PASSWORD)

    def send_mail(self, recipient_email: str, subject: str, body: str):
        """
        Sends an email to recipient with given fields.
        :param recipient_email: Recipient's email address
        :param subject: Subject line
        :param body: HTML Text Body
        :return: Boolean
        """

        # Prepare Message
        message: MIMEMultipart = MIMEMultipart()
        message["From"] = formataddr((self.DISPLAY_NAME, self.EMAIL))
        message["To"] = recipient_email
        message["Subject"] = subject

        # Attach HTML-Text Body
        message.attach(MIMEText(body, "html"))

        # Send Mail
        self.session.sendmail(self.EMAIL, recipient_email, message.as_string())
