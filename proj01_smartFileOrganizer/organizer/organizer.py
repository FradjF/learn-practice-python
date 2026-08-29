from pathlib import Path
import shutil

categories = {"Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
              "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
              "Videos":[".mp4"],
              "Zips":[".zip"]}

def categorize_file(file_path:Path) -> str:
    """
        Returns the destination category of file based on its extension.
    """
    file_ext = file_path.suffix
    for (key, value) in categories.items():
        if file_ext.lower() in value:
            category = key
            break
    else:
        category = "Other"

    return category

def build_destination_path(destination:Path) -> None:
    """
        Creates a destination path for a given category.
    """
    destination.mkdir(parents=True, exist_ok=True)

def move(item:Path, category:str, folder:Path) -> str:
    """
        Move a file to its category directory.

        Returns a status describing whether the file was moved,
        skipped because the destination exists, or failed.
    """
    destination = folder / category
    file_path = destination / item.name
    if file_path.exists():
        return "Skipped."

    try:
        build_destination_path(destination)
        shutil.move(item,destination)
        return "Moved."
    except OSError as e:
        return f"Failed: {e}."

def move_result(item:Path, category:str, result, dry_run:bool) -> str:
    """
        Report the action
    """
    return f"[DRY_RUN] {item.name} -> {category}" if dry_run else f"{item.name} -> {category}: {result}"

def organize_folder(folder:Path, dry_run:bool) -> None:
    """
        Organize files in a folder based on their extension.

        In dry-run mode, report the actions without modifying the filesystem.
    """
    print("Scanning folder ...\n")
    if dry_run:
        print("#### DRY_RUN mode activated ####")
    else:
        print("Moving files ...")

    for item in folder.iterdir():
        if not item.is_dir():
            category = categorize_file(item)
            result = ""
            if not dry_run:
                result = move(item, category, folder)
            print(f"{move_result(item, category, result, dry_run)}")