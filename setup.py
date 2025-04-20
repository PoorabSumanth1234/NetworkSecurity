'''
The setup.py file is an essential  part of packaging and distributing 
python projects. It is used by setuptools (or distutils in older python versions)
to define the configuration of  your project such as its metadata, dependencies
and many more 
'''

from setuptools import find_packages,setup
from typing import List
#find packages is used to scan the folders and find out the __init__.py files
## the folder which has an __init__.py file will be considered as a package
# setup is resposible for providing the project information 

def get_requirements()->List[str]:
    '''
    This function will return list of requirements
    '''
    
    requirement_lst:List[str]=[]
    try:
        with open('requirements.txt','r')as file:
            # Read lines from the file 
            lines=file.readlines()
            #Proecess each line 
            for line in lines:
                requirement=line.strip()
                ## Ignore empty lines and -e .
                if requirement and requirement!= '-e .':
                    requirement_lst.append(requirement)
                    # if stmt tells that in requiremnts.txt what all dependencies are there except -e . they will be considered
    except Exception as e:
        print(e)
    
    return requirement_lst

print(get_requirements())

setup(
    name="NetworkSecurity",
    version='0.0.1',
    author="Poorab Sumanth",
    author_email="vpoorabsumanth04@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements()
)
                    
    
