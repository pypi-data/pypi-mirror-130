import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='micro_cata',
    version='0.0.1',
    author='Andres Rodriguez and Adiel Perez',
    author_email='amrodrig@caltech.edu',
    description='Package that will help us analyze microtuble catastrophe data.',
   # long_description=long_description,
   # long_description_content_type='markdown',
    packages=setuptools.find_packages(),
    install_requires=["numpy","pandas","bokeh>=1.4.0"],
    classifiers=(
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ),
)