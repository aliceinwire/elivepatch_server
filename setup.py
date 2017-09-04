from setuptools import setup, find_packages

setup(
    name='elivepatch_server',
    version='0.01',
    description='Distributed elivepatch server API',
    url='https://wiki.gentoo.org/wiki/Elivepatch, ' + \
        'https://github.com/aliceinwire/elivepatch-server',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: System :: Operating System Kernels',
    ],

    author='Alice Ferrazzi',
    author_email='alice.ferrazzi@gmail.com',
    license='GNU GPLv2+',
    packages=['elivepatch_server','elivepatch_server.resources'],
    scripts=['elivepatch_server/elivepatch-server'],
)
