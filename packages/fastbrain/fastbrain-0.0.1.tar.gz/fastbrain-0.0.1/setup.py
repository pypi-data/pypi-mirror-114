import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastbrain",
    version="0.0.1",
    author="Baihan Lin",
    author_email="doerlbh@gmail.com",
    description="Python library of of jax-based representational studies in neuroscience and deep learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/doerlbh/fastbrain",
    project_urls={
        "Bug Tracker": "https://github.com/doerlbh/fastbrain/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    license="GPLv3",
    package_dir={"": "fastbrain"},
    packages=setuptools.find_packages(where="fastbrain"),
    python_requires=">=3.6",
    install_requires=["jax", "numpy>=1.16.5", "pandas"],
    test_suite="nose.collector",
    tests_require=["nose"],
    include_package_data=True,
)
