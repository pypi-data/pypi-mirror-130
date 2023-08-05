# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_util.ipynb (unless otherwise specified).

__all__ = ['sha1_digest', 'URL', 'make_session']

# Cell
from hashlib import sha1
from base64 import b32encode

def sha1_digest(content: bytes) -> str:
    return b32encode(sha1(content).digest()).decode('ascii')

# Cell
from dataclasses import dataclass

@dataclass(frozen=True)
class URL:
    """Wrapper around a URL string to provide nice display in IPython environments."""

    url: str

    def _repr_html_(self):
        """HTML link to this URL."""
        return f'<a href="{self.url}">{self.url}</a>'

    def __str__(self):
        """Return the underlying string."""
        return self.url

# Cell
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

def make_session(pool_maxsize):
    retry_strategy =  Retry(total=5, backoff_factor=1, status_forcelist=set([504, 500]))
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_maxsize=pool_maxsize, pool_block=True)
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session