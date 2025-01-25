# Clipboard File Concatenator 🖇️

Easily concatenate file contents and copy them to your clipboard with this Python script. Whether you need to quickly review code snippets or gather documentation fragments, this tool simplifies the process. This project has been created to easily pass some code from differents files to an AI prompt.

## Features ✨
- **File Search**: Locate files with specified extensions (`.py`, `.js`, etc.) in the current directory.
- **Recursive Search**: Optionally traverse subdirectories to find files.
- **Depth Control**: Limit the recursive search depth to keep it manageable.
- **Clipboard Integration**: Combine file contents and copy them directly to your clipboard.

## How to Use 🚀
1. **Install Requirements**:
   ```bash
   pip install pyperclip
   ```
2. **Run the Script**:
   ```bash
   python filetoprompt.py --format [*.py,*.js] --recursive --depth 2
   ```
   - `--format`: Specify file extensions to include (e.g., `[*.py,*.js]`).
   - `--recursive`: Enable recursive file search.
   - `--depth`: Set maximum recursion depth (optional).

3. **Copy Content**: The combined file contents will be automatically copied to your clipboard. Paste it wherever you need!

## Example Output 📋
After running the script:
```
[./example.py]
<content of example.py>

[./subdir/example.js]
<content of example.js>
