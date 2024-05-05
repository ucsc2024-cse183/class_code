#!/usr/bin/env python

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
import traceback
import threading
from importlib.machinery import SourceFileLoader

import selenium
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

try:
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.core.os_manager import ChromeType
except:
    ChromeDriverManager = None

__version__ = "20240420.1"


def run(cmd):
    print("Running:", cmd)
    return (
        subprocess.run(cmd, check=True, capture_output=True, shell=True)
        .stdout.decode()
        .strip()
    )


class StopGrading(Exception):
    pass


def make_chrome_driver(headless=True):
    options = webdriver.ChromeOptions()
    if ChromeDriverManager:
        try:
            chromium_path = run("which chromium")
            version = run(f"{chromium_path} --version").split()[1].split(".")[0]
            driver = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
            options.binary_location = chromium_path
        except Exception:
            driver = ChromeDriverManager().install()
        service = Service(driver)
    else:
        service = Service("/usr/lib/chromium/chromedriver")
        options.binary_location = "/usr/lib/chromium/chromium"

    options.add_argument("--window-size=1024,768")
    options.add_argument("--disable-extensions")
    options.add_argument("--ignore-certificate-errors")
    if headless:
        options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-extensions")
    options.add_argument("--enable-automation")
    options.add_argument("--disable-browser-side-navigation")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-infobars")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--disable-software-rasterizer")
    return webdriver.Chrome(options=options, service=service)


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
        return run("git rev-parse --show-toplevel")
    except:
        return None


def split_repo_path(path=None):
    """return the repo root and the the cwd relative to it"""
    root = get_git_root()
    if not root:
        return None
    return root, os.path.relpath(path or os.getcwd(), root)


def get_repo_info():
    """returns the origin url, name of the org, and name of the repo in a dict"""
    url = run("git config --get remote.origin.url")
    if url.startswith("git@"):
        org, name = url.split(":")[1][:-4].split("/")[-2:]
    else:
        org, name = url.split("/")[-2:]
    if name.endswith(".git"):
        name = name[:-4]
    branch = run("git rev-parse --abbrev-ref HEAD")
    return {"org": org, "name": name, "url": url, "branch": branch}


def check_student_repo():
    """
    check this command is being executed in a valid student repo and prints a report.
    returns the relative path
    """
    root, path = split_repo_path()
    info = path and get_repo_info()
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
            + "Error: You may not be in your personal class repo"
            + colors.END
        )
    if info and info["branch"] != "main":
        print(colors.FAIL + "Warning: You are not in the main git branch" + colors.END)
        sys.exit(0)
    if root and not os.path.exists(os.path.join(root, ".gitignore")):
        print(
            colors.WARN + "Warning: You have not created a .gitignore file" + colors.END
        )
    cmd = f"git status -s -- {path}"
    output = run(cmd)
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
    output = run(cmd)
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


class py4web:
    def start_server(self, source_apps, app_name, port=8888):
        print("Starting the server")
        self.app_name = app_name
        self.apps_folder = os.path.join(tempfile.mkdtemp(), "apps")
        self.url = f"http://127.0.0.1:{port}/{app_name}/"
        shutil.rmtree(self.apps_folder, ignore_errors=True)
        if not os.path.exists(source_apps):
            print(f"{source_apps} does not exist!")
            raise StopGrading
        run(f"cp -r {source_apps} {self.apps_folder}")
        subprocess.run(
            ["rm", "-rf", os.path.join(self.apps_folder, app_name, "databases")]
        )
        self.server = None
        cmd = [
            "py4web",
            "run",
            self.apps_folder,
            "--port",
            str(port),
            "--app_names",
            app_name,
        ]
        print("Running:", " ".join(cmd))
        try:
            self.server = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
        except Exception:
            print("Unable to start py4web")
            raise StopGrading
        started = False
        while True:
            self.server.stdout.flush()
            line = self.server.stdout.readline().decode().rstrip()
            print(line)
            if "[X]" in line:
                started = True
            if "127.0.0.1:" in line:
                break
        if not started:
            print("The app has errors and was unable to start it")
            raise StopGrading

    def stop_server(self):
        if getattr(self, "server", None):
            self.server.kill()
            self.server = None
            shutil.rmtree(self.apps_folder)

    def __del__(self):
        self.stop_server()


class AssignmentBase:
    def __init__(self, folder, max_grade):
        self.folder = folder
        self._max_grade = max_grade
        self._comments = []

    def add_comment(self, comment, points=0):
        print(comment)
        self._comments.append((comment, points))

    def grade(self):
        step_names = [name for name in dir(self) if name.startswith("step")]
        for step_name in step_names:
            step = getattr(self, step_name)
            print("\nRunning", step_name, "=" * 60)
            try:
                step()
            except StopGrading:
                break
            except selenium.common.exceptions.NoSuchElementException as err:
                print(err)
                break
            except AssertionError as error:
                self.add_comment(f"{step_name}: " + str(error), 0)
            except:
                print(traceback.format_exc())
                self.add_comment(
                    (step.__doc__ or f"{step_name}:") + " (Unable to grade)", 0
                )
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
    print(f"Begin grading {assignment_name}")
    assignment_file = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), assignment_name + ".py"
    )
    try:
        module = SourceFileLoader(assignment_name, assignment_file).load_module()
    except Exception:
        print(traceback.format_exc())
        print(colors.FAIL + f"Error: unable to load {assignment_file}" + colors.END)
        sys.exit(1)
    num = 0
    assignment_class = getattr(module, "Assignment", None)
    if not assignment_class:
        print("Grader not found!")
        return 0
    try:
        assignment = assignment_class(os.getcwd())
        num = assignment.grade()
    except StopGrading:
        # this only happens when error is in constructor
        return 0
    except:
        print(traceback.format_exc())
    print(f"End grading {assignment_name}")
    return num


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--override", help="specify a folder with the assignment")
    args = parser.parse_args()
    if args.override:
        os.chdir(args.override)
        rel_path = os.getcwd().split("/")[-1].lower()
    else:
        rel_path = check_student_repo()
    grade(rel_path)
    sys.exit(0)


if __name__ == "__main__":
    print(f"Grader version {__version__}")
    main()
