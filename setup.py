from setuptools import setup

config = {

    'name': 'puzzlepy',
    'version': '0.1.2',
    'author': 'B.A. van den Berg',
    'author_email': 'b.a.vandenberg@gmail.com',
    'url': 'https://github.com/basvandenberg/puzzlepy',
    'description': 'Python package for generating, solving, and testing grid-based puzzle games.',
    'download_url': 'https://github.com/basvandenberg/puzzlepy/releases',
    'license': 'MIT',
    'packages': ['puzzlepy'],
    'classifiers': [
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Games/Entertainment :: Puzzle Games',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    'scripts': ['bin/sudoku']
}

setup(**config)
