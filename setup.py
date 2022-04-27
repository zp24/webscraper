from setuptools import setup
from setuptools import find_packages

setup(
    name='se_scraper_test', ## This will be the name your package will be published with
    version='0.0.1', 
    description='Test package that scrapes',
    # url='https://github.com/zp24/New_Repo', # Add the URL of your github repo if published 
                                                                   # in GitHub
    author='Zoya Pasha', # Your name
    # license='MIT',
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['webdriver_manager', 'selenium'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)