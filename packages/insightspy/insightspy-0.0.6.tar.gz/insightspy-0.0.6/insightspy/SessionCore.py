import requests
from insightspy.utils import _single_spaced
from abc import ABC


class RequestCore(ABC):
    def __init__(self, api_key=None, url=None):
        session = requests.Session()
        self._session = session
        self.url = url
        if api_key is not None:
            self._update_credentials(api_key)

    def _update_credentials(self, access_token):
        self.access_token = access_token
        self._session.headers.update({"Authorization": "Bearer {access_token}"})

    def _get(self, route, params={}, expect_data=False):
        """Generic GET request

        Wrapper for generic get request to the Arpeggio portal

        Args:
            route (str): string for the route to call. Do not include the core domain
                (e.g. `https://insights.arpeggiobio.com`).
            params (dict): dictionary of parameters to pass to the route
            expect_data (bool): whether to expect data from the response

        Returns:
            result (dict): A dictionary`{status:status_code,
                response:requests.response}`
        """
        request = self._session.get(f"{self.url}/{route}", params=params)
        return RequestCore._clean_response(request, expect_data=expect_data)

    def _post(self, route, json={}, expect_data=False):
        """Generic POST request

        Wrapper for generic POST request to the Arpeggio portal

        Args:
            route (str): string for the route to call. Do not include the core domain
                (e.g. `https://insights.arpeggiobio.com`).
            json (dict): dictionary of parameters to pass to the route in the body of the
                request as a json
            expect_data (bool): whether to expect data from the response

        Returns:
            result (dict): A dictionary `{status:status_code,
                response:requests.response}`
        """
        request = self._session.post(f"{self.url}/{route}", json=json)
        return RequestCore._clean_response(request, expect_data=expect_data)

    @classmethod
    def _clean_response(cls, request, expect_data):
        if request.status_code == 500:
            raise requests.exceptions.RequestException(
                _single_spaced(
                    f"{request.status_code}: server-side error, "
                    + "please contact Arpeggio Biosciences"
                )
            )
        if request.status_code == 404:
            raise requests.exceptions.RequestException(
                _single_spaced(
                    f"{request.status_code}: route does not exist, "
                    + "please contact Arpeggio Biosciences"
                )
            )
        response = request.json()
        if isinstance(response, str):
            response = {"data": response}
        if "notification" not in response:
            response["notification"] = ""
        if request.status_code != 200:
            raise requests.exceptions.RequestException(
                _single_spaced(f'{request.status_code}: {response["notification"]}')
            )
        if expect_data and response["data"] is None:
            raise ValueError(_single_spaced(response["notification"]))
        return {"status": request.status_code, "response": response}
