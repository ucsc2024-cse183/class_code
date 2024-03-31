#!/bin/env python
import os
import sys
import subprocess
import shutil
import traceback

import mechanize
from bs4 import BeautifulSoup as Soup

class colors:
    TYPE = '\033[94m'
    OK = '\033[92m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_git_root():
    """return the root of the repo or None if not in a repo"""
    try:
        ret = subprocess.run("git rev-parse --show-toplevel", shell=True, capture_output=True, check=True)
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
    ret = subprocess.run("git config --get remote.origin.url", shell=True, capture_output=True, check=True)
    url = ret.stdout.decode("UTF8").strip()
    if url.startswith("git@"):
        org, name = url.split(":")[1][:-4].split("/")[-2:]
    else:
        org, name = url.split("/")[-2:]
    if name.endswith(".git"):
        name = name[:-4]
    ret = subprocess.run("git rev-parse --abbrev-ref HEAD", shell=True, capture_output=True, check=True)
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
            print(colors.FAIL + "Error: You are class_code repo, not your personal class repo" + colors.END)
            sys.exit(1)
        if not (info and info["name"].endswith("-code") and info["org"] == "ucsc2024-cse183"):
            print(colors.FAIL + "Error: You are not in your personal class repo" + colors.END)
            sys.exit(1)
    if not override and info and info["branch"] != "main":
        print(colors.FAIL + "Warning: You are not in the main git branch" + colors.END)
        sys.exit(0)
    if root and not os.path.exists(os.path.join(root, ".gitignore")):
        print(colors.WARN + "Warning: You have not created a .gitignore file" + colors.END)
    cmd = f"git status -s -- {path}"
    ret = subprocess.run(cmd, shell=True, capture_output=True, check=True)
    output = ret.stdout.decode().strip()
    if output:
        print(colors.WARN + "Warning: You have uncommitted changes!" + colors.END)
        print(f"> {cmd}\n{output}\n")
        print("To add them do:" + colors.TYPE + "\n\tgit add .\n\tgit commit -a -m \"...\"\n" + colors.END)
    cmd = f"git diff --name-status origin/main -- {path}"
    ret = subprocess.run(cmd, shell=True, capture_output=True, check=True)
    output = ret.stdout.decode().strip()
    if output:
        print(colors.WARN + "Warning: You have local changes not pushed!" + colors.END)
        print(f"> {cmd}\n{output}\n")
        print("To push them do:" + colors.TYPE + "\n\tgit push origin main\n\n" + colors.END)
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

########################################################################
# Assignment grading policies
########################################################################

class Assignment0(Assignment):
    def __init__(self, folder):
        Assignment.__init__(self, folder, max_grade=3)

    def step1(self):
        "check if index.html exists"
        self.filename = os.path.join(self.folder, "index.html")
        if not os.path.exists(self.filename):
            self.add_comment(self.step1.__doc__, 0)
            raise StopGrading
        self.add_comment(self.step1.__doc__, 1)

    def step2(self):
        "<head> and <body> exist"
        try:
            with open(self.filename) as content:            
                self.soup = Soup(content)
        except:
            self.add_comment(self.step2.__doc__, 0)
            raise StopGrading
        html = self.soup.find("html")
        head = html and html.find("head")
        body = html and html.find("body")
        if head and body:
            self.add_comment(self.step2.__doc__, 1)
        else:
            self.add_comment("Incorrect <html> structure", 1)

    def step3(self):
        "outer and inner divs have correct structure"
        outer = self.soup.find("div", class_="outer")
        inner = self.soup.find("div", class_="inner")
        if inner and inner.parent == outer:
            self.add_comment(self.step2.__doc__, 1)

    def step4(self):
        "find h1 with message"
        h1 = self.soup.find("h1")
        inner = self.soup.find("div", class_="inner")
        if h1.parent == inner and h1.text.strip().lower() == "hello world":
            self.add_comment(self.step2.__doc__, 1)


class Assignment1(Assignment):
    """ """

    def __init__(self, folder):
        Assignment.__init__(self, folder, max_grade=3)

    def step01(self):
        "it should have a <head/> and a <bod/y>"
        self.filename = os.path.join(self.folder, "index.html")
        success = False
        if not os.path.exists(self.filename):
            self.add_comment("cannot find the file", 0)
        else:
            try:
                with open(self.filename) as content:
                    self.soup = Soup(content, "html.parser")
                    success = self.soup.find("head") and self.soup.find("body")
            except:
                self.add_comment("file cannot be read or parsed", 0)
        self.add_comment(self.step01.__doc__, 1 if success else 0)
        if not success:
            raise StopGrading

    def step02(self):
        "it should use the Bulma css library"
        link = self.soup.find("link")
        url = link["href"].lower()
        success = "bulma" in url and url.endswith(".css")
        self.add_comment(self.step02.__doc__, 1 if success else 0)
        if not success:
            raise StopGrading

    def step03(self):
        "it should contain a <header/> a <footer/> and two <section/>s in between"
        body = self.soup.find("body")
        self.children = children(body)
        names = [c.name for c in self.children]
        success = len(self.children) == 4 and names == [
            "header",
            "section",
            "section",
            "footer",
        ]
        self.add_comment(self.step03.__doc__, 1 if success else 0)
        if not success:
            raise StopGrading

    def step04(self):
        "One section with class top and one with class bottom"
        success = (
            "top" in self.children[1]["class"] and "bottom" in self.children[2]["class"]
        )
        self.add_comment(self.step04.__doc__, 1 if success else 0)

    def step05(self):
        "The top section should contain an <img/> that fills the page horizontally and show the image of a cat"
        image = self.children[1].find("img")
        success = image
        self.add_comment(self.step05.__doc__, 1 if success else 0)

    def step06(self):
        "The bottom section should contain 6 columns"
        columns = self.children[2].find("div", class_="columns")
        self.cols = columns and children(columns) or []
        success = len(self.cols) == 6 and all("column" in e["class"] for e in self.cols)
        self.add_comment(self.step06.__doc__, 1 if success else 0)
        if not success:
            raise StopGrading

    def step07(self):
        "Each column should contain a card"
        self.cards = [c.find("div", class_="card") for c in self.cols]
        success = all(self.cards)
        self.add_comment(self.step07.__doc__, 1 if success else 0)
        if not success:
            raise StopGrading

    def step08(self):
        "each card should have a header and content"
        success = all(
            card.find(class_="card-header") and card.find(class_="card-content")
            for card in self.cards
        )
        self.add_comment(self.step08.__doc__, 1 if success else 0)

    def step09(self):
        "each card content the cards be some text of your choice followed by a button. In total there should 6 buttons, one per column, one of each of the Bulma styles"
        expected = ["primary", "link", "info", "success", "warning", "danger"]
        styles = []
        for col in self.cols:
            card = col.find("div", class_="card")
            button = card.find("button")
            if button:
                classes = button["class"]
                if "button" in classes:
                    for style in expected:
                        if f"is-{style}" in classes:
                            styles.append(style)
                            break
        success = set(expected) == set(styles)
        self.add_comment(self.step09.__doc__, 1 if success else 0)

    def step10(self):
        "each card header should have title with the name of the style of the corrensponding button."
        expected = ["primary", "link", "info", "success", "warning", "danger"]
        match = 0
        for card in self.cards:
            title = card.find(class_="card-header-title")
            if title:
                name = title.text.lower()
                if name in expected:
                    expected.remove(name)
                    button = card.find("button", class_=f"is-{name}")
                    if button:
                        match += 1
        success = match == 6
        self.add_comment(self.step10.__doc__, 1 if success else 0)

    def step11(self):
        "the footer should contain a link to the class code"
        self.footer_links = self.children[3].findAll("a")
        success = any(
            link["href"] == "class_code_link.html" for link in self.footer_links
        )
        self.add_comment(self.step11.__doc__, 1 if success else 0)

    def step12(self):
        "the footer should also contain an a link that, on click, will open the user's default email app with To: file equalt to your email address. The text of the link should be youor name."
        success = any(link["href"].startswith("mailto:") for link in self.footer_links)
        self.add_comment(self.step12.__doc__, 1 if success else 0)

def grade(rel_path):
    """entry point"""
    assignment_name = rel_path.title()
    print(assignment_name)
    if assignment_name not in ["Final"] + [f"Assignment{n}" for n in range(6)]:
        print(colors.FAIL + "Error: running grade from the wrong folder" + colors.END)
        sys.exit(1)
    assignment = globals()[assignment_name](rel_path)
    return assignment.grade()

def main():
    override = '--override' in sys.argv
    rel_path = check_student_repo(override)
    grade(rel_path)

if __name__ == "__main__":
    main()
        
        
