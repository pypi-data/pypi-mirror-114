from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='modelzoo_iitm',
    version = '0.0.1',
    description = 'Model Zoo by IIT Madras',
    py_modules = ["modelzoo_iitm"],
    package_dir = {'': 'src'},
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires = [
        "elasticdeform ~= 0.4.9",
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    },
    url = "https://github.com/Vinayak-VG/ModelZoo_PyPi",
    author = "Vinayak-VG",
    author_email = "vinayakguptapokal@gmail.com",
    long_description = long_description,
    long_description_content_type = "text/markdown",
)