import re
import sys

from gitflow_linter.report import Section, Issue
from gitflow_linter.repository import Repository
from gitflow_linter.rules import Gitflow
from gitflow_linter.visitor import BaseVisitor, arguments_checker


class Author:
    def __init__(self, name, email):
        self.original_name = name
        self.name = Author.__escape_name(name)
        self.email = email

    def __eq__(self, other):
        return isinstance(other, Author) and (other.name == self.name or other.email == self.email)

    def __hash__(self):
        return hash('little hack to force the use of eq')

    def __repr__(self):
        return 'Author(name=' + self.name + ', email=' + self.email + ')'

    def __str__(self):
        return "{name} <{email}>".format(name=self.original_name, email=self.email)

    @staticmethod
    def __escape_name(name):
        regex = re.compile('[^a-zA-Z]')
        return regex.sub('', name).lower()


class NoMultipleFeaturesPerAuthorVisitor(BaseVisitor):

    @property
    def rule(self) -> str:
        return 'no_multiple_open_features_per_author'

    @arguments_checker(['max_open_branches_per_author'])
    def visit(self, repo: Repository, *args, **kwargs) -> Section:
        section = Section(rule=self.rule, title='Checked if there are authors who have multiple not closed features')
        all_features = repo.branches(folder=self.gitflow.features) + repo.branches(folder=self.gitflow.fixes)
        merged_branches = repo.raw_query(lambda git: git.branch('-r', '--merged', repo.develop.name))
        not_merged = [branch for branch in all_features if branch.name not in merged_branches]
        authors = set()
        branches_per_authors = dict()

        for branch in not_merged:
            branch_authors = set([Author(name=commit.author.name, email=commit.author.email) for commit in
                                  repo.unique_commits_for_branch(branch)])
            branches_per_authors[branch.name] = branch_authors
            authors.update(branch_authors)

        for author in authors:
            count = len([branch for branch in branches_per_authors.keys() if author in branches_per_authors[branch]])
            if count > max(1, int(kwargs["max_open_branches_per_author"])):
                participated_branches = [branch for branch, authors in branches_per_authors.items() if
                                         author in authors]
                section.append(
                    Issue.error('{author} participates in {count} ongoing feature branches: {branches}'
                                .format(author=author, count=count, branches=', '.join(participated_branches)))
                )

        return section


def visitors(gitflow: Gitflow) -> list:
    return [NoMultipleFeaturesPerAuthorVisitor(gitflow=gitflow)]


def main():
    """
    This is how you can test/run your plugin as a standalone script:
    `python __init__.py /path/to/git/repo /path/to/settings.yaml`
    """
    import gitflow_linter
    from git import Repo  # GitPython
    with open(sys.argv[2], 'r') as file:
        gitflow, rules = gitflow_linter.parse_yaml(file)
    repo = gitflow_linter.repository.Repository(Repo(sys.argv[1]), gitflow=gitflow)
    visitor = NoMultipleFeaturesPerAuthorVisitor(gitflow=gitflow)
    kwargs = rules.args_for(visitor.rule)
    print(repo.apply(visitor, **kwargs).issues)


if __name__ == '__main__':
    main()
