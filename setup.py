from setuptools import find_packages,setup
from typing import List

hyphen='-e.'

def get_req(file_path:str)->List[str]:
    # this function will return a list of all the library that are in the file that is givern as input

    req=[]
    with open(file_path) as obj :
        req=obj.readlines()
        req=[r.replace('\n','') for r in req]

        if hyphen in req:
            req.remove(hyphen)

    return req 

setup(
    name='ML_Project_1',
    version='0.0.1',
    author='Parth Billore',
    author_email='billoreparth80@gmail.com',
    packages=find_packages(),
    install_requires=get_req('requirements.txt')
    
)