__all__ = ["assert_existing_rel_paths_within_tree"]

from pathlib import Path
from typing import List
from myminions import APath


def assert_existing_rel_paths_within_tree(
    expected_rel_paths: List[APath], target_path: APath
):
    """
    Asserts whether the expected file paths are within the target path. This
    method is meant for testing purposes.

    Notes:
        After moving files or copying this function asserts the success of the
        operation.

    Args:
        expected_rel_paths:
            Expected sub paths relative to the target path.

        target_path:
            The target path which should contain the expected sub paths.

    Examples:

        >>> import glob
        >>> from doctestprinter import doctest_iter_print
        >>> test_tree = list(sorted(glob.glob("./tests/resources/**", recursive=True)))
        >>> doctest_iter_print(test_tree)
        ./tests/resources/
        ./tests/resources/resources_index.md
        ./tests/resources/sample-1
        ./tests/resources/sample-1/file-1.txt
        ./tests/resources/sample-1/file-2.csv

        >>> expected_sample_paths = [
        ...     "sample-1",
        ...     "resources_index.md",
        ...     "sample-1/file-1.txt",
        ...     "sample-1/.hidden"
        ... ]
        >>> assert_existing_rel_paths_within_tree(
        ...     expected_rel_paths=expected_sample_paths,
        ...     target_path="tests/resources"
        ... )


        >>> assert_existing_rel_paths_within_tree(
        ...     expected_rel_paths=["is_not_there"],
        ...     target_path="tests/resources"
        ... )
        Traceback (most recent call last):
        ...
        AssertionError: Path 'tests/resources' doesn't contain these subpath(s) ['is_not_there'].
    """
    target_path = Path(target_path)
    paths_not_in_tree = []

    for expected_path_part in expected_rel_paths:
        expected_path_in_tree = target_path.joinpath(expected_path_part)
        if expected_path_in_tree.exists():
            continue
        paths_not_in_tree.append(expected_path_part)

    no_missing_file_paths = len(paths_not_in_tree) == 0
    if no_missing_file_paths:
        return

    missing_paths = "', '".join(
        [str(missing_path) for missing_path in paths_not_in_tree]
    )
    err_msg = "Path '{}' doesn't contain these subpath(s) ['{}'].".format(
        target_path, missing_paths
    )
    raise AssertionError(err_msg)
