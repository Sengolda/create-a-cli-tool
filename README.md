# Welcome to create-a-cli-tool 👋
![Version](https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](#)

> A way to make simple python CLIs.

### 🏠 [Homepage](https://github.com/Sengolda/create-a-cli-tool)

## Install

```sh
pip install -U git+https://github.com/Sengolda/create-a-cli-tool.git
```

## Features
* Easy-to-use.
* Comes with a default help command for your cli.

## Quick Example
```py
from cli.cli import CLI

my_cli = CLI("My Nice CLI tool!")

@my_cli.command(name="hi", description="Say hello!")
def hi():
    print("Hello World!")

my_cli.run()
```

## Author

👤 **Sengolda**

* Github: [@Sengolda](https://github.com/Sengolda)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/Sengolda/create-a-cli-tool/issues). 

## Show your support

Give a ⭐️ if this project helped you!