import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="autoviz",
    version="0.1.24",
    author="Ram Seshadri",
    # author_email="author@example.com",
    description="Automatically Visualize any dataset, any size with a single line of code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='Apache License 2.0',
    url="https://github.com/AutoViML/AutoViz",
    packages=setuptools.find_packages(exclude=("tests",)),
    install_requires=[
        "ipython",
        "jupyter",
        "xlrd",
        "wordcloud",
        "pandas",
        "matplotlib",
        "seaborn",
        "scikit-learn",
        "statsmodels",
        "holoviews",
        "hvplot",
        "bokeh>=2.4.0",
        "xgboost",
        "fsspec>=0.3.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
