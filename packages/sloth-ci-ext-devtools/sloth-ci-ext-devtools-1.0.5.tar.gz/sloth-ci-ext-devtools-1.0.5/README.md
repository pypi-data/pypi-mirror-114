# Utilities to help developers create validators and extensions for Sloth CI


## Installation
    
    $ pip install sloth-ci-ext-devtools


## Usage

Enable the extension in the server config:

    extensions:
        dev:
            # Use the module sloth_ci.ext.devtools.
            module: devtools

Call `sci dev` with `-e` or `-v` to create an extensions or a validator template:

    $ sci dev -e spam
    Extension "spam" created.
    $ sci dev -v eggs
    Validator "eggs" created.
