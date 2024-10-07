import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ATCForm",
    version="0.1.7.5",
    description="ATCFrom - Automatically fill in the collection form 自动化表单填写工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YKONGCO/ATCForm",
    author="YKONGCO",
    author_email="1570585752@qq.com",
    maintainer="YKONGCO",
    maintainer_email="1570585752@qq.com",
    license="MIT License",
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    project_urls={
        "Bug Tracker": "https://github.com/YKONGCO/ATCForm/issues",
    },
    python_requires=">=3.8",
    install_requires=[
        "webdriver_manager",
        "selenium>=4.0",
        "ping3",
    ]
)


