from setuptools import setup, find_packages
import sys

with open('requirements.txt') as f:
    reqs = f.read()

reqs = reqs.strip().split('\n')

install = [req for req in reqs if not req.startswith("git+git://")]
depends = [req.replace("git+git://", "git+http://") for req in reqs if req.startswith("git+git://")]

setup(
    name='fever-allennlp',
    version='0.0.5',
    author='James Thorne',
    author_email='james@jamesthorne.co.uk',
    url='https://jamesthorne.co.uk',
    description='Fact Extraction and VERification experiments built on AllenNLP',
    long_description="readme",
    license=license,
    python_requires='>=3.6',
    package_dir={'fever': 'src/fever',
                 'fever.submission': 'src/fever/submission',
                 'fever.evidence':'src/fever/evidence'},
    packages=['fever',
              'fever.submission',
              'fever.evidence'
              ],
    install_requires=install,
    dependency_links=depends,

)
