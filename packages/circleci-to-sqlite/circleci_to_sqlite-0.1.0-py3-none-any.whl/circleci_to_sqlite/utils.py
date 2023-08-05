import requests


def make_session(token):
    session = requests.Session()
    session.auth = requests.auth.HTTPBasicAuth(token, "")
    session.headers.update({"Accept": "application/json"})
    return session


def fetch_projects(token):
    session = make_session(token)
    response = session.get("https://circleci.com/api/v1.1/projects")
    response.raise_for_status()
    return response.json()


def fetch_jobs(project_slug, token):
    session = make_session(token)
    vcs_type, user, repo = project_slug.split("/")
    url = f"https://circleci.com/api/v1.1/project/{vcs_type}/{user}/{repo}"
    response = session.get(url)
    response.raise_for_status()
    return response.json()


def fetch_job(project_slug, build_num, token):
    session = make_session(token)
    vcs_type, user, repo = project_slug.split("/")
    url = f"https://circleci.com/api/v1.1/project/{vcs_type}/{user}/{repo}/{build_num}"
    response = session.get(url)
    response.raise_for_status()
    return response.json()


def save_projects(db, projects):
    for original in projects:
        project = {
            "vcs_type": original["vcs_type"],
            "username": original["username"],
            "reponame": original["reponame"],
        }
        # Delete existing project
        existing = list(
            db["projects"].rows_where(
                "vcs_type = ? and username = ? and reponame = ?",
                [project["vcs_type"], project["username"], project["reponame"]],
            ),
        )
        if existing:
            existing_id = existing[0]["id"]
            # TODO
            # db["measurements"].delete_where("diary_entry = ?", [existing_id])
            db["projects"].delete_where("id = ?", [existing_id])
        db["projects"].insert(
            project,
            pk="id",
            alter=True,
            column_order=["id", "vcs_type", "username", "reponame"],
            columns={"notes": str},
        )
        db["projects"].create_index(
            ["vcs_type", "username", "reponame"], unique=True, if_not_exists=True
        )


@cli.command()
@click.argument(
    "db_path",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=False),
    required=True,
)
@click.option(
    "-a",
    "--auth",
    type=click.Path(file_okay=True, dir_okay=False, allow_dash=True),
    default="auth.json",
    help="Path to auth.json token file",
)
# @click.option(
#     "--load",
#     type=click.Path(file_okay=True, dir_okay=False, allow_dash=True, exists=True),
#     help="Load projects JSON from this file instead of the API",
# )
def projects(db_path, auth):
    "Save all projects followed by the current user"
    db = sqlite_utils.Database(db_path)
    token = load_token(auth)
    projects = utils.fetch_projects(token)
    utils.save_projects(db, projects)
    # if load:
    #     issues = json.load(open(load))
    # else:
    #     issues = utils.fetch_issues(repo, token, issue_ids)

    # issues = list(issues)
    # utils.save_issues(db, issues, repo_full)
    # utils.ensure_db_shape(db)


def load_token(auth):
    try:
        token = json.load(open(auth))["circleci_personal_token"]
    except (KeyError, FileNotFoundError):
        token = None
    if token is None:
        # Fallback to CIRCLECI_TOKEN environment variable
        token = os.environ.get("CIRCLECI_TOKEN") or None
    return token
