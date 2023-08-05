import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xiu",
    version="0.0.5", # Latest version .
    author="R2FsCg",
    author_email="r2fscg@gmail.com",
    description="XIUXIU",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/private_repo/codefast",
    packages=setuptools.find_packages(),
     entry_points={
        'console_scripts': [
            'data=xiu.urls:display_shared_links'
        ]
    },

    install_requires=[
	    'codefast'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
