
from setuptools import setup

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
  name = 'AD-byteme',         # How you named your package folder (MyLib)
  packages = ['AD-byteme'],   # Chose the same as "name"
  version = '0.1.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Automatic differentiation library',   # Give a short description about your library
  author = 'CS107 Group 28: ByteMe',                   # Type in your name
  author_email = 'gcpasco@college.harvard.edu',      # Type in your E-Mail
  #long_description = long_description,
  #long_description_content_type = "text/markdown",
  url = 'https://github.com/cs107-byteme/cs107-FinalProject',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/cs107-byteme/cs107-FinalProject/archive/refs/tags/alpha.tar.gz',    
  keywords = ['AUTOMATIC DIFFERENTIATION'],   # Keywords that define your package best
  install_requires=[            # All of our dependencies
          'numpy'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)