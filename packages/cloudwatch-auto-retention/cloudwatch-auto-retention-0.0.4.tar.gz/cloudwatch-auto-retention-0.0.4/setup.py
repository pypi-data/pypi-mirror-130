import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudwatch-auto-retention",
    "version": "0.0.4",
    "description": "CloudWatch Auto Retention is a construct that creates a Lambda with a cronjob that checks whether CloudWatch loggroups are set to never-expire. If so, the construct sets it to one month.",
    "license": "Apache-2.0",
    "url": "https://github.com/stroobants-dev/cloudwatch-auto-retention",
    "long_description_content_type": "text/markdown",
    "author": "Tom Stroobants<tom@stroobants.dev>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/stroobants-dev/cloudwatch-auto-retention"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_cloudwatch_auto_retention",
        "cdk_cloudwatch_auto_retention._jsii"
    ],
    "package_data": {
        "cdk_cloudwatch_auto_retention._jsii": [
            "cloudwatch-auto-retention@0.0.4.jsii.tgz"
        ],
        "cdk_cloudwatch_auto_retention": [
            "py.typed"
        ]
    },
    "python_requires": ">=3.6",
    "install_requires": [
        "aws-cdk-lib>=2.1.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.47.0, <2.0.0",
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
