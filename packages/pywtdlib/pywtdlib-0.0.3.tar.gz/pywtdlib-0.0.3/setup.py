import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setuptools.setup(
    name="pywtdlib",
    version="0.0.3",
    author="alvhix",
    author_email="alvhix@gmail.com",
    description="A simple Python TDLib wrapper",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alvhix/pywtdlib",
    project_urls={
        "Bug Tracker": "https://github.com/alvhix/pywtdlib/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    install_requires=["python-dotenv"],
    python_requires=">=3.6",
)
