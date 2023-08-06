from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

# Consider https://packaging.python.org/tutorials/packaging-projects/

setup(
    name='autoconfsh',  # Required
    version='0.0.1',  # Required
    description='Autoconf.sh - the lazy mans bootstrapper for Arch Linux',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/jakeobsen/autoconf.sh',  # Optional
    author='Morten Jakeobsen',  # Optional
    author_email='morten@jakeobsen.com',  # Optional
    classifiers=[  # Optional
        'Development Status :: 3 - Alpha',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Installation/Setup',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='arch, linux, bootstrap, bootstrapping, arch linux, installer, install, automate, automation',  # Optional
    package_dir={'': 'src'},  # Optional
    packages=find_packages(where='src'),  # Required
    python_requires='>=3.9, <4',
    entry_points={  # Optional
        'console_scripts': [
            'autoconf.sh = autoconfsh.cli:cli_entrypoint',
        ],
    },
    project_urls={  # Optional
        'Bug Reports': 'https://github.com/jakeobsen/autoconf.sh/issues',
        'Source': 'https://github.com/jakeobsen/autoconf.sh',
    },
)