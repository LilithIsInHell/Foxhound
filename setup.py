from setuptools import setup, find_packages

setup(
    name='foxhound-recon',
    version='1.0.0',
    description='Pentesting Recon Automation Tool',
    author='Lilith',
    author_email='',
    packages=find_packages(),
    install_requires=[
        'colorama',
        
    ],
    entry_points={
        'console_scripts': [
            'foxhound=foxhound.main:main',  # points to foxhound/main.py main() function
        ],
    },
    python_requires='>=3.7',
)