import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vmhub3",
    version="1.0.1",
    author="rpcsp",
    author_email="pcunha@hotmail.com",
    description="python module to send instructions to VM Hub 3 routers",
    license="https://github.com/rpcsp/vmhub3/blob/main/LICENSE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rpcsp/vmhub3",
    project_urls={
        "Project page": "https://github.com/rpcsp/vmhub3",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "xmltodict",
    ],
    tests_require=[
        "pytest",
        "pytest-cov",
        "pytest-flake8",
    ],
    entry_points="""\
    [console_scripts]
    vmhub3 = vmhub3.vmhub3:main
    """
)
