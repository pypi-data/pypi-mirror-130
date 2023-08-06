import setuptools

with open("README.md", "r", encoding="utf-8") as fhdlr:
    long_description = fhdlr.read()

setuptools.setup(
    name="datalines",
    version="0.0.1",
    author="TheProjectsGuy",
    author_email="vdd29rjre@mozmail.com",
    description="Datalines = Dataloaders + Pipelines, add simplicity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TheProjectsGuy/DataLines",
    project_urls={
        "Bug Tracker": "https://github.com/TheProjectsGuy/DataLines/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
