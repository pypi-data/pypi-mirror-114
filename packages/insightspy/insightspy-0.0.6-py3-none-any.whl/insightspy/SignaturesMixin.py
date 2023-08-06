from insightspy.SessionCore import RequestCore
from insightspy.utils import _list_to_int_list, _parse_locus
import pandas as pd


class SignaturesMixin(RequestCore):
    def signatures(self):
        """List signatures

        Lists signatures accessible within the current portal session. Access is
        limited by user id.

        Examples:
            >>> # p is a logged in portal session
            >>> p.signatures()

        Returns:
            DataFrame: signature metadata
        """
        export_keys = ["signature_id", "description", "annotation_id", "size"]
        data = self._post("signature/retrieve", {"noData": True}, expect_data=True)[
            "response"
        ]["data"]
        if data is None:
            return pd.DataFrame()
        out = pd.DataFrame.from_records(
            [{key: v[key] for key in export_keys} for v in data.values()]
        )
        out.rename(columns={"annotation_id": "parent_reference"}, inplace=True)
        return out

    def get_signatures(self, signature_ids):
        """Get signature set

        Get signature set coordinates as a pandas dataframe

        Args:
            signature_id (int): a signature_id

        Examples:
            >>> # p is a logged in portal session
            >>> p.get_signatures(8)

        Returns:
            {DataFrame}:
                dictionary of DataFrames containing the chromosomal co-ordinates in (,]
                intervals for the signatures. The dictionary keys are the signature ids
        """
        if not isinstance(signature_ids, list):
            signature_ids = [signature_ids]
        signature_ids = _list_to_int_list(signature_ids)
        d = self._post(
            "signature/retrieve",
            {"signature_ids": signature_ids, "noData": False},
            expect_data=True,
        )["response"]["data"]
        colnames = ["seqname", "start", "end", "name"]
        out = {
            k: pd.DataFrame.from_records(
                [
                    _parse_locus(x["location"]) + [x["feature_id"]]
                    for x in v["features"]
                ],
                columns=colnames,
            )
            for k, v in d.items()
        }
        return out
