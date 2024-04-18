import os.path
from .Mail import Mail


class WelcomeEmail(Mail):

    def send(self, email: str):
        """
        Sends welcome email to accounts who just verified email.
        :param email: Account's Email
        """

        # Calculate Template Path
        template_path: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "templates", "welcome_email.html"
        )

        # Read Body Content
        with open(template_path, encoding="utf-8") as file:
            content: str = file.read().strip()

        # Send Mail
        return self.send_mail(
            recipient_email=email,
            subject="Welcome!",
            body=content
        )
