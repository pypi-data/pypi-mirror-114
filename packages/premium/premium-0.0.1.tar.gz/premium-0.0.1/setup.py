import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="premium",
    version="0.0.1",
    author="slipper",
    author_email="byteleap@gmail.com",
    description="Sound processing toolkit with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GaoangLiu/psox",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={
     # And include any *.msg files found in the "hello" package, too:
        "psox": ['data/*.txt', 'data/*.pickle', 'data/*.mp3', 'data/*.wav'],
    },
    install_requires=['smart-open'],
    entry_points={
        'console_scripts': ['demo=psox.demo:entry', 'zz=psox.zz:main'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
