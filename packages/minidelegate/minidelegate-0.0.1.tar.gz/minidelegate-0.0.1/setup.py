from setuptools import setup


def readme():
    with open("README.rst") as f:
        return f.read()


setup(
    name="minidelegate",
    version="0.0.1",
    description="Package for delegate based methods via decorators",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="developer delegate helpers decorators",
    url="https://github.com/BhMbOb/Py-Delegate",
    author="Bailey3D",
    author_email="contact@bailey3d.com",
    license="MIT",
    packages=["delegate"],
    install_requires=[],
    include_package_data=True,
    zip_safe=False
)
