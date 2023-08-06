import setuptools

setuptools.setup(
    name="shypdf",
    version=1.0,
    long_description="",
    packages=setuptools.find_packages(exclude=["tests","data"])
)

# python3 setup.py sdist bdist_wheel
