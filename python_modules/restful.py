#!/usr/bin/env python3
"""
Module providing a REST client class and associated functions, aimed primarily\
at accessing the Ensembl REST API. It is based on the example client found at\
https://github.com/Ensembl/ensembl-rest/wiki/Example-Python-Client.
"""
import time
import requests


class RestClient:
    """
    REST API client to perform rest requests to the indicated server.\
    Rate limiting is performed by waiting 'pause' seconds between requests.
    """

    def __init__(self, server, pause):
        self.server = server
        self.pause = pause
        self.last_time = time.time()

    def rate_limit(self):
        """
        Check the time since last request and limit request rate if needed
        """
        delta_t = time.time() - self.last_time
        if delta_t < self.pause:
            time.sleep(self.pause - delta_t)

    def rest(self, request, header=None, data=None):
        """Make a REST get request to the server"""
        if header is None:
            header = {'Content-Type': 'text/plain'}

        # Perform rate limiting
        self.rate_limit()

        # Make request
        if data is None:
            response = requests.get(self.server + request,
                                    headers=header)

        else:
            response = requests.post(self.server + request,
                                     headers=header,
                                     data=data)

        self.last_time = time.time()

        # Cheack response
        if not response.ok:
            if 'Retry-After' in response.headers:
                time.sleep(float(response.headers['Retry-After'] + 2))
                self.rest(request, header, data)
            else:
                response.raise_for_status()

        return response

if __name__ == "__main__":
    pass
