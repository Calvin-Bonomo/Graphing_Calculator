from EquationToken import EqToken as Token
import EquationTokenTypes as TokenType
import re

class EqTokenizer:
    def __init__(self):
        self.bad_eq = False
        self.current_state = 0x0
        self.current_token = Token()

    def getTokens(self, equation: str) -> list(Token):
         self.__resetStates()
         tokens = self.__tokenizeEqHelper(equation, list())
         # Check that this is even a valid sequence
         if (not self.__validateTokens(tokens)) or self.bad_eq:
             return list()
         return tokens

    def __tokenizeEqHelper(self, equation: str, tokens: list(Token)) -> list(Token):
        if equation == "" or self.bad_eq:
            return tokens
        return self.__tokenizeEqHelper(equation[1:], self.__handleState(equation[0], tokens))
        
    def __handleState(self, char: str, tokens: list(Token)) -> list(Token):
        match self.current_state:
            case 0x0: # Base state
                # Don't add token, this is only
                # at the start of the program
                self.__transitionState(char)
                return self.__handleState(char, tokens)
            case 0x1: # Number state
                if re.match("[\d.]", char) == None:
                    tokens.append(self.current_token)
                    self.current_token = Token()
                    self.__transitionState(char)
                    return self.__handleState(char, tokens)
                else:
                    self.current_token.addChar(char)
                    return tokens
            case 0x2: # Operator state
                return tokens
            case 0x4: # Parentheses state
                return tokens
            case default: # Throw an error
                self.bad_eq = True
                return tokens
    
    def __transitionState(self, char: str) -> None:
        # Handle negative numbers
        if re.match("-", char) != None:
            # Parentheses last
            if self.current_state ^ 0x4 == 0:
                self.current_token.setType(TokenType.TOKEN_NUMBER)
                self.current_state = 0x1
            # Number last
            elif self.current_state ^ 0x1 == 0:
                self.current_token.setType(TokenType.TOKEN_OPERATOR)
                self.current_state = 0x2
        elif re.match("[\d.]", char) != None:
            self.current_token.setType(TokenType.TOKEN_NUMBER)
            self.current_state = 0x1
        else:
            self.current_state = 0x0 # This shouldn't happen just fyi
    
    def __resetStates(self) -> None:
        self.bad_eq = False
        self.current_state = 0x0
        self.current_token = Token()