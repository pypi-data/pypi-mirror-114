from setuptools import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='exchangelib_listener',
    version='1.1.1',
    author='Evan Brown',
    author_email='evan.brown@ttigroupna.com',
    description='Simple inbox event listener for exchangelib.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/evan_brown/exchangelib-listener',
    packages=['exchangelib_listener'],
    install_requires=['exchangelib==4.4.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Intended Audience :: Developers"
    ],
    python_requires='>=3.8'
)
