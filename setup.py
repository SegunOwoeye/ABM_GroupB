from setuptools import setup, find_packages

setup(
    name="KCL_ABM-GroupB",  # Replace with your project name
    version="1.0",
    packages=find_packages(),  # Automatically find all subpackages
    include_package_data=True,  # Include non-code files specified in MANIFEST.in
    install_requires=[
        "requests",
        "pandas",
        "openpyxl",
        "mesa",
        "numpy",
        "networkx",
        "matplotlib",
        "altair",
        "solara"
    ],  # Add any dependencies here 
)