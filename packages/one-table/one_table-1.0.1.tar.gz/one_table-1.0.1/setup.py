from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Python dynamoDB one table'
LONG_DESCRIPTION = 'Python dynamoDB one table'

setup(
    name="one_table",
    version=VERSION,
    author="Gerswin Pineda",
    author_email="g3rswin@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["cerberus"],
    requires_python='>=3.6',
    keywords=['python', 'dynamodb'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Developers',
        "Programming Language :: Python :: 3",
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License'
    ]
)