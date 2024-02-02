import EquationTokenTypes as TokenTypes

class EqToken:
    def __init__(self):
        self.token = ""
        self.token_type = TokenTypes.TOKEN_NONE
    
    def addChar(self, new_char: str) -> None:
        self.token += new_char
    
    def setType(self, new_type: int) -> None:
        self.token_type = new_type