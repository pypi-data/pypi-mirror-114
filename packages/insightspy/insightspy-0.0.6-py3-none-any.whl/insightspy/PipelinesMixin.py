from insightspy.SessionCore import RequestCore
import pandas as pd


class PipelinesMixin(RequestCore):
    def pipeline_revisions(self):
        """List available pipelines

        Lists pipelines accessible within the current portal session. Pipeline access is
        limited by user id and the current session project if one is set.

        Examples:
            >>> # p is a logged in portal session
            >>> p.pipeline_revisions()

        Returns:
            DataFrame: table of pipeline metadata
        """
        return pd.DataFrame.from_dict(
            self._get("pipelinesDb/project_pipelines_revisions")["response"]["data"]
        )

    def pipeline_config(self, pipeline_id, pipeline_revision = None):
        """Get pipeline configurations

        Loads configurations for a pipeline as a dictionary.

        Args:
            pipeline_id (int): a pipeline_id
            pipeline_revision(int):
                a pipeline revision_id. Defaults to most recent revision if none
                specified

        Returns:
            {config_key: config_value}: dictionary of pipeline configurations
        """
        if pipeline_revision is None:
            x = self._get("pipelinesDb/latest_revision",
                    params={"pipeline_id": pipeline_id})["response"]["data"]
            pipeline_revision = x["revision"]
        out = self._get("pipelinesDb/get_config",
            params={"revision": pipeline_revision,
                "pipeline_id": pipeline_id})["response"]["data"]
        return(out)
