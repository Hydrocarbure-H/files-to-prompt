import os
import argparse
import fnmatch
import pyperclip
from typing import List, Optional

def is_excluded_directory(dirname: str) -> bool:
    """
    Check if a directory should be excluded from the search.

    Parameters
    ----------
    dirname : str
        The name of the directory to check.

    Returns
    -------
    bool
        True if the directory is excluded, False otherwise.
    """
    excluded_dirs = {"node_modules", "__pycache__", ".git"}
    return dirname in excluded_dirs

def find_files(base_dir: str, extensions: List[str], recursive: bool, depth: Optional[int]) -> List[str]:
    """
    Find files in a directory matching the given extensions, optionally recursively and up to a specified depth.

    Parameters
    ----------
    base_dir : str
        The base directory to search for files.
    extensions : List[str]
        A list of file extensions to include (e.g., [".js", ".py"]).
    recursive : bool
        Whether to search directories recursively.
    depth : Optional[int]
        The maximum depth for recursive search. Ignored if recursive is False or depth is None.

    Returns
    -------
    List[str]
        A list of relative file paths that match the specified criteria.
    """
    files: List[str] = []
    for root, dirs, filenames in os.walk(base_dir):
        # Exclude non-pertinent repositories
        dirs[:] = [d for d in dirs if not is_excluded_directory(d)]

        # Limit depth if specified
        if recursive and depth is not None:
            current_depth = root[len(base_dir):].count(os.sep)
            if current_depth >= depth:
                dirs[:] = []  # Stop deeper traversal

        for ext in extensions:
            for filename in fnmatch.filter(filenames, f"*{ext}"):
                files.append(os.path.relpath(os.path.join(root, filename), base_dir))

        if not recursive:
            break  # If not recursive, process only the top-level directory

    return files

def concatenate_files_to_clipboard(files: List[str]) -> None:
    """
    Concatenate the contents of specified files and copy the result to the clipboard.

    Parameters
    ----------
    files : List[str]
        A list of file paths to concatenate.

    Returns
    -------
    None
    """
    content: List[str] = []
    for file in files:
        content.append(f"[./{file}]\n")
        try:
            with open(file, "r", encoding="utf-8") as f:
                content.append(f.read() + "\n")
        except Exception as e:
            content.append(f"Error reading file {file}: {e}\n")

    combined_content = "\n".join(content)
    pyperclip.copy(combined_content)
    print("Contents copied to clipboard.")

def main() -> None:
    """
    Main function to parse arguments, find files, and concatenate their contents to the clipboard.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    parser = argparse.ArgumentParser(description="Concatenate file contents to clipboard.")
    parser.add_argument(
        "--format",
        type=str,
        help="File extensions to include, e.g., [*.js,*.py]",
        required=True,
    )
    parser.add_argument(
        "--recursive", "-r",
        action="store_true",
        help="Search files recursively.",
    )
    parser.add_argument(
        "--depth",
        type=int,
        help="Maximum depth for recursive search. Ignored if --recursive is not set.",
    )
    args = parser.parse_args()

    # Parse extensions from --format
    if args.format.startswith("[") and args.format.endswith("]"):
        extensions = [ext.strip() for ext in args.format[1:-1].split(",")]
    else:
        print("Invalid format for --format. Use [*.js,*.py].")
        return

    # Find files based on the arguments
    base_dir = os.getcwd()
    files = find_files(base_dir, extensions, args.recursive, args.depth)

    if not files:
        print("No files found matching the specified criteria.")
        return

    # Concatenate contents and copy to clipboard
    concatenate_files_to_clipboard(files)

if __name__ == "__main__":
    main()
