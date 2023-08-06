from setuptools import setup, find_packages

with open('README.rst','r') as f:
    long_desc = f.read()
setup(
    name='wikitable',
    version='0.0.1',
    description='Converts Wikipedia tables to dataframes and CSVs',
    pymodules=['wikitable'],
    package_dir={'':'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'requests',
        'pandas',
        'beautifulsoup4'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',],
        long_description = long_desc,
        long_description_content_type = 'text/x-rst',
        url = 'https://github.com/jaredmeyers/wikitable',
        author = 'Jared Meyers',
        author_email = 'jaredehren@verizon.net',
        )
