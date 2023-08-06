from distutils.core import setup

setup(
    name='mmparse',
    version='0.5',
    description='Parse Matrix Market Files',
    author='Michel Pelletier',
    author_email='michel@graphegon.com',
    url='https://github.com/michelp/mmparse',
    packages=['mmparse'],
    tests_require=["pytest"],
)
