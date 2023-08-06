from platformer import __version__
from setuptools import setup, find_packages

setup(
    name='platformer-iac',
    version=__version__,
    description='Platform generation tool based on terraform and git',
    license='MIT',
    author="Rafael F. Sant'Anna",
    author_email="rafaelsantanna@outlook.com",
    url='https://github.com/rfsantanna/platformer',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'pyyaml',
        'jinja2'
    ],
    entry_points={
        'console_scripts': [
            'platformer = platformer.cli:cli',
            'pf = platformer.cli:cli'
        ]
    }
)
