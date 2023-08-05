class ShortLinkData:
    """
    ShortLinkData represents data attached to a single shortlink.
    The attributes are...
        id: id of the shortlink.
        creation_time: unix timestamp representing the when the shortlink was created.
        expiration_time: unix timestamp representing when will the shortlink expire.
        value: the main URL value behind the shortlink.
        short_url: the short_url.
    """
    id: str
    creation_time: int
    expiration_time: int
    value: str
    short_url: str

    def __init__(self, _id, creation_time, expiration_time, value, short_url):
        self.id = _id
        self.creation_time = creation_time
        self.expiration_time = expiration_time
        self.value = value
        self.short_url = short_url

    def __str__(self):
        return f"{{'id': '{self.id}', 'creationTime': {self.creation_time}, 'expirationTime': {self.expiration_time}," \
               f"'value': '{self.value}', 'shortUrl': '{self.short_url}'}} "
