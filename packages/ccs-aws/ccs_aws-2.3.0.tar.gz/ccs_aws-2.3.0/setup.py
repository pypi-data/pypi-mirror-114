import setuptools

setuptools.setup(
    name="ccs_aws",
    version="2.3.0",
    author="code_duck",
    description="ccs aws modules",
    long_description_content_type="text/markdown",
    install_requires=['boto3'],
    package_dir={"ccs_aws": "ccs_aws"},
    packages=['ccs_aws'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)