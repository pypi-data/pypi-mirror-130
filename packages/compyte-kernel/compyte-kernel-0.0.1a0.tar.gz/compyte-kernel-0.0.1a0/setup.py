import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="compyte-kernel",
    version="0.0.1-alpha",
    author="AutomaCoin Devs",
    author_email="alessio.proietti@protonmail.com",
    description="A compute kernel",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/automacoin/compyte-kernel",
    project_urls={
        "Bug Tracker": "https://github.com/automacoin/compyte-kernel/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)