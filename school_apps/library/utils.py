import uuid


def get_random_id():
    id = (
        str(uuid.uuid4())[:8].replace("-", "").lower()
    )  # every thing up to 8 chars in lower case
    return id
