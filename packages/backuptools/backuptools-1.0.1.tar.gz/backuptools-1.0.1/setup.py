import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = [
    "google-api-python-client>=2.15.0",
    "google-auth-httplib2>=0.1.0",
    "python-magic>=0.4.10",
    "checksumdir>=1.2.0",
    "click"
]

setuptools.setup(
    name="backuptools",
    version="1.0.1",
    author="hieunv495",
    author_email="hieunv495@gmail.com",
    description="Backup, restore, version control local data to google drive",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hieunv495/backuptools",
    project_urls={
        "Bug Tracker": "https://github.com/hieunv495/backuptools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    # packages=['backuptools'],
    python_requires=">=3.6",
    install_requires=install_requires,
    entry_points={
        "console_scripts": [
            'backuptools=backuptools:cli'
        ]
    }
)
