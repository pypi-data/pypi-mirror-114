import setuptools 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name = 'pySimpleCalculator',
    version = '0.0.1',
    author = "Blessing .O. Agadagba",
    author_email ="agadagbablessing@gmail.com",
    description = "A simple calculator for arithmetic operations in python",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sherlocked-Blaire/PySimpleCalculator.git",
    project_urls={
        "Bug Tracker": "https://github.com/Sherlocked-Blaire/PySimpleCalculator/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["SimpleCalculator"],
    package_dir = {"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)   
