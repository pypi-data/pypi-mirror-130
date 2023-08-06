import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="GSKhopt",
    version="0.0.6",
    author="Hazem Nomer",
    author_email="h.nomer@nu.edu.eg",
    description="GSK algorithm for efficient hyperparameter optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ha2emnomer/GSKHpot/",
    project_urls={
        "Bug Tracker": "https://github.com/ha2emnomer/GSKHpot/issues",
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
