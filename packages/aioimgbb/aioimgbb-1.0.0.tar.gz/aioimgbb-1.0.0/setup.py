from setuptools import setup, find_packages

setup(name='aioimgbb',
      version='1.0.0',
      description='No',
      packages=find_packages(exclude=('tests')),
      author_email='veenrokdalv@gmail.com',
      zip_safe=False,
      install_requires=['aiohttp>=3.7.2,<4.0.0'],
      )