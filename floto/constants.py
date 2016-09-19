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


# This is the cache item that stores the list of photo IDS which the frame is currently using
# (The frame always has *all* of the photo IDs, it's really only the order which changes)
PHOTO_LIST_SESSION_KEY = "photo-list"

# This is the index of which photo is the list the frame is currently displaying
CURRENT_PHOTO_INDEX_SESSION_KEY = "current-photo-index"
