import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="treads",
    version="1.0.1",
    author="Pouria Kourehpaz",
    author_email="pouria.kourehpaz@ubc.ca",
    description="Tool for Recovery Estimation And Downtime Simulation of buildings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/carlosmolinahutt/treads",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering',
    ],
    python_requires='>=3.6',
)