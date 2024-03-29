import sys

# Make sure we are running python3.5+
if 10 * sys.version_info[0]  + sys.version_info[1] < 35:
    sys.exit("Sorry, only Python 3.5+ is supported.")

from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(
      name             =   'pfdo_med2image',
      version          =   '2.0.4',
      description      =   'Runs med2image on each nested dir of an inputdir',
      long_description =   readme(),
      author           =   'FNNDSC',
      author_email     =   'dev@babymri.org',
      url              =   'https://github.com/FNNDSC/pfdo_med2image',
      packages         =   ['pfdo_med2image'],
      install_requires =   ['pfmisc', 'pftree', 'pfdo', 'med2image'],
      #test_suite       =   'nose.collector',
      #tests_require    =   ['nose'],
      #scripts          =   ['bin/pfdo_med2image'],
      entry_points={
          'console_scripts': [
              'pfdo_med2image = pfdo_med2image.__main__:main'
          ]
      },
      license          =   'MIT',
      zip_safe         =   False
)
