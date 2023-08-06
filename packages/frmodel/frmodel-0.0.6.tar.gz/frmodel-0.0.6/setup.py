import setuptools

from Cython.Build import cythonize
import numpy as np

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="frmodel",
    version="0.0.6",
    author="Eve-ning",
    author_email="dev_evening@hotmail.com",
    description="The base package to support frmodel data processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Eve-ning/frmodel",
    packages=setuptools.find_packages(),
    ext_modules=cythonize(["frmodel/base/D2/frame/glcm2.pyx"]),
    include_dirs=np.get_include(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7'
)

