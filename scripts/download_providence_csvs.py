"""This script downloads the CSV data\
of the 6 children of the Providence corpus"""

from pathlib import Path
import os
from typing import Set
import childespy

# instead of loading all the data once in the memory,
# load the data one child by child.
CHILDREN: Set[str] = {'Alex', 'Ethan', 'Lily',
                      'Naima', 'Violet', 'William'}

def downloads_children_csvs(out_directory_name: str) -> None:
    """
    This function will download CSV data for each child in\
    the providence corpus. We will use childespy of version\
    1.0.1 to do this.

    Parameters
    ----------
    - out_directory_name: str
      The directory where the CSV data will be stored.
    """
    for children in CHILDREN :
        childespy.get_utterances(language="eng",
                                  collection="Eng-NA",
                                  corpus="Providence",
                                  target_child=children).to_csv(
                                    f"{out_directory_name}/{children}.csv")

if __name__ == "__main__" :
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument("--out_directory_name",
                        help="The directory where outputs will be stored.",
                        required=True)
    args = parser.parse_args()
    out_directory_name = Path(args.out_directory_name)
    out_directory_name.mkdir(parents=True, exist_ok=True)
    downloads_children_csvs(out_directory_name)
