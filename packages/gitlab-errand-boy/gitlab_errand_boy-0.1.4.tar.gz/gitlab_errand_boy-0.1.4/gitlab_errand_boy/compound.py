import requests
import typing as t
import datetime


class Compounder:
    def __init__(
        self,
        *,
        project_id: str,
        api_token: str,
        base_api_url: str = "https://gitlab.com/api/v4",
        with_migrations: bool = False,
        with_pipeline: bool = True,
        target_branch: str = "main",
        use_wip: bool = False,
    ):
        """Compounder GitLab client.

        Args:
            project_id: Either numeric gitlab project id (preferred) or url-encoded name
                of the project.
            api_token: GitLab API token.
            base_api_url: Change if self-hosted. Defaults to "https://gitlab.com/api/v4".
            with_migrations: Use MRs with label `migrations` on them. Defaults to False.
            with_pipeline: Pipelines for individual MRs should be with status `passed`.
                Defaults to True.
            target_branch: Main branch to run compound job for.
            use_wip: Use ONLY MRs with `Draft:` prefix
        """
        self.api = "".join([base_api_url, "/projects/", project_id])
        self.headers = {"Authorization": f"Bearer {api_token}"}
        self.with_migrations = with_migrations
        self.with_pipeline = with_pipeline
        self.target_branch = target_branch
        self.use_wip = use_wip

        def construct_method(
            name: str,
        ) -> t.Callable[[Compounder, str, t.Optional[dict[str, t.Any]]], requests.Response]:
            def _request(
                cls: Compounder, path: str, params: t.Optional[dict[str, t.Any]] = None
            ) -> requests.Response:
                response = requests.request(
                    name.capitalize(), self.api + path, headers=self.headers, params=params
                )
                return response

            return _request

        for method in ["get", "post", "put", "delete"]:
            setattr(self.__class__, method, construct_method(method))

    # These are for mypy
    def get(self, path: str, params: t.Optional[dict[str, t.Any]] = None) -> requests.Response:
        ...

    def post(self, path: str, params: t.Optional[dict[str, t.Any]] = None) -> requests.Response:
        ...

    def put(self, path: str, params: t.Optional[dict[str, t.Any]] = None) -> requests.Response:
        ...

    def delete(self, path: str, params: t.Optional[dict[str, t.Any]] = None) -> requests.Response:
        ...

    def get_mr_candidates(self) -> list[int]:
        query = {
            "state": "opened",
            "wip": "no",
            "target_branch": self.target_branch,
            "with_merge_status_recheck": "true",
        }
        if self.use_wip:
            query["wip"] = "yes"
        r = self.get("/merge_requests", query)
        mrs = r.json()
        mr_iids = [mr["iid"] for mr in mrs]
        return mr_iids

    def get_branches(self) -> list[str]:
        """Get names of branches eligible for composition.

        Does not perform any destructive calls.

        Returns:
            List of branch names.
        """
        branches = []
        mr_iids = self.get_mr_candidates()
        for mr_iid in mr_iids:
            r = self.get(f"/merge_requests/{mr_iid}")
            mr = r.json()
            if mr["merge_status"] != "can_be_merged":
                continue
            if not self.with_migrations:
                if "migrations" in r.json()["labels"]:
                    continue
            if self.with_pipeline:
                if mr["head_pipeline"]["status"] != "success":
                    continue
            branches.append(mr["source_branch"])
        return branches

    def create_compound_branch(self) -> None:
        """Create compound branch.

        Delete `compound` branch if exists and create a new one from main branch.
        """
        r = self.delete("/repository/branches/compound")
        r = self.post(
            "/repository/branches",
            {
                "branch": "compound",
                "ref": self.target_branch,
            },
        )

    def open_clone_mrs(self, branches: list[str]) -> list[int]:
        self.create_compound_branch()
        new_mrs = []

        for branch in branches:
            import random

            r = self.post(
                "/merge_requests",
                {
                    "source_branch": branch,
                    "target_branch": "compound",
                    "title": f"THIS IS CLONE MR. {branch}. Random id: {random.randint(1, 1000)}",
                },
            )
            try:
                new_mr = r.json()["iid"]
                new_mrs.append(new_mr)
            except:
                pass
        return new_mrs

    def compound(self) -> None:
        """Runs the full cycle of creating compound MR."""
        branches = self.get_branches()
        print(branches)
        new_mrs = self.open_clone_mrs(branches)

        for new_mr in new_mrs:
            r = self.put(
                f"/merge_requests/{new_mr}/merge",
            )
            # Add manual action here to check if they need conflict resolution

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        branches_str = ", ".join(branches)
        r = self.post(
            "/merge_requests",
            {
                "source_branch": "compound",
                "target_branch": self.target_branch,
                "title": f"Draft: {time}. Branches: {branches_str}.",
                "description": "none",
                "labels": "compound",
            },
        )


# client = GitLabClient(project_id=PROJECT_ID, api_token=TOKEN)


# client.compound()
