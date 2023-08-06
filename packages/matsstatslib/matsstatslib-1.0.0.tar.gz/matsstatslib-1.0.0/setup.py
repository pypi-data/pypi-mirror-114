from setuptools import setup, find_packages, version
import setuptools

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Programming Language :: Python :: 3.9'
]

setup(name='matsstatslib',
      version='1.0.0',
      description='a library of statistical tools',
      long_description='''
      FILL THIS IN
      ''',
      url='https://upload.pypi.org/legacy/',
      author='Matthew Fyfe',
      author_email='mfyfeatlethenty@hotmail.co.uk',
      license='mit',
      classifiers=classifiers,
      keywords='regression, probabilities, ADD MORE HERE',
      packages=find_packages(),
      install_requires=[''])

