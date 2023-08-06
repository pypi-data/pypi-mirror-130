# -*- coding: utf-8 -*-
#
# setup.py
# Create source distribution with: python setup.py sdist
#
import re
from distutils.core import setup
from version import pump_version, get_version, get_minor, get_camel

pump_version()
ver = get_version()
print(f'version: {ver}')
minor = get_minor(ver)
ver_camel = get_camel(ver)

setup(name='dl2050utils',
      packages=['dl2050utils'],
      version=ver,
      license='MIT',
      description='Utils lib',
      author='João Neto',
      author_email='joao.filipe.neto@gmail.com',
      keywords=['utils'],
      url='https://github.com/jn2050/utils',
      download_url=f'https://github.com/jn2050/utils/archive/v_{ver_camel}.tar.gz',
      # install_requires=[
      #       'pathlib',
      #       'zipfile',
      #       'json',
      #       'socket',
      #       'smtplib',
      #       'ssl',
      #       'boto3',
      #       'asyncpg',
      #       '',
      # ],
      classifiers=[
            'Development Status :: 4 - Beta',      # "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Build Tools',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3.7',
      ],
)
