from setuptools import setup


def readme_file():
    with open("README.rst", encoding="utf-8") as rf:
        return rf.read()


setup(name="sztestlib20210724",
      version="1.0.0",
      description="this is a niubi lib",
      long_description=readme_file(),
      packages=["sztestlib"],
      py_modules="Tool",
      author="Sz",
      author_email="maweiustb@163.com",
      url="https://github.com/pypa/sampleproject",
      license="MIT")
