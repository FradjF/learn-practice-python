from pathlib import Path
from organizer.core import categorize_file
from config import validate_configuration

TEST_CATEGORIES = {
  "Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
  "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
  "Videos":[".mp4"],
  "Zips":[".zip"]
}

###############################################################
##########          Test "categorize_file"           ##########
###############################################################
def test_categorize_jpg():
    result = categorize_file(Path("photo.jpg"), TEST_CATEGORIES)
    assert result == "Images"

def test_categorize_pdf():
    result = categorize_file(Path("doc.pdf"), TEST_CATEGORIES)
    assert result == "Docs"

def test_categorize_mp4():
    result = categorize_file(Path("clip.mp4"), TEST_CATEGORIES)
    assert result == "Videos"

def test_categorize_zip():
    result = categorize_file(Path("compressed.zip"), TEST_CATEGORIES)
    assert result == "Zips"

def test_categorize_other():
    result = categorize_file(Path("data.csv"), TEST_CATEGORIES)
    assert result == "Other"

def test_categorize_uppercase_ext():
    result = categorize_file(Path("photo.JPG"), TEST_CATEGORIES)
    assert result == "Images"

def test_categorize_no_ext():
    result = categorize_file(Path("file"), TEST_CATEGORIES)
    assert result == "Other"

###############################################################
##########      Test "validate_configuration"        ##########
###############################################################

def test_configuration_valid():
    result = validate_configuration(TEST_CATEGORIES)
    assert result is True

def test_configuration_empty_dict():
    result = validate_configuration({})
    assert result is False

def test_configuration_list_of_lists():
    result = validate_configuration([])
    assert result is False

def test_configuration_category_not_list():
    result = validate_configuration({"doc":[".pdf",".docx"], "image":".png"})
    assert result is False

def test_configuration_extension_not_string():
    result = validate_configuration({"doc":[".pdf",1], "image":[".png"]})
    assert result is False