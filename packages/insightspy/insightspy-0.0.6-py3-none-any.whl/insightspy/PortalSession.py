from insightspy.ProjectsMixin import ProjectsMixin
from insightspy.SamplesMixin import SamplesMixin
from insightspy.PipelinesMixin import PipelinesMixin
from insightspy.ReferenceSetMixin import ReferenceSetsMixin
from insightspy.ComparisonsMixin import ComparisonsMixin
from insightspy.SignaturesMixin import SignaturesMixin
import requests
import getpass


class PortalSession(
    ProjectsMixin,
    SamplesMixin,
    PipelinesMixin,
    ReferenceSetsMixin,
    ComparisonsMixin,
    SignaturesMixin,
):
    def __init__(self, api_key=None, url="https://insights.arpeggiobio.com"):
        session = requests.Session()
        self._session = session
        self.url = url
        if api_key is not None:
            self._update_credentials(api_key)

    def login(self, email=None, password=None, api_key=None):
        """Login to Arpeggio portal

        Logs in current session to the Arpeggio portal. All subsequent requests will be
        authenticated with these credentials. Will try the `api_key` first if
        specified. If `api_key` is not present can use the same `email` and `password`
        that is used to log in to the portal. If email is entered without as password
        the user will be asked to enter their password. NOTE: we do not reccommend
        saving your password in a script, either access it as an environment variable or
        enter it interactively.

        Args:
            api_key (str): login key
            email (str): email used to login to the arpeggio portal
            password (str): password used to login to the arpeggio portal

        Examples:
            >>> p = PortalSession()
            >>> p.login(email = user@domain.com)
        """
        if api_key is None:
            if email is not None and password is None:
                password = getpass.getpass()
            elif email is None and password is None:
                raise ValueError("Please specify login credentials")
            access_response = self._post(
                "user/login", {"email": email, "password": password}, True
            )
            self._update_credentials(access_response["response"]["data"]["token"])
        else:
            raise NotImplementedError("API key login not yet implemented")
        print("Login succeeded")
