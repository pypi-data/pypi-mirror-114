import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()


setuptools.setup(
    name="yatai",
    version="0.0.1",
    author="bentoml",
    author_email="contact@bentoml.ai",
    description="Model and deployment management for BentoML",
    long_description=long_description,
    url="https://github.com/bentoml/bentoml",
    packages=setuptools.find_packages(exclude=["tests*"]),
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    python_requires=">=3.6.1",
)

