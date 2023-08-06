import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bodytracking",
    version="1.02",
    author="Suprime",
    license = 'MIT',
    author_email="suprime.sendings@gmail.com",
    description="bodytracking is a collection of functions powered by mediapipe and opencv-python.",
    long_description= long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MOBSkuchen/tkt-Toolkit",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'mediapipe',
        'opencv-python'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)