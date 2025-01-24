import os
import argparse
import fnmatch
import pyperclip

def is_excluded_directory(dirname):
    excluded_dirs = {"node_modules", "__pycache__", ".git"}
    return dirname in excluded_dirs

def find_files(base_dir, extensions, recursive, depth):
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        # Exclure les répertoires non pertinents
        dirs[:] = [d for d in dirs if not is_excluded_directory(d)]

        # Limiter la profondeur si spécifiée
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

def concatenate_files_to_clipboard(files):
    content = []
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

def main():
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
