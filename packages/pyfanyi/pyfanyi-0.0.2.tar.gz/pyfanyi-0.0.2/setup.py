from distutils.core import setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='pyfanyi',
    version='0.0.2',
    description='Translate every string. It is very good.',
    author='stripe-python',
    author_email='13513519246@139.com',
    py_modules=['pyfanyi'],
    long_description=long_description,
)
