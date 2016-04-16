
try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages


def read(relative):
    """
    Read file contents and return a list of lines.
    ie, read the VERSION file
    """
    contents = open(relative, 'r').read()
    return [l for l in contents.split('\n') if l != '']

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='viprobto',
    url='',
    keywords=['vipr'],
    long_description=readme,
    version=read('VERSION')[0],
    description='A quick way to do your implementation',
    author='Adel Zaalouk',
    author_email='adel.zalok@emc.com',
    install_requires=read('./requirements.txt'),
    include_package_data=True,
    packages=find_packages(exclude=['ez_setup'])
)