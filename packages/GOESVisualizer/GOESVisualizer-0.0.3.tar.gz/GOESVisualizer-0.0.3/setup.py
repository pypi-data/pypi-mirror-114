from setuptools import setup,find_packages
from os.path import splitext
from os.path import basename
from glob import glob


with open('README.md') as f:
    readme = f.read()

setup(name='GOESVisualizer',
      version='0.0.3',
      description='A simple tool to visualize GOES16/17',
      long_description=readme,
      long_description_content_type='text/markdown',
      author='Amir Souri',
      author_email='ahsouri@gmail.com',
      license='MIT',
      packages=['GOESVisualizer'],
      install_requires=[
          'numpy','matplotlib','xarray','netCDF4','opencv-python','datetime','metpy','boto3','requests','botocore','cartopy'
      ],
      zip_safe=False)
