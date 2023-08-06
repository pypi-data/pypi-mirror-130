import setuptools

# Load README
with open('README.md', 'r', encoding='utf8') as file:
    long_description = file.read()

# Define package metadata
setuptools.setup(
    name='sitzungsdienst',
    version='1.5.3',
    author='Martin Folkers',
    author_email='hello@twobrain.io',
    description='A simple Python utility for converting the weekly assignment PDF by the "Staatsanwaltschaft Freiburg"',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://codeberg.org/S1SYPHOS/sitzungsdienst',
    license='MIT',
    project_urls={
        'Issues': 'https://codeberg.org/S1SYPHOS/sitzungsdienst/issues',
    },
    entry_points='''
        [console_scripts]
        sta=sitzungsdienst.cli:cli
    ''',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=setuptools.find_packages(),
    install_requires=[
        'backports.zoneinfo',
        'click',
        'ics',
        'pandas',
        'pypdf2',
    ],
    python_requires='>=3.6',
)
