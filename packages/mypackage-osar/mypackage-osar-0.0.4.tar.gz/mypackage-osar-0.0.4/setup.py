import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mypackage-osar", # Replace with your own username
    version="0.0.4",
    author="Buzovskyi Vitalii",
    author_email="buzovskiy.v@gmail.com",
    description="test mypackage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    python_requires='>=3.8',
    install_requires=[],
)