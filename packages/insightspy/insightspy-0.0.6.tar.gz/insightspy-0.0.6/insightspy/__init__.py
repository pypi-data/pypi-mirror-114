# Flatten the namespace
from .PortalSession import *  # NOQA
import insightspy.utils
import sys
from .__version__ import __version__

# If in an interactive session
if hasattr(sys, "ps1"):
    # check for portal connection and if that succeeds check package version
    if not insightspy.utils._connect("https://insights.arpeggiobio.com"):
        if not insightspy.utils._connect("https://www.google.com/"):
            print(
                "You are not connected to the internet (or google is down) "
                + "so will be unable to access the Arpeggio Portal"
            )
        else:
            print(
                "Arpeggio portal is not responding. Contact Arpeggio Biosciences "
                + "if this persists."
            )
    else:
        insightspy.utils._versions(__version__)
