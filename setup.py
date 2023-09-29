from setuptools import setup, find_packages

setup(
    name='pyhan',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'click',
        'pypinyin'
    ],
    entry_points='''
        [console_scripts]
        pyhan=cli.pyhan_cli:execute
    ''',
)
