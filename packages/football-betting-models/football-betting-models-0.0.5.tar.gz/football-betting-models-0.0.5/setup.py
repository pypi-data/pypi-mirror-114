from setuptools import setup
from setuptools import find_packages


with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='football-betting-models',
    version='0.0.5',
    author='MikeyJW',
    author_email='michael.watson@whoknowswins.com',
    description='Seeding models package',
    url='https://github.com/MikeyJW/football_betting_models',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    #package_dir={'': 'betting_models'},
    packages=find_packages(),   # What the fuck is going on here? Check others examples.
    install_requires=[
        'numpy==1.20.3',
        'scipy==1.6.2',
        'matplotlib==3.3.4',
        'seaborn==0.11.1',
        'pandas==1.2.5'
    ],
    python_requires='>=3.8'
)
