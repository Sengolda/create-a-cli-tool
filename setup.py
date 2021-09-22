import re

from setuptools import setup

with open("cli/__init__.py", "r", encoding="utf-8") as f:
    version = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE
    ).group(1)

with open("README.rst", "r", encoding="utf-8") as f:
    long_description = f.read()

if not version:
    raise RuntimeError("version not set...")

extra_requires = {"docs": ["sphinx>=4.0.2", "furo"]}


packages = ["cli", "cli.ext"]


args = dict(
    name="create-a-cli-tool",
    version=str(version),
    description="A way to make simple python CLIs.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/Sengolda/create-a-cli-tool",
    author="Sengolda",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Typing :: Typed",
    ],
    packages=packages,
    include_package_data=True,
    python_requires=">=3.6",  # Cause of f-strings.
    license="MIT",
    extra_requires=extra_requires,
)

setup(**args)
