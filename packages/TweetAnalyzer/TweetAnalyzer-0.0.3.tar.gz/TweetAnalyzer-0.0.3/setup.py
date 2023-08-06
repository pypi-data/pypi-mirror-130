from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'Tweet Analyzer Package'
LONG_DESCRIPTION = 'A simple package to demonstrate the usage of TextBlob from tweet analysis'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="TweetAnalyzer", 
        version=VERSION,
        author="Daniel Becker",
        author_email="dbecker1@g.emporia.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package', 'textblob'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)