import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hugging-gan-test",
    version="0.0.8",
    author="Javi and Vicc",
    author_email="vipermu97@gmail.com",
    description="Testing pip",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/javismiles/HuggingGAN",
    project_urls={
        "Docs": "https://github.com/javismiles/HuggingGAN/docs",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={
        "": ".",
        "taming": "./bigotis/models/taming/modeling_taming",
    },
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires = []
)