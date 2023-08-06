from setuptools import setup, find_packages

setup(
    name='BlizzOAuth',
    version='0.1.0',
    description='A simply OAuth token generator for your Blizzard API apps',
    url='https://github.com/jacobwdheath/blizz-py-auth.git',
    author='Jacob Heath',
    author_email='Jacobwdheath@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=['Development Status :: 4 - Beta',
                 'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                 'Programming Language :: Python',
    ],
    )
    