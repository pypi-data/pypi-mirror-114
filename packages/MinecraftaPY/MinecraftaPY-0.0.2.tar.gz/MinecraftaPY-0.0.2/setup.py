import setuptools


setuptools.setup(
    name="MinecraftaPY",
    version="0.0.2",
    author="ThisIsanAlt",
    description="Simple wrapper for Hypixel and Mojang's APIs. WIP, very unstable!",
    url="https://github.com/ThisIsanAlt/MinecraftaPY",
    project_urls={
        "Bug Tracker": "https://github.com/ThisIsanAlt/MinecraftaPY/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)