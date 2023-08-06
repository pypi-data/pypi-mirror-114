from setuptools import setup
from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='qfunction',
    version='1.0.1642',
    url='https://github.com/gpftc/qfunction',
    license='MIT License',
    author='Reinan Br',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='slimchatuba@gmail.com',
    keywords='qfunction non-extensive mechanical statistical data science',
    description=u'Library for researcher with statistics and mechanics equation non-extensive 📈📊📚',
    packages=find_packages(),
    install_requires=['numpy','qutip','tqdm','matplotlib','imageio','bs4','requests'],)