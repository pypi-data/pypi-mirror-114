import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shinc-lib-sofs",
    version="7.0.0",
    author="William Greenly",
    author_email="william_greenly@hotmail.com",
    description="SOF interpreter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    tests_require=['unittest'],
    test_suite="test",
    packages=setuptools.find_packages(),
    include_package_data = True,
    install_requires=[
        'pytesseract','twine','Pillow','PyPDF2','rdflib','pdfplumber','python-dateutil','dateparser'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)