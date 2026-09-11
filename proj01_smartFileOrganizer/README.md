# Project 1 — File Organizer

## Product Brief
Imagine your Downloads folder has become a mess.

You want a command-line tool that automatically organizes files into folders.

Instead of manually dragging files around, you'll run:

`file-organizer ~/Downloads`

and get: 
``` 
Downloads/
    Images/
    Docs/
    Videos/
    Zips/
    Other/
```


## Features
- Parse command-line arguments
- Validate the target folder and configuration
- Organize files based on their extensions
- Preview file movements with dry-run mode
- Support custom JSON configuration
- Handle filename collisions
- Log application activity and errors
- Handle expected application errors gracefully
- Provide an installable command-line interface
- Test application behavior with pytest


## Installation

### Requirements
- Python 3.13 or 3.14
- pip

### Install from source
Clone the repository and navigate to the project directory:

```bash
git clone <repository-url>
cd LearnByDoing/proj01_smartFileOrganizer
```

### Install the application
```bash
python -m pip install .
```
### Verify the installation
```bash
file-organizer --help
```


## Usage
### Organize files
Organize files in the specified folder based on their file extensions.
```bash
file-organizer <folder>
```

### Preview changes with dry-run
Show the files that would be moved without actually moving them.
```bash
file-organizer <folder> --dry-run
```

### Use a custom configuration
Define a mapping: category → extensions
```bash
file-organizer <folder> --config <config-file>
```

### Configuration file
Mapping:
```json
{
  "Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
  "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
  "Videos":[".mp4"],
  "Zips":[".zip"]
}
```
Files whose extensions do not match any configured category are placed in `Other`.

### Configuration errors
If a custom configuration file is missing, contains invalid JSON, or has an invalid structure, the application reports an error and exits with a non-zero status code.

### Collision handling
destination already exists → skip file


## Testing
Run the test suite with:
```bash
python -m pytest
```

## CI
Tests are automatically executed by GitHub Actions on pushes and pull requests.

The test suite verifies:

- Configuration validation and configuration loading
- File categorization and file movement
- Collision handling
- Error handling

