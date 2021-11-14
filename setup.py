from setuptools import setup


def readme_file_contents():
    with open('README.rst') as readme_file:
        data = readme_file.read()
    return data

# setup will have all info about the project and the packaging


setup(
    name='nanopot',
    version='1.0.0',
    description='Simple TCP honeypot',
    # every time we push it to pip install will always have information from our readme file
    long_description=readme_file_contents(),
    author='RajModak',
    author_email='adwaitaraj@gmail.com',
    license='MIT',
    packages=['nanopot'],
    zip_safe=False,
    install_requires=[]
)

# we can do python setup.py develop and it will link everything to my working stuff as if I did a python setup.py install
