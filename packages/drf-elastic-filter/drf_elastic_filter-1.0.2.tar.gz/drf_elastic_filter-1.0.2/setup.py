import setuptools

setuptools.setup(
    name="drf_elastic_filter",
    version="1.0.2",
    author="Saeed Hassani Borzadaran",
    author_email="hassanisaeed19@gmail.com",
    description="DRF Elastic Filter for Models",
    long_description_content_type="text/markdown",
    url="https://github.com/realsaeedhassani/drf_elastic_filter",
    project_urls={
        "Bug Tracker": "https://github.com/realsaeedhassani/drf_elastic_filter/issues/new",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
