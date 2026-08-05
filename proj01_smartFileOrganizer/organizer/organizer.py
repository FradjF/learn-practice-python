from pathlib import Path

categories = {"Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
              "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
              "Vids":[".mp4"],
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
    else: category = "Other"

    return category


def move_file(folder:Path) -> None:
    """
        Moves files to destination folder based on their extension.
    """
    print("Would move:\n")
    for item in folder.iterdir():
        if not item.is_dir():
            print(f"{item.name}\n -> {categorize_file(item)}\n")
