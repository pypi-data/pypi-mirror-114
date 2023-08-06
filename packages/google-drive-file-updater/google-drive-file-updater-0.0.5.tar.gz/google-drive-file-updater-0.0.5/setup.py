from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.5'
DESCRIPTION = 'Google Drive file updater'
LONG_DESCRIPTION = open('README.md').read()

# Setting up
setup(
    name='google-drive-file-updater',
    version=VERSION,
    author='Daniel Riffert',
    author_email='riffert.daniel@gmail.com',
    description=DESCRIPTION,
    long_description_content_type='text/markdown',
    long_description=LONG_DESCRIPTION,
    package_dir={'':'src'},
    packages=['gd_fup'],
    scripts=['src/gdfup.py'],
    install_requires=['colorama', 'pywin32', 'google-api-python-client', 'google-auth-httplib2', 'google-auth-oauthlib'],
    keywords=['file', 'update', 'path', 'backup', 'google drive'],
)