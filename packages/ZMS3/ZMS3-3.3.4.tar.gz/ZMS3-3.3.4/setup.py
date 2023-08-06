import os
from setuptools import setup

HERE = os.path.abspath(os.path.dirname(__file__))


def _read_file(filename):
    with open(os.path.join(HERE, filename)) as f:
        return f.read()


README = _read_file('README.rst')
CHANGES = _read_file('CHANGES.rst')


version = '3.3.4'

setup(
    name='ZMS3',
    description='ZMS: Simplified Content Modelling',
    long_description="\n\n".join([README, CHANGES]),
    version=version,
    author='HOFFMANN+LIEBENBERG in association with SNTL Publishing, Berlin',
    author_email='zms@sntl-publishing.com',
    url='http://www.zms-publishing.com',
    download_url='https://github.com/zms-publishing/ZMS3',
    license='GPLv2',
    keywords="zope zms cms content management system meta",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Framework :: Zope2',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Customer Service',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Telecommunications Industry',
        'Intended Audience :: Financial and Insurance Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
    ],
    zip_safe=False,
    install_requires=[
        'ZMS<4',
    ],
)
