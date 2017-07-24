# coding=utf-8
import re


class SimpleParser:
    """
    Принимает шаблон письма и разбивает его на части (SUBJECT, CONTENT, HTML)
    """

    result = {}

    def __init__(self, template):
        parse_dict = {}

        index = "_DEFAULT"
        for line in template.split("\n"):
            r = re.search(r"^\[([A-Za-z0-9_]+)\]$", line.strip())
            if r:
                index = r.group(1)
                parse_dict[index] = ""
            else:
                parse_dict[index] += line + "\n"

        self.result = {k: v.strip() for k, v in parse_dict.iteritems()}

    def get(self, key):
        return self.result.get(key)
