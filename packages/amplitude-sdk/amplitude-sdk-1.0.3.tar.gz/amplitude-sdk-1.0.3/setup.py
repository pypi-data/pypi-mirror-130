from setuptools import find_packages
from distutils.core import setup

with open('README.rst') as file:
    long_description = file.read()

setup(
    name='amplitude-sdk',
    version='1.0.3',
    description='Amplitude Python 3 SDK.',
    packages=find_packages(),
    keywords=(
        'amplitude sdk Amplitude v2  bahav HTTP api V2 '
        'Batch Event Upload  Identify  Attribution '
        ' Behavioral Cohorts  Chart Annotations '
        ' Dashboard REST  Export  '
        'Group Identify  Releases  '
        'SCIM  Taxonomy  '
        'User Privacy  User Profile '),
    install_requires=[],
    url='https://github.com/paulokuong/amplitude',
    author='Paulo Kuong',
    license='MIT',
    tests_require=['pytest', 'pytest-cov'],
    long_description=long_description,
    include_package_data=True,
    zip_safe=False,
)
