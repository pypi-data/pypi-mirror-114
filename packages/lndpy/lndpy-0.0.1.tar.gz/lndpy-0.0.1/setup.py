import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lndpy",
    version="0.0.1",
    author="Yuval Adam",
    author_email="_@yuv.al",
    description="Modern pythonic bindings for the lightning network daemon ",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuvadm/lndpy",
    project_urls={
        "Bug Tracker": "https://github.com/yuvadm/lndpy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["grpcio", "grpcio-tools", "googleapis-common-protos"],
)
