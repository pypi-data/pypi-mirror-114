from insightspy.SessionCore import RequestCore
import pandas as pd


class ProjectsMixin(RequestCore):
    def projects(self):
        """List projects

        Lists projects accessible withthin the current portal session. Project access is
        limited by user id.

        Examples:
            >>> # p is a logged in portal session
            >>> p.projects()

        Returns:
            DataFrame: table of project descriptions and ids
        """
        out = [
            {"project_id": v["project_id"], "description": v["description"]}
            for k, v in self._post("project/retrieve", expect_data=True)["response"][
                "data"
            ].items()
        ]
        return pd.DataFrame.from_dict(out)

    def set_project(self, project_id):
        """Set current project

        Limits resources available in the current session to those accessible from the
        specified `project_id`. See available project ids with
        :meth:`~PortalSession.projects`

        Args:
            project_id (int): project id.

        Examples:
            >>> # p is a logged in portal session
            >>> p.set_project(3)
        """
        self._post("project/session", {"project_id": project_id})
