"""Setup."""

from codecs import open
from os.path import abspath, dirname, join
from subprocess import call
from setuptools import Command, find_packages, setup
from sked import __version__

this_dir = abspath(dirname(__file__))
with open(join(this_dir, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()


class RunTests(Command):
    """Run all tests."""
    description = 'run tests'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        """Run all tests!"""
        errno = call(['py.test', '--cov=sked', '--cov-report=term-missing'])
        raise SystemExit(errno)

def readme():
    with open("README.rst") as f:
        return f.read()
setup(
    name='sked',
    version=__version__,
    description='CLI utility to create AWS Scheduled Actions using instance tags or autoscaling id via a config file',
    long_description=readme(),
    url='https://github.com/niklongstone/sked',
    author='Nicola Pietroluongo',
    author_email='nik.longstone@gmail.com',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    keywords='cli, aws, scaling, auto scaling group, scheduled actions',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=['docopt', 'boto3', 'PyYAML'],
    extras_require={
        ':python_version in "2.6, 2.7"': ['mock'],
        'test': ['coverage', 'pytest', 'pytest-cov', 'tox'],
    },
    entry_points={
        'console_scripts': [
            'sked=sked.cli:main',
        ],
    },
    cmdclass={'test': RunTests},
)
