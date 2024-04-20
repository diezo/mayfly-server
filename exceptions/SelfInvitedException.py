class SelfInvitedException(Exception):
    """
    When a user adds their own identifier in room invitees list.
    """

    def __init__(self): super().__init__()
