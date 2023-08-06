import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mytosex",
    version="0.1",
    author="Manuel Mendoza",
    author_email="manuelmendoza@uvigo.gal",
    description="Sexual inference based on mitochondrial genome content",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/manuelsmendoza/mytosex",
    project_urls={
        "Bug Tracker": "https://github.com/manuelsmendoza/mytosex/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
