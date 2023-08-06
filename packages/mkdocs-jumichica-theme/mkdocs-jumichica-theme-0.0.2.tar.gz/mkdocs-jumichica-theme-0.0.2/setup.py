from setuptools import setup, find_packages

VERSION = '0.0.2'

setup(
    name="mkdocs-jumichica-theme",
    version=VERSION,
    url='https://github.com/jumichica/mkdocs-jumichica-theme',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Topic :: Documentation',
        'Topic :: Text Processing',
    ],
    install_requires=[
        'mkdocs',
    ],
    license='BSD',
    description='Jumíchica theme for MkDocs.',
    author='Edwin Ariza',
    author_email='me@edwinariza.com',
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'mkdocs.themes': [
            'jumichica = jumichica',
        ]
    },
    zip_safe=False
)
