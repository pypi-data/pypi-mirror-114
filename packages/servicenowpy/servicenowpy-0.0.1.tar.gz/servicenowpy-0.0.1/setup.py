from setuptools import setup, find_packages

long_description = open("README.md", encoding="utf-8").read()

classifiers=[
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9"
]

# This call to setup() does all the work
setup(
    name="servicenowpy",
    version="0.0.1",
    description="ServiceNow's Table API, easily.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://servicenowpy.readthedocs.io/",
    author="Henrique Santos",
    author_email="henrique.nsantos@outlook.com",
    license="MIT",
    classifiers=classifiers,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=["requests"]
)