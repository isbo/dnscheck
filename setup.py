from setuptools import setup

__version__ = '0.1'

setup(name='dnscheck',
    version=__version__,
    description='A CLI tool to check Amazon Route 53 DNS configuration',
    license='MIT',
    author='Imran Patel',
    author_email='aesboe@gmail.com',
    url='http://loads.pickle.me.uk/cli53/',
    install_requires=['boto', 'dnspython'],
    scripts=['scripts/dnscheck'],
)