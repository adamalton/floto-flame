ALBUM_TITLE_TRUNCATIONS = [
    r"^(\d{6,}|-|\s)+",  # Albums which begin with YYYYMMDD dates, or ranges of
]

ALBUM_TITLES_TO_IGNORE = [
    r"^\s+$",
    r"^Auto Upload",
]


PHOTO_TITLES_TO_IGNORE = [
    r"^\s*$",
    r"^IMG_",
    r"^DSC[A-Z]*[0-9]+",
]
