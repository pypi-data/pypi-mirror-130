import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="latestearthquakenewsindonesia",
    version="0.5",
    author="Firman Arya P",
    author_email="firmanap22@gmail.com",
    description="his package will get the latest earthquake news from Indonesia BMKG Meteorological, "
                "Climatological And Geophysical Agency",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jakarta-remote-work/Latest-Earthquake-News",
    project_urls={

    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable"
    ],
    # package_dir={"": "src"},
    # packages=setuptools.find_packages(where=""),
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
)

