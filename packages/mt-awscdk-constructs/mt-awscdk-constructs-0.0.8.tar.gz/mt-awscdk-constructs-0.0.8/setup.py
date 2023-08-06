import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "mt-awscdk-constructs",
    "version": "0.0.8",
    "description": "Marley Tech AWS CDK Construct Library",
    "license": "MIT",
    "url": "https://github.com/marleytech/mt-awscdk-constructs.git",
    "long_description_content_type": "text/markdown",
    "author": "Greg Farrow<g-farrow@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/marleytech/mt-awscdk-constructs.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "mt_awscdk_constructs",
        "mt_awscdk_constructs._jsii"
    ],
    "package_data": {
        "mt_awscdk_constructs._jsii": [
            "mt-awscdk-constructs@0.0.8.jsii.tgz"
        ],
        "mt_awscdk_constructs": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk.aws-events-targets>=1.109.0, <2.0.0",
        "aws-cdk.aws-events>=1.109.0, <2.0.0",
        "aws-cdk.aws-lambda>=1.109.0, <2.0.0",
        "aws-cdk.aws-sqs>=1.109.0, <2.0.0",
        "aws-cdk.core>=1.109.0, <2.0.0",
        "constructs>=3.2.27, <4.0.0",
        "jsii>=1.32.0, <2.0.0",
        "publication>=0.0.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
