import requests
import typing as t
import datetime


class GitLabClient:
    def __init__(
        self,
        *,
        project_id: str,
        api_token: str,
        base_api_url: str = "https://gitlab.com/api/v4",
    ):
        self.api = "".join([base_api_url, "/projects/", project_id])
        self.headers = {"Authorization": f"Bearer {api_token}"}

        def construct_method(
            name: str,
        ) -> t.Callable[[GitLabClient, str, t.Optional[dict[str, t.Any]]], requests.Response]:
            def _request(
                cls: GitLabClient, path: str, params: t.Optional[dict[str, t.Any]] = None
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
        r = self.get(
            "/merge_requests",
            {
                "state": "opened",
                "wip": "no",
                "target_branch": "main",
                "with_merge_status_recheck": "true",
            },
        )
        mrs = r.json()
        mr_iids = [mr["iid"] for mr in mrs]
        return mr_iids

    def get_branches_to_compound(
        self, with_migrations: bool = True, with_pipeline: bool = False
    ) -> list[str]:
        branches = []
        mr_iids = self.get_mr_candidates()
        for mr_iid in mr_iids:
            r = self.get(f"/merge_requests/{mr_iid}")
            mr = r.json()
            if mr["merge_status"] != "can_be_merged":
                continue
            if not with_migrations:
                if "migrations" in r.json()["labels"]:
                    continue
            if with_pipeline:
                if mr["head_pipeline"]["status"] != "success":
                    continue
            branches.append(mr["source_branch"])
        return branches

    def create_compound_branch(self) -> requests.Response:
        r = self.delete("/repository/branches/compound")
        r = self.post(
            "/repository/branches",
            {
                "branch": "compound",
                "ref": "main",
            },
        )
        return r

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

    def compound(self):
        branches = self.get_branches_to_compound()
        print(branches)
        new_mrs = self.open_clone_mrs(branches)

        for new_mr in new_mrs:
            r = self.put(
                f"/merge_requests/{new_mr}/merge",
            )
            print(r.status_code)
            # Add manual action here to check if they need conflict resolution

        # Create compound merge request on main
        time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        branches_str = ", ".join(branches)
        r = self.post(
            "/merge_requests",
            {
                "source_branch": "compound",
                "target_branch": "main",
                "title": f"Draft: {time}. Branches: {branches_str}.",
                "description": "none",
                "labels": "compound",
            },
        )
        print(r.status_code)


# client = GitLabClient(project_id=PROJECT_ID, api_token=TOKEN)


# client.compound()
