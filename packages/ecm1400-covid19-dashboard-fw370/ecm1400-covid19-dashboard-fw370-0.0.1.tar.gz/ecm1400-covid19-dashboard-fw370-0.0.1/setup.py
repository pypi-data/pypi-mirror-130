import setuptools
with open("README.md", "r") as readme:
    long_description = readme.read()

setuptools.setup(
    name="ecm1400-covid19-dashboard-fw370",
    version="0.0.1",
    author="Frederick Westhead",
    author_email="fw370@exeter.ac.uk",
    description="Local hosted webpage displaying a Covid-19 dashboard for ECM1400 Programming Continuous Assesment",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fw370/ecm1400-covid-dashboard-fw370",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
    