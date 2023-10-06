
from pypinyin import pinyin, Style
from lex import Lexer
import hashlib

def getAlphaNumericVar(var: str) -> None:
    """
    Return a variable name that is alphanumeric.
    
    Parameters:
    var (str): The variable name to convert.
    """
    if not Lexer.ischinese(var):
        return var
    
    # Convert to Pinyin (with tone marks)
    pinyin_word = ''.join([item[0] for item in pinyin(var, style=Style.NORMAL)])

    # Generate a unique identifier
    unique_hash = hashlib.sha256(var.encode()).hexdigest()

    # Create a unique variable name
    variable_name = f"{pinyin_word}_{unique_hash}"

    return variable_name
