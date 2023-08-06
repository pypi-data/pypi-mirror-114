from typing import Dict, Union, Optional, Tuple
from threading import Thread, Event
import requests


class Get:
    """A :code:`get` method with progress tracking.

    Uses :mod:`requests` as a backend. The request takes place in the background
    and can be queried with :meth:`Get.finished`.

    Example:
        get = Get()
        url = "http://some_url/files/a_file"
        another_url = "http://some_other_url/files/b_file"
        get(url, **kwargs)                 # fetches url in background
        get(another_url, **kwargs)         # fetches url in background
        while not get.finished(url):
            print(get.progress(url))       # prints progress
            time.sleep(1)

    """

    def __init__(self):
        self._status: Dict[str, int] = {}
        self._finished: Dict[str, Event] = {}
        self._dl_bytes: Dict[str, int] = {}
        self._progress: Dict[str, Union[int, float]] = {}
        self._result: Dict[str, bytes] = {}

    def __call__(self, url: str, **kwargs):
        """Call :func:`requests.get` with the :code:`url` and :code:`kwargs`.

        Args:
            url: The url to fetch
            kwargs: passed to :func:`requests.get`

        """
        self._finished[url] = Event()
        self._progress[url] = 0
        t = Thread(target=self._call_subr, args=[url], kwargs=kwargs)
        t.start()

    def _call_subr(self, url, **kwargs):
        content = bytearray()
        response = requests.get(url, stream=True, **kwargs)
        self._status = response.status_code
        if response.status_code != 200:
            self._finished[url].set()
            self._result[url] = response.content
        else:
            total = response.headers.get('content-length')
            self._dl_bytes[url] = 0
            if total is not None:           # no content length header
                total_length = int(total)
            for data in response.iter_content(chunk_size=4096):
                content.extend(data)
                self._dl_bytes[url] += 4096
                if total is not None:
                    self._progress[url] = (100 * (self._dl_bytes[url] / total_length))
            self._finished[url].set()
            self._result[url] = content

    def result(self, url: str) -> Tuple[int, Union[bytes, bytearray]]:
        """Return the result of the fetch operation.

        Args:
            url: The url for which to perform operation

        Returns:
            A tuple of status and response content.

        """
        return self._status[url], self._result[url]

    def finished(self, url: str) -> Optional[bool]:
        """Check if the URL has been fetched.

        Args:
            url: The url for which to perform operation

        """
        finished = self._finished.get(url)
        if finished:
            return finished.is_set()
        else:
            return None

    def bytes_downloaded(self, url: str) -> Optional[int]:
        """Display progress of URL.

        Args:
            url: The url for which to perform operation

        """
        return self._dl_bytes.get(url)

    def progress(self, url: str) -> Optional[float]:
        """Display progress of URL.

        Args:
            url: The url for which to perform operation

        """
        return self._progress.get(url)

    def clear(self, url: str):
        """Clear the artefacts for URL.

        Args:
            url: The url for which to perform operation

        """
        self._progress.pop(url)
        self._finished.pop(url)
        self._result.pop(url)
        self._dl_bytes.pop(url)
        self._status.pop(url)
