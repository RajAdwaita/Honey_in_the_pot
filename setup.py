from setuptools import setup  # Run setup


def readme_file_contents():  # Read the README file
    with open('README.rst') as readme_file:  # Open the README file
        data = readme_file.read()  # Read the README file contents into data variable
    return data  # Return the data variable


# setup will have all info about the project and the packaging


setup(
    name='nanopot',
    version='1.0.0',  # version number
    description='Simple TCP honeypot',
    # every time we push it to pip install will always have information from our readme file
    long_description=readme_file_contents(),
    author='RajModak',
    author_email='adwaitaraj@gmail.com',
    license='MIT',
    packages=['nanopot'],  # this is the name of the package

    # if we have a package that is not a zip file then we need to set this to false
    zip_safe=False,
    install_requires=[]  # list of packages that are required to run the project
)

# we can do python setup.py develop and it will link everything to my working stuff as if I did a python setup.py install
