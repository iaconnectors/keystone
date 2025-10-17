"""Simulated Git integration layer."""

import datetime


class GitService:
    """
    Simplified Git service used for demonstrations.
    In production this would rely on GitPython and the GitHub API.
    """

    def __init__(self, repo_name: str = "chroma/synthetica-kb") -> None:
        self.repo_name = repo_name
        print("[GitService] Inicializado em modo de simulacao.")

    def create_feature_branch(self, base_branch: str = "main") -> str:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        branch_name = f"feature/autonomous_update_{timestamp}"
        print(f"[GitService] Criando branch a partir de {base_branch}: {branch_name}")
        return branch_name

    def commit_changes(
        self, file_path: str, commit_message: str, branch_name: str
    ) -> None:
        print(
            "[GitService] Commitando mudancas em "
            f"{branch_name}: \"{commit_message}\" (arquivo: {file_path})"
        )

    def create_pull_request(
        self,
        title: str,
        body: str,
        head_branch: str,
        base_branch: str = "main",
    ) -> str:
        pr_url = f"https://github.com/{self.repo_name}/pull/123"
        print("\n" + "=" * 50)
        print("[GitService] Gerando pull request simulado:")
        print(f"  Base: {base_branch}")
        print(f"  Head: {head_branch}")
        print(f"  Titulo: {title}")
        preview = body[:500] + ("..." if len(body) > 500 else "")
        print(f"  Corpo (preview):\n{preview}")
        print(f"[GitService] Pull request criado: {pr_url}")
        print("=" * 50 + "\n")
        return pr_url
