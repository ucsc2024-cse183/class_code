#!/bin/env python

import os
import shutil
import subprocess
import sys
import traceback
from importlib.machinery import SourceFileLoader

import mechanize
from bs4 import BeautifulSoup as Soup


class colors:
    TYPE = "\033[94m"
    OK = "\033[92m"
    WARN = "\033[93m"
    FAIL = "\033[91m"
    END = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def get_git_root():
    """return the root of the repo or None if not in a repo"""
    try:
        ret = subprocess.run(
            "git rev-parse --show-toplevel", shell=True, capture_output=True, check=True
        )
    except:
        return None
    return ret.stdout.decode("UTF8").strip()


def split_repo_path(path=None):
    """return the repo root and the the cwd relative to it"""
    root = get_git_root()
    if not root:
        return None
    return root, os.path.relpath(path or os.getcwd(), root)


def get_repo_info():
    """returns the origin url, name of the org, and name of the repo in a dict"""
    ret = subprocess.run(
        "git config --get remote.origin.url",
        shell=True,
        capture_output=True,
        check=True,
    )
    url = ret.stdout.decode("UTF8").strip()
    if url.startswith("git@"):
        org, name = url.split(":")[1][:-4].split("/")[-2:]
    else:
        org, name = url.split("/")[-2:]
    if name.endswith(".git"):
        name = name[:-4]
    ret = subprocess.run(
        "git rev-parse --abbrev-ref HEAD", shell=True, capture_output=True, check=True
    )
    branch = ret.stdout.decode().strip()
    return {"org": org, "name": name, "url": url, "branch": branch}


def check_student_repo(override):
    """
    check this command is being executed in a valid student repo and prints a report.
    returns the relative path
    """
    root, path = split_repo_path()
    info = path and get_repo_info()
    if not override:
        if info and info["name"] == "class_code":
            print(
                colors.FAIL
                + "Error: You are class_code repo, not your personal class repo"
                + colors.END
            )
            sys.exit(1)
        if not (
            info and info["name"].endswith("-code") and info["org"] == "ucsc2024-cse183"
        ):
            print(
                colors.FAIL
                + "Error: You are not in your personal class repo"
                + colors.END
            )
            sys.exit(1)
    if not override and info and info["branch"] != "main":
        print(colors.FAIL + "Warning: You are not in the main git branch" + colors.END)
        sys.exit(0)
    if root and not os.path.exists(os.path.join(root, ".gitignore")):
        print(
            colors.WARN + "Warning: You have not created a .gitignore file" + colors.END
        )
    cmd = f"git status -s -- {path}"
    ret = subprocess.run(cmd, shell=True, capture_output=True, check=True)
    output = ret.stdout.decode().strip()
    if output:
        print(colors.WARN + "Warning: You have uncommitted changes!" + colors.END)
        print(f"> {cmd}\n{output}\n")
        print(
            "To add them do:"
            + colors.TYPE
            + '\n\tgit add .\n\tgit commit -a -m "..."\n'
            + colors.END
        )
    cmd = f"git diff --name-status origin/main -- {path}"
    ret = subprocess.run(cmd, shell=True, capture_output=True, check=True)
    output = ret.stdout.decode().strip()
    if output:
        print(colors.WARN + "Warning: You have local changes not pushed!" + colors.END)
        print(f"> {cmd}\n{output}\n")
        print(
            "To push them do:"
            + colors.TYPE
            + "\n\tgit push origin main\n\n"
            + colors.END
        )
    return path


############################################################
# Grading logic
############################################################


class StopGrading(Exception):
    pass


def children(element):
    return [e for e in element if not isinstance(e, str)]


def parents(soup):
    """find all the ancestors of an element"""
    s, p = [], soup
    while p:
        s.append(p)
        p = p.parent
    return s


def common_ancestor(a, b):
    """find a commo ancestor between two elements"""
    parents_a = parents(a)
    parents_b = parents(b)
    for item in parents_a:
        if item in parents_b:
            return item
    return None


class Assignment:
    def __init__(self, folder, max_grade):
        self.folder = folder
        self._max_grade = max_grade
        self._comments = []

    def add_comment(self, comment, points=0):
        self._comments.append((comment, points))

    def grade(self):
        steps = [getattr(self, name) for name in dir(self) if name.startswith("step")]
        for step in steps:
            try:
                step()
            except StopGrading:
                break
            except:
                print(traceback.format_exc())
                self.add_comment(step.__doc__ + " (Unable to grade)", 0)
        grade = 0
        for comment, points in self._comments:
            print("=" * 40)
            print(f"[{points} points]", comment)
            grade += points
        print("=" * 40)
        print(f"TOTAL GRADE {grade}")
        print("=" * 40)
        return grade


def grade(rel_path):
    """entry point"""
    assignment_name = rel_path
    assignment_file = os.path.join(os.path.dirname(__file__), assignment_name + ".py")
    try:
        module = SourceFileLoader(assignment_name, assignment_file).load_module()
    except:
        print(colors.FAIL + "Error: running grade from the wrong folder" + colors.END)
        sys.exit(1)
    assignment = getattr(module, assignment_name.title())(rel_path)
    return assignment.grade()


def main():
    override = "--override" in sys.argv
    rel_path = check_student_repo(override)
    grade(rel_path)


if __name__ == "__main__":
    main()
