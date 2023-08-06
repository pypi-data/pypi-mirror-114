import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mahabharata",
    version="0.1.0",
    author="Sharlon Regales",
    author_email="sharlon.regales@tno.nl",
    description="Mahabharata poem query cli",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "click",
        "pydantic",
    ],
    entry_points={
        "console_scripts": [
            "mahabharata=mahabharata.services.cli_service.group:cli",
        ],
    },
    python_requires=">=3.8",
)
