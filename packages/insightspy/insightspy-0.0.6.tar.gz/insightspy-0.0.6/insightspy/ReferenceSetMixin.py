from insightspy.SessionCore import RequestCore
from insightspy.utils import _parse_locus
import pandas as pd


class ReferenceSetsMixin(RequestCore):
    def reference_sets(self, tag_suffix="_tag_dupl"):
        """List reference sets

        Lists reference sets accessible withthin the current portal session. Project
            access is limited by user id.

        Args:
            tag_suffix (str):  the suffix that is appended to the column name if a tag
                shares the same name as one of the columns in the core database used to
                describe the reference sets

        Examples:
            >>> # p is a logged in portal session
            >>> p.reference_sets()

        Returns:
            DataFrame: table annotation metadata
        """
        export_keys = [
            "annotation_id",
            "description",
            "reference_genome",
            "size",
            "tags",
        ]
        out = [
            {key: v[key] for key in export_keys}
            for v in self._post(
                "annotation/retrieve", {"tagsAsDict": True}, expect_data=True
            )["response"]["data"]
        ]
        out = pd.DataFrame.from_dict(out)
        out.rename(columns={"annotation_id": "reference_id"}, inplace=True)
        return out.join(
            pd.DataFrame(out.pop("tags").values.tolist()), rsuffix=tag_suffix
        )

    def get_reference_set(self, reference_id):
        """Get reference set

        Get reference set as a pandas dataframe

        Args:
            reference_id (int): a reference_id

        Examples:
            >>> # p is a logged in portal session
            >>> p.get_reference_set(5)

        Returns:
            DataFrame: chromosomal co-ordinates in (,] intervals
        """
        if not isinstance(reference_id, (int, float)):
            raise TypeError("reference_id must be an integer")
        if int(reference_id) == 1:
            raise NotImplementedError(
                "Reference set 1 is a special set in the portal "
                + "whose export is not currently supported"
            )
        d = self._post(
            "annotation/features",
            {"annotation_id": int(reference_id)},
            expect_data=True,
        )["response"]["data"]
        out = pd.DataFrame.from_records(
            [
                _parse_locus(x["location"]) + [x["feature_id"]]
                for x in d[str(reference_id)]["ids"]
            ]
        )
        out.columns = ["seqname", "start", "end", "name"]
        out = out.astype({"start": "int32", "end": "int32"}, copy=False)
        return out
