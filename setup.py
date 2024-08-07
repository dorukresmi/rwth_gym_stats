from setuptools import setup, find_packages

def parse_requirements(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file if line.strip() and not line.startswith('#')]

setup(
    name='rwth_gym_stats',
    version='0.1.0',
    author='Doruk Resmi',
    author_email='dorukresmi@gmail.com',
    description='A package for tracking rwth gym visitor statistics, with scheduling and visitor counting functionality.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/dorukresmi/rwth_gym_stats',
    packages=find_packages(),
    install_requires=parse_requirements('requirements.txt'),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',
    entry_points={
        'console_scripts': [
            'gym_stats=gym_stats.main:main',
        ],
    },
    include_package_data=True,
    package_data={
        '': ['*.txt', '*.md'],
    },
)