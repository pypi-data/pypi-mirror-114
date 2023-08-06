from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='nikipy2021',
      version='0.1',
      long_description = long_description,
      long_description_content_type="text/markdown",
      description='Taiwan No. 1',
      url='http://github.com/storborg/funniest',
      author='niki7120',
      author_email='niki.a7821@gmail.com',
      license='2Lriioai',
      packages=['nikipy2021'],
      zip_safe=False)