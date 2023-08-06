from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Lab 03 Package'
LONG_DESCRIPTION = 'Package for Lab 03. Manages Tweet Sentiment and adds it to a data frame.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="lab03", 
        version=VERSION,
        author="Nicholas Carr",
        author_email="ncarr@g.emporia.edu",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
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
