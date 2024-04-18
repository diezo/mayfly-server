import os.path
from .Mail import Mail


class OTPEmailVerification(Mail):

    def send(self, email: str, otp: str):
        """
        Sends verification email for newly registered accounts with registration_token.
        :param email: Account's Email
        :param otp: OTP For Email Verification
        """

        # Calculate Template Path
        template_path: str = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "templates", "otp_email_verification.html"
        )

        # Read Body Content
        with open(template_path, encoding="utf-8") as file:
            content: str = file.read().strip()

        # Replace Placeholders
        content = content.replace("{{otp}}", otp)

        # Send Mail
        return self.send_mail(
            recipient_email=email,
            subject="Verify your account",
            body=content
        )
