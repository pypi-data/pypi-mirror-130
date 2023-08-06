from setuptools import setup, find_packages

VERSION = '0.0.21'
DESCRIPTION = 'simple Huffman encoder'
LONG_DESCRIPTION = 'A simple package that allows you to perform Huffman coding on user input strings.'

# Setting up
setup(
    name="HuffmanCoder",
    version=VERSION,
    author="Shikhar Sahu",
    author_email="<shikharsahu76@gmail.com>",
    description=DESCRIPTION,
    url="https://github.com/ShikharSahu/HuffmanCoder",
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'huffman', 'encoding', 'decoding', 'data', 'compression'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)