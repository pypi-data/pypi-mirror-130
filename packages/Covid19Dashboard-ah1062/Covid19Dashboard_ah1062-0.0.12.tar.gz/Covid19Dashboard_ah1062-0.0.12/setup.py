import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Covid19Dashboard_ah1062",
    version="0.0.12",
    author="Alex Houghton",
    author_email="ah1062@exeter.ac.uk",
    description="Covid-19 Data Presentation Dashboard, ECM1400 Programming Coursework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ah1062/Covid19Dashboard",
    packages=['Covid19Dashboard_ah1062'],
    package_data={
        'Covid19Dashboard_ah1062': [
            "*.json",
            "templates/*.*",
            "templates/index_files/*.*",
            "CSV Data Files/*.*"
        ]
    },
    include_package_data=True,
    classifiers=[

    ],
    python_requires=">=3.9"
)
