from .Mail import Mail


class EmailVerification(Mail):

    def send(self, full_name: str, email: str, registration_token: str):
        """
        Sends verification email for newly registered accounts with registration_token.
        :param full_name: Person's Full Name
        :param email: Account's Email
        :param registration_token: Registration Token of Accounts On-Hold
        """

        uri: str = f"{self.SERVER_ADDRESS}/api/v1/verify-email?token={registration_token}"

        return self.send_mail(
            recipient_email=email,
            subject="Verify your account",
            body=f"Hello, {full_name}!\n\nHere's the link to complete your account registration.\n\n{uri}"
        )
