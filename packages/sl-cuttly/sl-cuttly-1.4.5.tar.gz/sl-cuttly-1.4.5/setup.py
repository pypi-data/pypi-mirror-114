from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="sl-cuttly",
    version="1.4.5",
    description="",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/shehan9909/sl-cuttly",
    author="shehan_lahiru",
    author_email="www.shehan6472@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    packages=["sl_cuttly"],
    include_package_data=True,
    install_requires=["sl-shortner"],
    entry_points={
        "console_scripts": [
            "sl-cuttly=sl_cuttly.__main__:main",
        ]
    },
)
