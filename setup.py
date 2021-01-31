from setuptools import setup, find_packages


def readme():
   with open('README.md', 'r', encoding='utf-8') as f:
       return f.read()


setup(
    name='treebuilder',
    author='Fabien Dieulle',
    author_email='fabiendieulle@hotmail.fr',
    description='Build tree data model.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/fdieulle/treebuilder',
    packages=find_packages(),
    install_requires=['sly'],
    zip_safe=False,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    use_scm_version=True,
    setup_requires=['setuptools_scm']
)