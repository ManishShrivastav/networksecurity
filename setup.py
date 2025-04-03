'''
The setup.py file is an essential part of packaging and distributing Python projects. It is used by setuptools(
or distutils in older Python versions) to define the configuration of the project as its metadata, dependencies, 
and more.
'''

from setuptools import find_packages, setup
from typing import List

from typing import List

HYPHEN_E_DOT = '-e .'

def get_requirements(file_path: str) -> List[str]:
    """
    This function will return the list of requirements from the given file,
    ignoring empty lines, comments, and '-e .' entries.
    """
    requirements_lst: List[str] = []
    
    try:
        with open(file_path, 'r') as file_obj:
            # Read all lines from the file
            lines = file_obj.readlines()
            
            # Process lines
            requirements_lst = [
                line.strip() for line in lines  # Remove leading/trailing whitespace
                if line.strip() and not line.startswith('#') and line.strip() != HYPHEN_E_DOT
            ]
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    return requirements_lst

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Manish",
    author_email="manish@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements("requirements.txt")
)
