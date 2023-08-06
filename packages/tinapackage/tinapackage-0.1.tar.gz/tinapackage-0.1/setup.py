from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='tinapackage',
      version='0.1',
      long_description = long_description,
      long_description_content_type="text/markdown",
      description='Taiwan No. 1',
      url='http://github.com/storborg/funniest',
      author='Michael Chen',
      author_email='tinalin5665@gmail.com',
      license='MIT',
      packages=['tinapackage'],
      zip_safe=False)