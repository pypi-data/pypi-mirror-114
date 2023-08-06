from insightspy.SessionCore import RequestCore
from insightspy.utils import _list_to_int_list
import pandas as pd


class ComparisonsMixin(RequestCore):
    def comparisons(self):
        """List comparisons

        Lists comparisons accessible within the current portal session. Access is
        limited by user id.

        Examples:
            >>> # p is a logged in portal session
            >>> p.comparisons()

        Returns:
            DataFrame: comparison metadata
        """
        export_keys = [
            "comparison_id",
            "description",
            "genome",
            "control_label",
            "treatment_label",
            "treatment_ids",
            "control_ids",
        ]
        data = self._post("comparisons/retrieve", expect_data=True)["response"]["data"]
        if data is None:
            return pd.DataFrame()
        out = [{key: v[key] for key in export_keys} for v in data]
        out = pd.DataFrame.from_dict(out)
        return out

    def get_comparisons(self, comparison_ids):
        """List comparisons

        Get comparison results

        Args:
            comparison_ids (int, [int]):  one or more sample ids

        Examples:
            >>> # p is a logged in portal session
            >>> p.get_comparisons([4,8])

        Returns:
            DataFrame:
                comparison results from DESeq2. Refer to DESeq2 documentation for column
                description
        """
        if not isinstance(comparison_ids, list):
            comparison_ids = [comparison_ids]
        comparison_ids = _list_to_int_list(comparison_ids)
        data = self._post(
            "comparisons/retrieve",
            {"comparison_ids": comparison_ids, "withData": True},
            expect_data=True,
        )["response"]["data"]
        if len(data) > 0:
            out = {
                str(i): g.drop(columns="comparison_id")
                for i, g in pd.DataFrame.from_dict(data).groupby("comparison_id")
            }
        else:
            out = {}
        return out
