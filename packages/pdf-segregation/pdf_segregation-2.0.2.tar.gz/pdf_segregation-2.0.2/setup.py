from setuptools import setup

VERSION = '2.0.2'
DESCRIPTION = 'This module will return whether PDF is Digital, Non-Digital or Mixed.'

# Setting up
setup(
    name="pdf_segregation",
    version=VERSION,
    author="Kishan Tongrao",
    author_email="kishan.tongs@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=['pdf_segregation'],
    include_package_data=True,
    install_requires=['PyPDF2'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    long_description = """
    ```
    # After installation use syntax :
    
    ## Load library
    #
    from pdf_segregation import pdf_classifier
    
    result, digital_pages, nondigital_pages = pdf_classifier.digital_nondigital_classifier("scansmpl.pdf")
    #scansmpl.pdf replace with your file name.
    
    print(result)
    print(digital_pages)
    print(nondigital_pages)

    # result - Digital, Non-Digital or Mixed based on document.
    # digital_pages - Page numbers which are digital.
    # nondigital_pages - Page numbers which are nondigital.
    
    ```

    Thanks and Enjoy !!!

    """

)