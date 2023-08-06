from setuptools import setup

setup(
    name='excel2xx',
    version='0.5.0',
    packages=['excel2xx'],
    url='https://github.com/cupen/excel2xx',
    license='WTFPL',
    author='cupen',
    author_email='xcupen@gmail.com',
    description='Extract data from excel file, and export to json, msgpack, or any code(mako template).',
    install_requires=[
        'xlrd == 2.0.*',
        'docopt >= 0.6.0',
        'mako >= 1.0.0',
        'msgpack-python >= 0.4.8'
    ],
    entry_points={
       'console_scripts': [
           'excel2xx=excel2xx.main:main_docopt',
       ],
    },
    python_requires='>=3.6.*,!=3.6.1',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
