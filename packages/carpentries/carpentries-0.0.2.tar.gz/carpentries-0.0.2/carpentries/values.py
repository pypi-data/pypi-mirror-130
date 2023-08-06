"""
The Nine Core Values of The Carpentries.
https://carpentries.org/blog/2019/11/carpentries-values/
"""


def our_values(print_values: bool = False) -> str:
    """
    The Nine Core Values of The Carpentries.
    """

    value_str = """
    At The Carpentries we...

    - Act Openly
    - Empower One Another
    - Value All Contributions

    We are...

    - Always Learning
    - Inclusive of All

    We champion...

    - People First
    - Access for All
    - Community Collaboration
    - Strength through Diversity
    """
    if value_str:
        print(value_str)

    return value_str


our_values(print_values=True)
