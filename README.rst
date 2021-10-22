============================================
Welcome to create-a-cli-tool 👋
============================================

|Version| |License: MIT|

    A way to make simple python CLIs.

🏠 `Homepage <https://github.com/Sengolda/create-a-cli-tool>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install
======================

.. code:: sh

    pip install -U create-a-cli-tool

Features
======================

-  Easy-To-Use
-  Maintained CLI Tool Maker
-  Built-In Help Command

Quick Example
======================

.. code:: py

    from cli.cli import CLI

    my_cli = CLI("My Nice CLI tool!")

    @my_cli.command(name="hi", description="Say hello!")
    def hi():
        print("Hello World!")

    my_cli.run()

Author
======================

👤 **Sengolda**

*  Github: `@Sengolda <https://github.com/Sengolda/create-a-cli-tool/issues>`_

🤝 Contributing
======================

Contributions, issues and feature requests are welcome!

Feel free to check `issues
page <https://github.com/Sengolda/create-a-cli-tool/issues>`__.

Show your support
======================


Give a ⭐️ if this project helped you!

.. |Version| image:: https://img.shields.io/badge/version-0.1.0-blue.svg?cacheSeconds=2592000
.. |License: MIT| image:: https://img.shields.io/badge/License-MIT-yellow.svg
   :target: #