from distutils.core import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst', format='md')
except ImportError:
    #print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='kping',
    version='0.1.0',
    author='Kenneth Burgener',
    author_email='kenneth@oeey.com',
    scripts=['bin/kping'],
    packages=['kping'],
    url='https://pypi.python.org/pypi/kping/',
    license='LICENSE.txt',
    description='Simple visual Ping',
    long_description=read_md('README'),
)
