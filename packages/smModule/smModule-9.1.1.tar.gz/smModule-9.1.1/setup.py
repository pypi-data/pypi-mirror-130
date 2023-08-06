import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="smModule",
    version="9.1.1",
    author="Pascal Vallaster",
    author_email="pascalvallaster@gmail.com",
    description="Doc for module is now in the module itself",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="sm/src"),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["sm"],
    package_dir={'': 'sm/src'},
)
