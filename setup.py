from setuptools import setup, find_packages

setup(
    name='raspyrfm_client',
    version='1.0.0',
    description='A library to send rc signals with the RaspyRFM module',
    license='GPLv3+',
    author='Markus Ressel',
    author_email='mail@markusressel.de',
    url='https://www.markusressel.de',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
    ],
    install_requires=[
    ],
    tests_require=[
        'rstr'
    ]
)
