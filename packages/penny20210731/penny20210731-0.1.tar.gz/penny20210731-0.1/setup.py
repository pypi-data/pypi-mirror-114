from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(name='penny20210731',
      version='0.1',
      long_description = long_description,
      long_description_content_type="text/markdown",
      description='Taiwan No. 1',
      url='http://github.com/storborg/penny20210731',
      author='Michael Chen',
      author_email='flyingcircus@example.com',
      license='MIT',
      packages=['penny20210731'],
      zip_safe=False)