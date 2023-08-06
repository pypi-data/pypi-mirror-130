import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name='c_log',
    version='0.0.3',
    author='Andrey Bolshakov',
    author_email='andrey.bolshakov@accenture.com',
    description='Colored logger',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    python_requires='>=3.8',
)
