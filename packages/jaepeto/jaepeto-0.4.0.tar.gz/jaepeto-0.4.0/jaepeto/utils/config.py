"""
Parse user config
"""
import os
from configparser import ConfigParser, NoOptionError
from pathlib import Path
from typing import Union


def _clean_config_dir(value: str) -> str:
    """
    Remove errant / and . from directory values in config.

    Leading `./` and trailing `/`
    are to be removed as the code does not expect paths
    in this format and consequently cannot resolve the paths.

    Parameters
    ----------
    value : str
        The unclean directory

    Returns
    -------
    str
        A clean directory
    """
    value = value.lstrip("./")
    value = value.rstrip("/")
    return value


def parse_config(config_file: Union[Path, str]):
    config = ConfigParser()
    config.read(config_file)

    project_name = config.get("project", "name")
    project_name = project_name if project_name else "Project"

    project_info = {
        "name": project_name,
        "description": config.get("project", "description"),
        "src": _clean_config_dir(config.get("project", "srcdir")),
        "doc_dir": _clean_config_dir(config.get("docs", "docdir")),
    }

    try:
        local = config.getboolean("project", "local")
    except NoOptionError:
        local = False

    os.environ["JAEPETO_API_KEY"] = config.get("project", "api_key")
    os.environ["JAEPETO_PROJECT_NAME"] = project_name
    os.environ["JAEPETO_RUN_LOCALLY"] = str(local)

    language = config.get("project", "language")

    if language.lower().strip().rstrip("3") != "python":
        raise RuntimeError(
            f"""Jaepeto currently only works
        on Python (3), not {language}"""
        )

    # Documentation
    project_info["docs"] = {"technical": True, "technical_name": "technical_doc"}

    # Issues
    if config.has_section("issues"):
        issue_service = config.get("issues", "integration")
        if issue_service and issue_service.lower() != "github":
            project_info["issues"] = {}
        else:
            try:
                username = config.get("issues", "username")
                repo = config.get("issues", "repo")
            except:
                project_info["issues"] = {}
            else:
                project_info["issues"] = {"username": username, "repo": repo}
    else:
        project_info["issues"] = {}

    return project_info


def create_config():
    """
    Create a minimal config file.

    Must be called when project root is current working directory.
    Some information must be filled out by a user, such as `api_key`.
    `srcdir` is assumed to be `src` or just home directory.

    Notes
    -----
    * Writes config file to CWD / ".jaepeto.ini"
    """
    project = Path.cwd()
    config_path = project / ".jaepeto.ini"

    if config_path.exists():
        print(".jaepeto.ini already exists!")
        return

    config = ConfigParser()

    project_name = project.stem

    if (project / "src").is_dir():
        srcdir = "src"
    else:
        srcdir = "."

    config.add_section("project")
    config.set("project", "name", project_name)
    config.set("project", "description", "<ENTER SHORT PROJECT DESCRIPTION>")
    config.set("project", "language", "python")
    config.set("project", "api_key", "<ADD API KEY HERE>")
    config.set("project", "srcdir", srcdir)

    config.add_section("docs")
    config.set("docs", "docdir", "./")

    print(f"Creating config file at {config_path}")
    with open(config_path, "w") as f:
        config.write(f)
