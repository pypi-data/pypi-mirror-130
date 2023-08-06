from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Luke Twitter Sentiment'
LONG_DESCRIPTION = 'Sentiment reader on the given CSV file'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="assignment11Luke", 
        version=VERSION,
        author="Luke Cunningham",
        author_email="lcunnin2@g.emporia.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=['textblob', 'pandas'], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)