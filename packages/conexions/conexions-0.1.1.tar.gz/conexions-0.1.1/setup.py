import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="conexions",
    version="0.1.1",
    author="Ran#",
    author_email="ran-n@tutanota.com",
    description="Módulo para disttintos tipos de conexión en python como proxies ou tor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ran-n/conexions",
    project_urls={
        "Bug Tracker": "https://github.com/ran-n/conexions/issues",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
