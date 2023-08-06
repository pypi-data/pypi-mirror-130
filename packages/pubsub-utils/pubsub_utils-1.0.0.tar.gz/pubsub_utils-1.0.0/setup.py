import setuptools

setuptools.setup(
    name="pubsub_utils",
    version="1.0.0",
    author="Wonderful Agency",
    author_email="web.devops@wonderful.com",
    description="Pub sub package ",
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/wonderfulagency/pubsub-utils",
    packages=setuptools.find_packages(),
    install_requires=["google-cloud-pubsub>=2.0.0"],
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)

