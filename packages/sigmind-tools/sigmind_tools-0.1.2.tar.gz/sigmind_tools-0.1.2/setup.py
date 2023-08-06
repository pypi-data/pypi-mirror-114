from setuptools import setup, find_packages

setup(
    name='sigmind_tools',
    version='0.1.2',    
    author='Sigmind',
    packages= ['sigmind_tools',],
    install_requires=[
                      'boto3'
                      ],
)