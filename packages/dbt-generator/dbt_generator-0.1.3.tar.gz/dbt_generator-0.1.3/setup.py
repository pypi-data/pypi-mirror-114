from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name = 'dbt_generator',
    version = '0.1.3',
    author = 'Tuan Nguyen',
    author_email = 'anhtuan.nguyen@me.com',
    url = 'https://github.com/tuanchris/dbt-generator',
    description = 'Generate and process base models for dbt',
    license ='MIT',
    packages = find_packages(),
    entry_points = {
        'console_scripts': [
            'dbt-generator = dbt_generator.dbt_generator:dbt_generator',
        ]
    },
    classifiers =(
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
    ),
    keywords ='dbt python package base models',
    install_requires=requirements,
    zip_safe = False
    )
