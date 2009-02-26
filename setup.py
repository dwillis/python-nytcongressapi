from distutils.core import setup
from nytcongressapi import __version__,__license__,__doc__
 
license_text = open('LICENSE').read()
long_description = open('README.rst').read()
 
setup(name="python-nytcongressapi",
      version=__version__,
      py_modules=["nytcongressapi"],
      description="Libraries for interacting with The New York Times Congress API",
      author="Derek Willis",
      author_email = "dwillis@gmail.com",
      license=license_text,
      url="http://github.com/dwillis/python-nytcongressapi/",
      long_description=long_description,
      platforms=["any"],
      classifiers=["Development Status :: 1 - Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: BSD License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Topic :: Software Development :: Libraries :: Python Modules",
                   ],
       install_requires=["simplejson >= 1.8"]
      )