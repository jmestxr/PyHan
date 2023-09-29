import click
import sys
import os
import tempfile
import subprocess

# # appending the directory of compiler.py in the sys.path list
sys.path.append(f"{os.path.dirname(__file__)}/../src")   
import compiler

# Define CLI version
VERSION = 'v0.0.1'

class CustomHelpCommand(click.Command):
    ASCII_ART =  """
 :::::::;,                
::        ;:                      
::        ::               ';,           
::       ,;'                 ';,    ,;::::::::::;,      
::::::::;'    ::      ::             ;;        ;; 
::             ::    ::     ';,       ;;      ;;    
::              ;;  ;;        ';       ':,  ,:'     
::               '::'            .:      '::'
::                ;;            ;'      .:'':.
                 ;;          ,;'      ,;'    ';,                 
             ,:;''        :;'      ,:;'        ';:,

"""

    HELP_MESSAGE = f"""
Compiler for Py汉 (PyHan) language.
Py汉 is equivalent to Python language, written in Simplified Chinese.
This compiler compiles Py汉 code into Python code.

{VERSION}

Usage: pyhan [OPTIONS] INPUT

  INPUT: Path to the Py汉 file to compile.

Options:
  -c, --compile      Compile only
  -o, --output PATH  Specified path of compiled .py file if --compile option
                     is enabled. If not provided, defaults to ./out.py.
  --help             Show this message and exit.\
"""

    def format_help(self, ctx, formatter):
        click.echo(click.style(self.ASCII_ART, fg="magenta", bold=True)+ self.HELP_MESSAGE)

def is_valid_file_path(file_path):
    """Check if a file path is valid.

    Parameters:
    file_path (str): The file path to check.

    Returns:
    bool: True if the file path is valid, False otherwise.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        return False

    # Check if it's a regular file (not a directory)
    if not os.path.isfile(file_path):
        return False

    # Check if the parent directory exists
    parent_directory = os.path.dirname(file_path)
    if not os.path.exists(parent_directory):
        return False

    # All checks passed, the file path is valid
    return True

@click.command(cls=CustomHelpCommand, no_args_is_help=True)
@click.argument('input', type=click.Path(exists=True))
@click.option('--compile', '-c', is_flag=True, help='Compile only.')
@click.option('--output', '-o', type=click.Path(file_okay=True),\
              help='Specified path of compiled .py file if --compile option is enabled. If not provided, defaults to ./out.py.')
def execute(input, compile, output):
    """Compiler for Py汉 (PyHan) language. \
Py汉 is equivalent to Python language, written in Simplified Chinese. \
This compiler compiles Py汉 code into Python code."""
    if not input.endswith('.pyhan'):
        raise click.BadArgumentUsage("Input file must have .pyhan extension")

    output_path = ""
    if compile:
        output_path = output if output else './out.py'
    else:
        temp_output_file = tempfile.NamedTemporaryFile()
        output_path = temp_output_file.name
        
    compiler.compile(input, output_path)

    if compile:
        return

    # Running the compiled Python code
    try:
        subprocess.run(['python', output_path], check=True)
    except subprocess.CalledProcessError as e:
        click.echo(e.stderr.decode())
    

if __name__ == '__main__':
    execute()
