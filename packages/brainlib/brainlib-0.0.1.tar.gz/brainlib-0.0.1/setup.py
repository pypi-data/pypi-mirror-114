import setuptools

setuptools.setup(
    name="brainlib",
    version="0.0.1",
    author="BrainLib Team",
    author_email="genssler@iti.uni-stuttgart.de",
    description="Stay tuned!",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
