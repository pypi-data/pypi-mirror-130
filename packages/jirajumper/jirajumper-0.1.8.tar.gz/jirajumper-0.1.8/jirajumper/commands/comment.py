from dataclasses import dataclass
from typing import Optional, List

import rich
from documented import DocumentedError
from more_itertools import first
from typer import Argument

from jirajumper.cache.cache import JeevesJiraContext


def comment(
    context: JeevesJiraContext,
    text: str = Argument(...),
):
    """Comment an issue."""
    issue = context.obj.current_issue
    jira = context.obj.jira

    jira.add_comment(
        issue=issue.key,
        body=text,
    )

    rich.print('💬 Commented.')
