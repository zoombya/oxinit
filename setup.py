from setuptools import setup 

setup(
    name = 'az_oxinit',
    version = '1.0', 
    py_modules = ['relaxer'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        oxy=relaxer:cli 
    ''' 
)