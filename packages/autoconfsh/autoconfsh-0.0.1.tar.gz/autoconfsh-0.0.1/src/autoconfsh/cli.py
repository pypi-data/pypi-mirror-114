def cli_entrypoint() -> int:
    """
    CLI execution begins here, this function is the first that executes when the autoconf.sh package is executed.

    :return: integer, this value will be set as the exit-code of the program and can be used for debugging when running
             in a terminal.
    """
    print("Hello world!")

    return 0
