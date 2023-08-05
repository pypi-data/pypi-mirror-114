from setuptools import setup, find_packages


with open("README.rst", "r", encoding = "utf8") as f:
    long_description = f.read()

setup(
    name = "pylogpro",
    version = "0.0.4",
    author = "31core",
    author_email = "zero.mail@foxmail.com",
    description = "pylogpro - 更加简洁的python日志记录工具",
    long_description = long_description,
    license = "Mit License",
    license_file = "LICENSE",
    packages = find_packages()
)
