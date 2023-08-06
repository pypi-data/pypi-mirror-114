import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="thonny-etboard-micropython-firmware",
    version="0.0.1",
    author="KETRi",
    author_email="ketri3000@gmail.com",
    description="ET보드 마이크로파이썬 펌웨어",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://et.ketri.re.kr/",
    project_urls={
        "Bug Tracker": "http://et.ketri.re.kr/",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["thonnycontrib.thonny_etboard_firmware"],
    package_data={"thonnycontrib.thonny_etboard_firmware" : ["*", "*/*", "*/*/*", "*/*/*/*", "*/*/*/*/*"]},
    install_requires = ["thonny>=3.3.11"],
    python_requires=">=3.6",
)