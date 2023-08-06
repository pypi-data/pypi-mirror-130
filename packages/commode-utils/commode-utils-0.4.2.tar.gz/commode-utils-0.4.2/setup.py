from setuptools import setup

VERSION = "0.4.2"

with open("README.md") as readme_file:
    readme = readme_file.read()

with open("requirements.txt") as requirements_file:
    install_requires = [
        "tqdm >= 4.62.0",
        "torchmetrics >= 0.6.0",
        "torch >= 1.10.0",
        "omegaconf >= 2.1.0",
        "pytorch_lightning >= 1.5.0",
        "sacrebleu >= 2.0.0",
    ]

setup_args = dict(
    name="commode-utils",
    version=VERSION,
    description="Set of useful functions and modules for Code Modeling",
    long_description_content_type="text/markdown",
    long_description=readme,
    install_requires=install_requires,
    license="Apache 2.0",
    package_data={"commode_utils": ["py.typed"]},
    packages=[
        "commode_utils",
        "commode_utils.metrics",
        "commode_utils.modules",
        "commode_utils.losses",
        "commode_utils.callbacks",
    ],
    zip_safe=False,
    author="Egor Spirin",
    author_email="spirin.egor@gmail.com",
    keywords=[],
    url="https://github.com/SpirinEgor/commode-utils",
    download_url="https://pypi.org/project/commode-utils/",
)

if __name__ == "__main__":
    setup(**setup_args)
