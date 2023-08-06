from setuptools import setup, find_packages

VERSION = '0.0.4' 
DESCRIPTION = 'Paint your terminal with beautifull colors.'
LONG_DESCRIPTION = 'This package lets you print colored text on the terminal.'
# Setting up
setup(
       # the name must match the folder name 'colorchef'
        name="colorchef", 
        version=VERSION,
        author="Mithilesh Pradhan",
        author_email="knowmit@gmail.com",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package.
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Information Technology",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)