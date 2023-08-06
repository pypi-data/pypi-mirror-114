import setuptools

with open("C:/Users/Lenovo/Documents/container2/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AmoghPasswordChecker",
    version="0.0.3",
    author="Amogh Jhamb",
    author_email="amogh100109@gmail.com",
    description="Password validator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ammo78/AmoghPasswordChecker",
    project_urls={
        "Bug Tracker": "https://github.com/Ammo78/AmoghPasswordChecker/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "AmoghPasswordChecker"},
    packages=setuptools.find_packages(where="AmoghPasswordChecker"),
    python_requires=">=3.6",
)
