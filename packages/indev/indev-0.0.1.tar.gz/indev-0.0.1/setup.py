from setuptools import setup


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="indev",
    version="0.0.1",
    description="Package containing some basic developer helpers",
    long_description=readme(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="developer indev helpers todo decorators",
    url="https://github.com/BhMbOb/Py-InDev",
    author="Bailey3D",
    author_email="contact@bailey3d.com",
    license="MIT",
    packages=["indev"],
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
