class GameRulesException(Exception):
    """
    Exception raised when the user doesn't play by the rules of the game.
    """
    pass


class UserRequestException(Exception):
    """
    Exception raised when the user request doesn't match the expected format.
    """
    pass
