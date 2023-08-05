import requests
from sniplink.utils import *
from sniplink.api import API
from sniplink.objects import ShortLinkData


class Client:
    """
    The Backend Client
    Sniplink-Py is powered by a back-end client/runner, this system is responsible for ensuring safety among API access.

    Once you've registered a client, you can access all the Sniplink-Py API features available without worry.
    It's best to declare your client in the global scope to ensure you only ever have one client active.
    """
    def __init__(self):
        pass

    @staticmethod
    def get_link(public_id):
        """
        Fetches the data of shortlink with provided public ID.

        :param public_id:
        :returns ShortLinkData:
        """
        resp = requests.get(API.link_endpoint + f"/{public_id}").json()
        return ShortLinkData(resp['id'], resp['creationTime'], resp['expirationTime'], resp['value'], resp['shortUrl'])

    @staticmethod
    def create_link(expires_in, url):
        """
        Creates a new shortlink with provided expires_in, url values.

        Note: expires_in value represents a unix timestamp.
        the maximum expiration time is 30 days.

        :param expires_in:
        :param url:
        :returns ShortLinkData:
        """
        body = {
            "value": url
        }

        if isinstance(expires_in, float) or isinstance(expires_in, int):
            body["expirationTime"] = int(expires_in)
        elif isinstance(expires_in, str):
            body["expirationTime"] = int(expires_in)
        else:
            raise SnipLinkError("Invalid expires in value passed.")

        resp = requests.post(API.link_endpoint, json=body, headers={'content-type': 'application/json'}).json()
        return ShortLinkData(resp['id'], resp['creationTime'], resp['expirationTime'], resp['value'], resp['shortUrl'])
