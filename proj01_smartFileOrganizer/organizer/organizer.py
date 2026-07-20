from pathlib import Path

categories = {"Images":[".png", ".jpg", ".jpeg", ".bmp"],
              "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
              "Vids":[".mp4"]}

def categorize_file(file_path:Path) -> str:
    """
        Returns the destination category of file based on its extension.
    """

    file_ext = file_path.suffix
    category = "Other"
    for (key, value) in categories.items():
        if file_ext.lower() in value:
            category = key
            break
    return category


def move_file(folder:Path) -> None:
    """
        Moves files to destination folder based on their extension.
    """
    print("Would move:\n")
    for item in folder.iterdir():
        print(f"{item.name}\n-> {categorize_file(item)}\n")