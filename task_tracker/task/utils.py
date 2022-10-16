import re
from random import randint


def select_random_element(iterable):
    random_ix = randint(0, len(iterable) - 1)
    return iterable[random_ix]


TITLE_REGEX = re.compile(r"^([A-Z]+-\d+)([^\w]+)(.*)")


def parse_title(title: str):
    res = TITLE_REGEX.match(title)
    if not res:
        return None, title

    jira_id, _, title = res.groups()

    return jira_id, title
