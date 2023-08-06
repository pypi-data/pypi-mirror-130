import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

SRC = 'src'
setuptools.setup(
    name="changefinderPRO",
    version="0.0.2",
    author="Dheiver Santos",
    author_email="dheiver.santos@gmail.com",
    description="Detection of change points is useful in modelling and prediction of time series ",
    long_description=long_description,
    package_dir={'': SRC},
    long_description_content_type="text/markdown",
    url="https://.....",
    packages=setuptools.find_packages(SRC),
    include_package_data = True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'pandas',
          'rrcf',
          'sklearn',
          'idfops'
      ],
    python_requires='>=3.6',
)
