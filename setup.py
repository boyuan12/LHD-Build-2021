from setuptools import setup

setup(
    author="Boyuan Liu",
    author_email="boyuanliu6@yahoo.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Utilities"
    ],
    description="This is a simple CLI for uploading file to Google Drive",
    license="MIT",
    install_requires=["google-api-python-client==1.12.8", "google-auth-httplib2==0.0.4", "google-auth-oauthlib==0.4.2"],
    keywords=["google", "drive", "upload", "cli"],
    name="GDriveCLI",
    packages=["GoogleDriveCLI"],
    python_requires=">= 3.6",
    entry_points={
        "console_scripts": ["google-drive=GoogleDriveCLI.cli:cli"]
    },
    url="https://github.com/boyuan12/LHD-Build-2021",
    version="0.0.3",
    include_package_data=True
)