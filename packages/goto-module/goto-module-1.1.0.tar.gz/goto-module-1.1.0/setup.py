from setuptools import setup, find_packages

with open(('README.md'),encoding='utf-8') as f:
          LONG_DESCRIPTION = f.read()
          #print(LONG_DESCRIPTION)
          

VERSION = '1.1.0' 
DESCRIPTION = 'Goto module'
#LONG_DESCRIPTION =open("README.md",'r')

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="goto-module", 
        version=VERSION,
        author="Meet Patel",
        author_email="<meetp6116@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'goto package','goto','goto-module','goto module'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
