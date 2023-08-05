import setuptools

long_description = open("README.md", "r", encoding="utf-8").read()

setuptools.setup(
    name="GeoSnipe",
    version="1.1.3",
    author="Geographs",
    maintainer="Geographs",
    author_email="87452561+Geographs@users.noreply.github.com",
    description="A pythonic Minecraft username sniper based on asyncio.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Geographs/GeoSnipe",
    download_url="https://github.com/Geographs/GeoSnipe/releases",
    project_urls={
        "GitHub": "https://github.com/Geographs/GeoSnipe",
        "Documentation": "https://geographs.pro/GeoSnipe/",
        "Bug Tracker": "https://github.com/Geographs/GeoSnipe/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=["geosnipe", "geosnipe.auth"],
    python_requires=">=3.9",
    license="MIT",
    entry_points={"console_scripts": ["geosnipe=geosnipe.__main__:main"]},
    install_requires=["fire>=0.4.0", "aiohttp>=3.7.4.post0", "msmcauth==0.0.3", "paramiko>=2.7.2"]
)
