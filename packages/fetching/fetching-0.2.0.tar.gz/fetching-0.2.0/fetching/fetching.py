import github
import os


class Handler:
    def __init__(self, name: str, auth: str):
        self.name = name
        self.repo = github.Github(auth).get_repo(name)

    def get_file(self, file_path: str, ref: [str, None]):

        try:
            content = \
                self.repo.get_contents(file_path, ref=ref) \
                if ref is not None \
                else self.repo.get_contents(file_path)

            return content.decoded_content.decode("utf-8")
        except github.GithubException:
            print(f"Could not locate file {file_path} in repository {self.name} with ref {ref}.")
            return None

    def get_files_by_ref(self, files: list, ref: [str, None]):

        files = [self.get_file(file, ref) for file in files]
        return [f for f in files if f is not None]

    def _get_ref_for_tag(self, tag: str):

        tags = self.repo.get_tags()
        for t in tags:
            if t.name == tag:
                return t.commit.sha

        return None

    def get_files_by_tag(self, files: list, tag: str):

        ref = self._get_ref_for_tag(tag)
        if ref is None:
            raise ValueError(f"Error: Unable to locate tag {tag} for repository {self.repo.name}.")

        return self.get_files_by_ref(files, ref)


class Fetching:

    @staticmethod
    def resolve_token(token: [str, None]):
        """
        resolve API token according to order of precedence from
        GH docs: https://cli.github.com/manual/gh_help_environment
        """

        if token is not None:
            return token
        elif os.getenv("GH_TOKEN") is not None:
            return os.getenv("GH_TOKEN")
        elif os.getenv("GITHUB_TOKEN") is not None:
            return os.getenv("GITHUB_TOKEN")
        else:
            raise ValueError("Unable to locate GitHub API token.")

    @staticmethod
    def _fetch(target: dict, token: str):

        if target.get("tag") is not None:
            return Handler(target.get("name"), token).get_files_by_tag(target.get("files"), target.get("tag"))
        else:
            return Handler(target.get("name"), token).get_files_by_ref(target.get("files"), target.get("ref"))

    def fetch_requirements(self, targets: list, token: [str, None] = None):

        ret = []
        token = self.resolve_token(token)

        for t in targets:
            t["files"] = ["requirements.txt"]
            ret.extend(self._fetch(t, token))

        return ret

    def fetch_source(self, targets: list, token: [str, None] = None):

        ret = []
        token = self.resolve_token(token)

        for t in targets:
            t["files"] = [f for f in t.get("files", []) if f != "requirements.txt"]
            ret.extend(self._fetch(t, token))

        return ret

    @staticmethod
    def _filter_main(f: str):
        """
        extract contents of file up until main invocation, if it exists
        """

        lines = f.split("\n")
        ret = []
        for l in lines:
            if ("if __name__ == '__main__'" in l) or ("if __name__ == \"__main__\"" in l):
                break
            else:
                ret.append(l)

        return "\n".join(ret)

    def build_dependencies(self, dependencies: list):
        return "\n".join([self._filter_main(d) for d in dependencies])

    @staticmethod
    def build_requirements(requirements: list):
        """
        filter repeats from concatenated requirements.txt file contents
        """

        return "\n".join(
            list(set(
                [lib for file in requirements for lib in file.split("\n") if lib != ""])
            )
        )

    @staticmethod
    def write(dest: str, content: str):
        with open(dest, "w") as out:
            out.write(content)

    def fetch_and_build(self, targets: list, token: [str, None]):

        dependencies = self.fetch_source(targets, token)
        requirements = self.fetch_requirements(targets, token)

        source_code = self.build_dependencies(dependencies)
        source_requirements = self.build_requirements(requirements)

        return [source_code, source_requirements]
