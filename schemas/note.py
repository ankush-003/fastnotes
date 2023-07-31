def noteEntity(item) -> dict:
    return {
        "_id": str(item["_id"]),
        "title": item["title"],
        "desc": item["desc"],
        # "important": item["important"],
        "file": item["file"],
        "file_type": item["file_type"]
    }

def notesEntity(items) -> list:
    return [noteEntity(item) for item in items]
