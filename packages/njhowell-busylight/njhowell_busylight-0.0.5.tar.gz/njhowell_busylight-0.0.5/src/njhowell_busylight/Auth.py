import requests

class Auth:
    """Class to make authenticated requests."""

    def __init__(self, host: str, access_token: str):
        """Initialize the auth."""
        self.host = host
        self.access_token = access_token

    async def request(self, method: str, path: str, **kwargs):
        """Make a request."""
                
        if(method == "get"):
            return requests.get(f"{self.host}/{path}")
        
        if(method == "post"):
            return requests.post(f"{self.host}/{path}", **kwargs)