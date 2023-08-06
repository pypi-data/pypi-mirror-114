def is_string(arg: any) -> bool:
    """Checks if an argument is a valid string.

        Parameters
        ----------
        arg
            A variable of any type to be checked.

        Returns
        -------
        bool
            True/False depending on the argument being a string.
        """
    return isinstance(arg, str)
