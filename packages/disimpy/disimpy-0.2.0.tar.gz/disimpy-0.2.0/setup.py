from setuptools import setup

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="disimpy",
    version="0.2.0",
    description="Massively parallel diffusion MR simulator",
    long_description=long_description,
    url="https://github.com/kerkelae/disimpy",
    author="Leevi Kerkelä",
    author_email="leevi.kerkela@protonmail.com",
    license="MIT",
    packages=["disimpy", "disimpy.tests"],
    install_requires=["matplotlib", "numba", "numpy", "pytest"],
    include_package_data=True,
    package_data={"": ["requirements.txt", "license.txt", "tests/*"]},
)
