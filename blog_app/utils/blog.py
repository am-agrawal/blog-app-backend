import string, re


BASE62_ALPHABET = string.digits + string.ascii_letters

def to_base62(num: int) -> str:
    if num == 0:
        return "0"
    base62 = []
    while num:
        num, rem = divmod(num, 62)
        base62.append(BASE62_ALPHABET[rem])
    return ''.join(reversed(base62))


def generate_slug(title, blog_id):
    base_title = title.lower()[:30]
    base_title = re.sub(r"\s+", "-", base_title)
    base_title = re.sub(r"[^a-z0-9\-]", "", base_title)
    base62_id = to_base62(blog_id)
    return f"{base_title}-{base62_id}"
