import setuptools
from distutils.core import setup

setup(
  name = 'up_results',         # How you named your package folder (MyLib)
  packages = ['up_results'],   # Chose the same as "name"
  version = 'v0.4',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = "Result maker of roll numbers from excel sheet for UP Board, India",   # Give a short description about your library"
  author = 'Aniket Upadhyay and Tanzeel Ur Rahman',                   # Type in your name
  author_email = 'iamtanzeel1998@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/ponyket/up_results',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/ponyket/up_results/archive/refs/tags/v0.3.tar.gz',    # I explain this later on
  keywords = ['UP board', 'result', 'scraper'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'selenium',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)