:orphan:

============================================
Welcome to create-a-cli-tool 👋
============================================

|CI_STATUS|

    A way to make simple python CLIs.

🏠 `Homepage <https://github.com/Sengolda/create-a-cli-tool>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install
====================================

.. code:: sh

    pip install -U create-a-cli-tool

Features
============================================

-  Easy-to-use.
-  Comes with a default help command for your cli.

Quick Example
==========================================

.. code:: py

    from cli.cli import CLI

    my_cli = CLI("My Nice CLI tool!")

    @my_cli.command(name="hi", description="Say hello!")
    def hi():
        print("Hello World!")

    my_cli.run()

Author
============================================

👤 **Sengolda**

*  Github: `@Sengolda <https://github.com/Sengolda/create-a-cli-tool/issues>`_

🤝 Contributing
============================================

Contributions, issues and feature requests are welcome!

Feel free to check `issues
page <https://github.com/Sengolda/create-a-cli-tool/issues>`__.

Show your support
======================================


Give a ⭐️ if this project helped you!

.. |CI_STATUS| image:: https://github.com/Sengolda/create-a-cli-tool/workflows/CI/badge.svg

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
