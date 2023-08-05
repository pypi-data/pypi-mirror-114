from setuptools import setup, find_packages




long_description = "FUNCTIONS:\n\n  get_key(url) -> gets the key to the sourcebin out of the link(must be a valid link)\n\n  get_url(key) -> takes in the key to a sourcebin and turns it into a sourbin url\n\n  create(name, code, title=\"None\", description=\"None\") -> creates a sourcbin with the inputted code\n\n  read_key(key) -> returns the contents of the sourbin with that key\n\n  read_url(url) -> same as read_key but you can put in a sourbin url"

setup(
  name='pysourcebin',
  version='0.0.3',
  description='a sourcebin api wrapper',
  long_description=long_description,
  url='',
  author='Amashi',
  author_email='amashisenpai386@gmail.com',
  license='MIT',
  classifiers=[
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
],
  keywords=['sourcebin', 'source', 'bin'],
  packages=find_packages(),
  install_requires=['']
)
