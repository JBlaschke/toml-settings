from setuptools import setup, find_packages


if __name__ == "__main__":

    with open("README.md", "r") as fh:
        long_description = fh.read()

    setup(
        name="TOML-Settings",
        version="0.1.0",
        author="Johannes Blaschke",
        author_email="johannes@blaschke.science",
        description="Create global settings contexts from a TOML file",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/JBlaschke/toml-settings",
        packages=find_packages(),
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
        install_requires=[
          "toml",
          "simple-singleton>=1.5.1",
          "msgspec>=0.9.0"
        ],
    )