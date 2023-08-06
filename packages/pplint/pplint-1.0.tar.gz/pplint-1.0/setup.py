from setuptools import setup, find_packages

setup(
    name='pplint',
    version='1.0',
    description='Thie is localLint of the setup',
    author='liudeping',
    author_email='liudeping@bytedance.com',
    packages=find_packages(),
    install_requires=[
        'GitPython>=3.1.8',
        'unidiff>=0.6.0'
    ]
)
