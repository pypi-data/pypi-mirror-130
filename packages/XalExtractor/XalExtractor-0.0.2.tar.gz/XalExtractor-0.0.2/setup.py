import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="XalExtractor",
    version="0.0.2",
    author="Diego Ramírez",
    author_email="diego.ramirez@xaldigital.com",
    description="servicios para extractores",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['py4j', 'pyspark'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)