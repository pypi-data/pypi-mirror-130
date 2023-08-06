import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='covid-dashboard-jadam',
    version='0.0.1',
    author='James Adam',
    author_email='ja669@exeter.ac.uk',
    description='A dashboard to display up to date covid data and news',
    long_description=long_description,
    packages=setuptools.find_packages(),
    python_requires='>=3.9'
)
