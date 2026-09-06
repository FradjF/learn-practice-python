from pathlib import Path
from organizer.core import categorize_file, move
from unittest.mock import patch
import pytest

TEST_CATEGORIES = {
  "Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
  "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
  "Videos":[".mp4"],
  "Zips":[".zip"]
}

###############################################################
##########          Test "categorize_file"           ##########
###############################################################
# def test_categorize_jpg():
#     result = categorize_file(Path("photo.jpg"), TEST_CATEGORIES)
#     assert result == "Images"
#
# def test_categorize_pdf():
#     result = categorize_file(Path("doc.pdf"), TEST_CATEGORIES)
#     assert result == "Docs"
#
# def test_categorize_mp4():
#     result = categorize_file(Path("clip.mp4"), TEST_CATEGORIES)
#     assert result == "Videos"
#
# def test_categorize_zip():
#     result = categorize_file(Path("compressed.zip"), TEST_CATEGORIES)
#     assert result == "Zips"
#
# def test_categorize_other():
#     result = categorize_file(Path("data.csv"), TEST_CATEGORIES)
#     assert result == "Other"
#
# def test_categorize_uppercase_ext():
#     result = categorize_file(Path("photo.JPG"), TEST_CATEGORIES)
#     assert result == "Images"
#
# def test_categorize_no_ext():
#     result = categorize_file(Path("file"), TEST_CATEGORIES)
#     assert result == "Other"

### Parameterized test - replacing the 7 tests above ###
@pytest.mark.parametrize(
    "filename, expected",
    [
        ("photo.jpg", "Images"),
        ("doc.pdf", "Docs"),
        ("clip.mp4", "Videos"),
        ("compressed.zip", "Zips"),
        ("data.csv", "Other"),
        ("photo.JPG", "Images"),
        ("file", "Other")
    ]
)

def test_categorize_file(filename, expected):
    assert categorize_file(Path(filename), TEST_CATEGORIES) == expected

###############################################################
##########                Test "move"                ##########
###############################################################
def test_successful_move(tmp_path: Path):
    source_file = tmp_path/"photo.jpg"
    source_file.touch()

    result = move(source_file, "Images", tmp_path)

    assert result == "Moved."
    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert not (tmp_path / "photo.jpg").exists()

def test_collision(tmp_path: Path):
    source_file = tmp_path / "photo.jpg"
    source_file.touch()

    existing_file = tmp_path / "Images" / "photo.jpg"
    existing_file.parent.mkdir()
    existing_file.touch()

    result = move(source_file, "Images", tmp_path)

    assert result == "Skipped."
    assert (tmp_path / "Images" / "photo.jpg").exists()
    assert (tmp_path / "photo.jpg").exists()

def test_failure(tmp_path: Path):
    source_file = tmp_path / "photo.jpg"
    source_file.touch()

    with patch("organizer.core.shutil.move") as mock_move:
        mock_move.side_effect = OSError("Something went wrong.")

        result = move(source_file, "Images", tmp_path)

    assert result == "Failed."
    assert (tmp_path / "photo.jpg").exists()

