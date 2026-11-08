"""Set up the practice issues, pull requests, release and discussion.

Run by the "Set up practice" workflow. It reads GITHUB_TOKEN, GITHUB_REPOSITORY
and GITHUB_ACTOR from the environment, and uses only the standard library.

Every step checks first and makes nothing twice, so the workflow can run again
at any time to put back what someone has closed or deleted.
"""

import base64
import io
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile

API = "https://api.github.com"
UPLOADS = "https://uploads.github.com"
TOKEN = os.environ["GITHUB_TOKEN"]
REPO = os.environ["GITHUB_REPOSITORY"]
ACTOR = os.environ.get("GITHUB_ACTOR", "")
OWNER, NAME = REPO.split("/", 1)

MILESTONE = "Practice milestone 1"
LINE_BRANCH = "practice/line-count"
SPEED_BRANCH = "practice/speed-up-word-counting"
TAG = "v0.1.0"

made = []
skipped = []
problems = []


class GitHubError(Exception):
    def __init__(self, status, message):
        super().__init__(f"{status}: {message}")
        self.status = status
        self.message = message


def call(method, path, body=None, base=API, data=None, content_type="application/json"):
    url = path if path.startswith("http") else base + path
    if body is not None:
        data = json.dumps(body).encode("utf-8")
    request = urllib.request.Request(url, data=data, method=method)
    request.add_header("Authorization", f"Bearer {TOKEN}")
    request.add_header("Accept", "application/vnd.github+json")
    request.add_header("X-GitHub-Api-Version", "2022-11-28")
    if data is not None:
        request.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read()
    except urllib.error.HTTPError as error:
        try:
            message = json.loads(error.read()).get("message", "")
        except ValueError:
            message = error.reason
        raise GitHubError(error.code, message) from None
    return json.loads(raw) if raw else None


def graphql(query, **variables):
    result = call("POST", "/graphql", {"query": query, "variables": variables})
    if result.get("errors"):
        raise GitHubError(0, result["errors"][0].get("message", "GraphQL error"))
    return result["data"]


def all_pages(path):
    items = []
    page = 1
    joiner = "&" if "?" in path else "?"
    while True:
        batch = call("GET", f"{path}{joiner}per_page=100&page={page}")
        items.extend(batch)
        if len(batch) < 100:
            return items
        page += 1


def read(path):
    with open(path, encoding="utf-8") as handle:
        return handle.read()


# -- labels and milestone ---------------------------------------------------

LABELS = {
    "bug": ("d73a4a", "Something isn't working"),
    "documentation": ("0075ca", "Improvements or additions to documentation"),
    "enhancement": ("a2eeef", "New feature or request"),
    "good first issue": ("7057ff", "Good for newcomers"),
    "question": ("d876e3", "Further information is requested"),
    "accessibility": ("1d76db", "Affects people using assistive technology"),
}


def ensure_labels():
    existing = {label["name"].lower() for label in all_pages(f"/repos/{REPO}/labels")}
    for name, (color, description) in LABELS.items():
        if name.lower() in existing:
            continue
        call("POST", f"/repos/{REPO}/labels",
             {"name": name, "color": color, "description": description})
        made.append(f"Label: {name}")


def ensure_milestone():
    for milestone in all_pages(f"/repos/{REPO}/milestones?state=all"):
        if milestone["title"] == MILESTONE:
            return milestone["number"]
    milestone = call("POST", f"/repos/{REPO}/milestones", {
        "title": MILESTONE,
        "description": "Issues to practise milestones with. Nothing is due.",
    })
    made.append(f"Milestone: {MILESTONE}")
    return milestone["number"]


# -- issues -------------------------------------------------------------------

ISSUES = [
    {
        "title": "Word count is off by one when text ends with a space",
        "labels": ["bug"],
        "milestone": True,
        "assign": True,
        "body": (
            "## What happened\n\n"
            "`word_count(\"hello world \")` returns 3. There are only two words.\n\n"
            "## What I expected\n\n"
            "2. A space at the end of the text shouldn't count as a word.\n\n"
            "## How to see it\n\n"
            "1. Run `python -c \"import sys; sys.path.insert(0, 'src'); "
            "import tally; print(tally.word_count('hello world '))\"`\n"
            "2. It prints 3.\n\n"
            "The same happens with two spaces between words."
        ),
        "comments": [
            "I think this is because `word_count` splits on a single space, so "
            "each extra space makes an empty word. `text.split()` with no "
            "argument would fix it.",
        ],
    },
    {
        "title": "Add a line count to the summary",
        "labels": ["enhancement", "good first issue"],
        "milestone": True,
        "body": (
            "It would help to know how many lines a piece of text has, as well "
            "as words and characters.\n\n"
            "- Add a `line_count(text)` function.\n"
            "- Empty text should have no lines.\n"
            "- Text with no line breaks is one line.\n\n"
            "There's a pull request for this: \"Add a line count\"."
        ),
        "comments": [],
    },
    {
        "title": "CONTRIBUTING should explain how to write a test",
        "labels": ["documentation"],
        "body": (
            "CONTRIBUTING.md says to add a test with each change, but not where "
            "the tests live or how they're named. A short example would help "
            "someone making their first pull request."
        ),
        "comments": [],
    },
    {
        "title": "Question: what counts as a word?",
        "labels": ["question"],
        "body": (
            "Should `tally` count \"screen-reader\" as one word or two? And what "
            "about numbers, such as \"3.5\"? I'd like to agree on this before "
            "anyone changes `word_count`."
        ),
        "comments": [
            "One word for \"screen-reader\", I think. Most word processors "
            "count a hyphenated word once.",
            "Agreed on hyphens. Numbers should count as words too, so \"3.5 "
            "miles\" is two words.",
            "That's settled, then: hyphenated words and numbers each count "
            "once. The docstring for `word_count` already says so for hyphens.",
        ],
        "react_first_comment": ["+1", "heart"],
    },
    {
        "title": "Typo in the module docstring",
        "labels": ["documentation"],
        "body": "The module docstring said \"cound\" where it meant \"count\".",
        "comments": ["Fixed on main."],
        "close": True,
    },
    {
        "title": "Count sentences as well as words",
        "labels": ["enhancement"],
        "body": (
            "A sentence count would be useful for checking readability. It "
            "could count full stops, question marks and exclamation marks "
            "that end a sentence."
        ),
        "comments": [],
    },
]


def ensure_issues(milestone_number):
    existing = {}
    for issue in all_pages(f"/repos/{REPO}/issues?state=all"):
        if "pull_request" not in issue:
            existing[issue["title"]] = issue
    numbers = {}
    for spec in ISSUES:
        issue = existing.get(spec["title"])
        if issue is not None:
            numbers[spec["title"]] = issue["number"]
            if spec.get("close") or issue["state"] == "open":
                skipped.append(f"Issue already there: {spec['title']}")
                continue
            call("PATCH", f"/repos/{REPO}/issues/{issue['number']}", {"state": "open"})
            made.append(f"Reopened issue: {spec['title']}")
            continue
        body = {"title": spec["title"], "body": spec["body"], "labels": spec["labels"]}
        if spec.get("milestone"):
            body["milestone"] = milestone_number
        if spec.get("assign") and ACTOR:
            body["assignees"] = [ACTOR]
        try:
            issue = call("POST", f"/repos/{REPO}/issues", body)
        except GitHubError as error:
            if "assignees" not in body:
                raise
            # The person running the workflow may not be assignable here.
            del body["assignees"]
            issue = call("POST", f"/repos/{REPO}/issues", body)
            problems.append(f"Couldn't assign {ACTOR}: {error.message}")
        numbers[spec["title"]] = issue["number"]
        first_comment = None
        for text in spec["comments"]:
            comment = call("POST", f"/repos/{REPO}/issues/{issue['number']}/comments",
                           {"body": text})
            first_comment = first_comment or comment
        for reaction in spec.get("react_first_comment", []):
            if first_comment is not None:
                call("POST",
                     f"/repos/{REPO}/issues/comments/{first_comment['id']}/reactions",
                     {"content": reaction})
        if spec.get("close"):
            call("PATCH", f"/repos/{REPO}/issues/{issue['number']}",
                 {"state": "closed", "state_reason": "completed"})
        made.append(f"Issue #{issue['number']}: {spec['title']}")
    return numbers


# -- branches and pull requests -------------------------------------------

LINE_COUNT_CODE = '''

def line_count(text):
    """Return how many lines *text* holds."""
    return len(text.split("\\n"))
'''

LINE_COUNT_TEST = '''

class LineCountTests(unittest.TestCase):
    def test_counts_lines(self):
        self.assertEqual(tally.line_count("one\\ntwo"), 2)
'''

SPEED_OLD = '    return len(text.split(" "))\n'
SPEED_NEW = '    return len(text.replace("-", " ").split())\n'


def default_branch_sha():
    repo = call("GET", f"/repos/{REPO}")
    branch = repo["default_branch"]
    ref = call("GET", f"/repos/{REPO}/git/ref/heads/{urllib.parse.quote(branch)}")
    return branch, ref["object"]["sha"]


def branch_exists(name):
    try:
        call("GET", f"/repos/{REPO}/git/ref/heads/{name}")
        return True
    except GitHubError as error:
        if error.status == 404:
            return False
        raise


def put_file(branch, path, text, message):
    current = call("GET", f"/repos/{REPO}/contents/{path}?ref={urllib.parse.quote(branch)}")
    call("PUT", f"/repos/{REPO}/contents/{path}", {
        "message": message,
        "content": base64.b64encode(text.encode("utf-8")).decode("ascii"),
        "sha": current["sha"],
        "branch": branch,
    })


def make_branch(name, base_sha, changes):
    if branch_exists(name):
        skipped.append(f"Branch already there: {name}")
        return
    call("POST", f"/repos/{REPO}/git/refs", {"ref": f"refs/heads/{name}", "sha": base_sha})
    for path, text, message in changes:
        put_file(name, path, text, message)
    made.append(f"Branch: {name}")


def open_pull(head, base, title, body, draft=False):
    for pull in all_pages(f"/repos/{REPO}/pulls?state=all&head={OWNER}:{head}"):
        if pull["state"] == "open":
            skipped.append(f"Pull request already there: {title}")
            return pull, False
        if pull["merged_at"] is None:
            call("PATCH", f"/repos/{REPO}/pulls/{pull['number']}", {"state": "open"})
            made.append(f"Reopened pull request: {title}")
            return pull, False
        # Merged already: the branch is spent, so leave it be.
        skipped.append(f"Pull request already merged: {title}")
        return pull, False
    pull = call("POST", f"/repos/{REPO}/pulls",
                {"head": head, "base": base, "title": title, "body": body, "draft": draft})
    made.append(f"Pull request #{pull['number']}: {title}")
    return pull, True


def review_line_count(pull):
    code = read("src/tally/__init__.py") + LINE_COUNT_CODE
    target = '    return len(text.split("\\n"))'
    line = code.splitlines().index(target) + 1
    tests = read("tests/test_tally.py")
    cut = tests.index("\n\nif __name__")
    new_tests = tests[:cut] + LINE_COUNT_TEST + tests[cut:]
    test_target = '        self.assertEqual(tally.line_count("one\\ntwo"), 2)'
    test_line = new_tests.splitlines().index(test_target) + 1
    call("POST", f"/repos/{REPO}/pulls/{pull['number']}/reviews", {
        "commit_id": pull["head"]["sha"],
        "event": "COMMENT",
        "body": (
            "Thanks for this. One thing to fix before it's merged: the issue "
            "says empty text should have no lines."
        ),
        "comments": [
            {
                "path": "src/tally/__init__.py",
                "line": line,
                "side": "RIGHT",
                "body": (
                    "`\"\".split(\"\\n\")` gives `['']`, so empty text counts as "
                    "one line. `splitlines()` handles that, and Windows line "
                    "endings too:\n\n"
                    "```suggestion\n"
                    "    if not text:\n"
                    "        return 0\n"
                    "    return len(text.splitlines())\n"
                    "```"
                ),
            },
            {
                "path": "tests/test_tally.py",
                "line": test_line,
                "side": "RIGHT",
                "body": "Could you add a test for empty text as well?",
            },
        ],
    })
    made.append("Review with a suggested change on: Add a line count")


def run_tests_on(branch):
    try:
        call("POST", f"/repos/{REPO}/actions/workflows/tests.yml/dispatches", {"ref": branch})
        made.append(f"Started the Tests workflow on {branch}")
    except GitHubError as error:
        problems.append(f"Couldn't start the Tests workflow on {branch}: {error.message}")


def ensure_pulls(numbers):
    base, base_sha = default_branch_sha()
    code = read("src/tally/__init__.py")
    tests = read("tests/test_tally.py")
    tests_main = tests.index("\n\nif __name__")
    make_branch(LINE_BRANCH, base_sha, [
        ("src/tally/__init__.py", code + LINE_COUNT_CODE, "Add line_count"),
        ("tests/test_tally.py",
         tests[:tests_main] + LINE_COUNT_TEST + tests[tests_main:],
         "Test line_count"),
    ])
    make_branch(SPEED_BRANCH, base_sha, [
        ("src/tally/__init__.py", code.replace(SPEED_OLD, SPEED_NEW),
         "Count words with one split"),
    ])
    line_issue = numbers.get("Add a line count to the summary")
    closes = f"\n\nCloses #{line_issue}." if line_issue else ""
    try:
        pull, new = open_pull(
            LINE_BRANCH, base, "Add a line count",
            "Adds `line_count(text)`, with a test." + closes)
        if new:
            review_line_count(pull)
        run_tests_on(LINE_BRANCH)
        open_pull(
            SPEED_BRANCH, base, "Speed up word counting",
            "Splits the text once instead of on every space.\n\n"
            "This is a draft because a test fails, and I'm not sure why yet.",
            draft=True)
        run_tests_on(SPEED_BRANCH)
    except GitHubError as error:
        if error.status == 403:
            problems.append(
                "GitHub Actions isn't allowed to open pull requests in this "
                "repository. Turn on Settings > Actions > General > Workflow "
                "permissions > Allow GitHub Actions to create and approve pull "
                "requests, save, and run Set up practice again."
            )
        else:
            raise


# -- release ------------------------------------------------------------------

def ensure_release():
    try:
        call("GET", f"/repos/{REPO}/releases/tags/{TAG}")
        skipped.append(f"Release already there: {TAG}")
        return
    except GitHubError as error:
        if error.status != 404:
            raise
    _, sha = default_branch_sha()
    release = call("POST", f"/repos/{REPO}/releases", {
        "tag_name": TAG,
        "target_commitish": sha,
        "name": "Tally 0.1.0",
        "body": (
            "The first release of Tally.\n\n"
            "- `word_count`, `character_count` and `summary`.\n"
            "- Known problem: text that ends with a space counts one word too "
            "many. See the issue \"Word count is off by one when text ends "
            "with a space\".\n\n"
            "The attached file holds the source and the tests."
        ),
    })
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in ("README.md", "LICENSE", "src/tally/__init__.py", "tests/test_tally.py"):
            archive.write(path, f"tally-0.1.0/{path}")
    upload = release["upload_url"].split("{", 1)[0]
    call("POST", f"{upload}?name=tally-0.1.0.zip", data=buffer.getvalue(),
         content_type="application/zip")
    made.append(f"Release {TAG} with tally-0.1.0.zip attached")


# -- discussion ---------------------------------------------------------------

DISCUSSION_TITLE = "Welcome: say hello and ask anything"


def ensure_discussion():
    data = graphql(
        """query($owner: String!, $name: String!) {
          repository(owner: $owner, name: $name) {
            id
            hasDiscussionsEnabled
            discussionCategories(first: 25) { nodes { id name } }
            discussions(first: 50) { nodes { title } }
          }
        }""",
        owner=OWNER, name=NAME,
    )["repository"]
    if not data["hasDiscussionsEnabled"]:
        problems.append(
            "Discussions are off in this repository, so no discussion was made. "
            "Turn on Settings > General > Features > Discussions and run Set up "
            "practice again."
        )
        return
    if any(node["title"] == DISCUSSION_TITLE for node in data["discussions"]["nodes"]):
        skipped.append(f"Discussion already there: {DISCUSSION_TITLE}")
        return
    categories = {node["name"]: node["id"] for node in data["discussionCategories"]["nodes"]}
    category = categories.get("General") or next(iter(categories.values()), None)
    if category is None:
        problems.append("This repository has no discussion categories, so no discussion was made.")
        return
    discussion = graphql(
        """mutation($repo: ID!, $category: ID!, $title: String!, $body: String!) {
          createDiscussion(input: {repositoryId: $repo, categoryId: $category,
                                   title: $title, body: $body}) {
            discussion { id }
          }
        }""",
        repo=data["id"], category=category, title=DISCUSSION_TITLE,
        body=(
            "This is the place to practise discussions. Reply to say hello, "
            "or ask a question about GitHub, QUILL or QUILL Lite. Replies "
            "can have replies of their own, so you can practise moving through "
            "a thread too."
        ),
    )["createDiscussion"]["discussion"]
    for text in (
        "Hello! I'm practising with QUILL Lite.",
        "Welcome. Try replying to this comment to start a thread of its own.",
    ):
        graphql(
            """mutation($id: ID!, $body: String!) {
              addDiscussionComment(input: {discussionId: $id, body: $body}) {
                comment { id }
              }
            }""",
            id=discussion["id"], body=text,
        )
    made.append(f"Discussion: {DISCUSSION_TITLE}")


# -- summary --------------------------------------------------------------

def write_summary():
    lines = ["# Practice setup", ""]
    if problems:
        lines += ["## Needs your attention", ""]
        lines += [f"- {text}" for text in problems] + [""]
    lines += ["## Made this time", ""]
    lines += [f"- {text}" for text in made] or ["- Nothing: everything was already there."]
    if skipped:
        lines += ["", "## Already there", ""] + [f"- {text}" for text in skipped]
    text = "\n".join(lines) + "\n"
    print(text)
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as handle:
            handle.write(text)


def main():
    steps = (
        ("labels", ensure_labels),
        ("milestone", None),
        ("issues", None),
        ("pull requests", None),
        ("release", ensure_release),
        ("discussion", ensure_discussion),
    )
    milestone_number = None
    numbers = {}
    for name, step in steps:
        try:
            if name == "milestone":
                milestone_number = ensure_milestone()
            elif name == "issues":
                numbers = ensure_issues(milestone_number)
            elif name == "pull requests":
                ensure_pulls(numbers)
            else:
                step()
        except GitHubError as error:
            problems.append(f"The {name} step failed: {error}")
    write_summary()
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
