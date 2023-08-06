from distutils.core import setup
    
setup(name="FirestoreExtractor", 
      version="1.5", 
      url="https://github.com/praKhr/FirestoreExtractor",
      download_url="https://github.com/prakHr/FirestoreExtractor-v/archive/refs/tags/v15.tar.gz",
      install_requires=[            # I get to this in a second
          'firebase-admin',
      ],
      maintainer='Prakhar Gandhi',
      maintainer_email='gprakhar0@gmail.com',
      py_modules=['FirestoreExtractor'],
      description="Extracts data from cloud firestore and firebase database") 
#from distutils.core import setup
'''
from setuptools import setup, find_packages

setup(
  name = 'FirestoreExtractor',         # How you named your package folder (MyLib)
  packages = find_packages('firestore_extractor_database'),   # Chose the same as "name"
  version = '0.7',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Extracts data from cloud firestore and firebase database',   # Give a short description about your library
  author = 'Prakhar Gandhi',                   # Type in your name
  author_email = 'gprakhar0@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/praKhr/FirestoreExtractor',   # Provide either the link to your github or to your website
  download_url ='https://github.com/prakHr/FirestoreExtractor/archive/refs/tags/v_07.tar.gz',    # I explain this later on
  keywords = ['cloud-firestore', 'firebase', 'firestore'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'firebase-admin',
      ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
  ],
)
'''
