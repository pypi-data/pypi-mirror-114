import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dsa-package-data-structures",
    version="0.0.5",
    author="VivinMeth",
    author_email="vivinmeth@gmail.com",
    description="Data Structures [for Python]",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="BSD-3-Clause",
    url="https://gitlab.com/dsa-package/data-structures/python/-/wikis/home",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    project_urls={
        'Documentation': 'https://gitlab.com/dsa-package/data-structures/python/-/wikis',
        'Source': 'https://github.com/dsa-package/data-structures-python',
        'Tracker': 'https://gitlab.com/dsa-package/data-structures/python/-/issues',
    },
)