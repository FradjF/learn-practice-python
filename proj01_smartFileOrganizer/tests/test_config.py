import pytest
from organizer.validations import validate_configuration
from organizer.config import get_configuration, DEFAULT_CATEGORIES

TEST_CATEGORIES = {
  "Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
  "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
  "Videos":[".mp4"],
  "Zips":[".zip"]
}

###############################################################
##########      Test "validate_configuration"        ##########
###############################################################

# def test_configuration_valid():
#     result = validate_configuration(TEST_CATEGORIES)
#     assert result is True
#
# def test_configuration_empty_dict():
#     result = validate_configuration({})
#     assert result is False
#
# def test_configuration_list_of_lists():
#     result = validate_configuration([])
#     assert result is False
#
# def test_configuration_category_not_list():
#     result = validate_configuration({"doc":[".pdf",".docx"], "image":".png"})
#     assert result is False
#
# def test_configuration_extension_not_string():
#     result = validate_configuration({"doc":[".pdf",1], "image":[".png"]})
#     assert result is False


@pytest.mark.parametrize(
    "categories, expected",
    [(TEST_CATEGORIES, True),
    ({}, False),
    ([], False),
    ({"doc":[".pdf",".docx"], "image":".png"}, False),
    ({"doc":[".pdf",1], "image":[".png"]}, False)
     ]
)
def test_configuration(categories, expected):
    assert validate_configuration(categories) == expected

###############################################################
##########      Test "get_configuration"        ##########
###############################################################
def test_config_valid(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(
        """
            {
              "Images":[".png", ".jpg", ".jpeg", ".bmp", ".gif"],
              "Docs": [".pdf", ".docx", ".xlsx", ".pptx", ".md"],
              "Videos":[".mp4"],
              "Zips":[".zip"]
            }    
            """,
            encoding="utf-8"
    )
    result = get_configuration(config_file)
    assert result == TEST_CATEGORIES


def test_config_missing_file(tmp_path):
    config_file = tmp_path / "config.json"
    result = get_configuration(config_file)

    assert result == DEFAULT_CATEGORIES


def test_config_invalid_json(tmp_path):
    config_file = tmp_path / "config.json"
    config_file.write_text(
    """
        {"Images": [".jpg", ".png"}
    """
    )
    result = get_configuration(config_file)
    assert result == DEFAULT_CATEGORIES