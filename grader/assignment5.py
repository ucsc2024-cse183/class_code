import importlib
import os
import sys
import time
import traceback

import requests
from grade import (
    AssignmentBase,
    By,
    Keys,
    Soup,
    StopGrading,
    children,
    make_chrome_driver,
    py4web,
)


def fetch(method, url, body=None, cookies=None):
    print(f"Trying {method} {body or ''} to {url} ...")
    if method == "GET":
        response = requests.get(url, allow_redirects=True, cookies=cookies)
    if method == "PUT":
        response = requests.put(url, json=body, cookies=cookies)
    if method == "POST":
        response = requests.post(url, json=body, cookies=cookies)
    if method == "DELETE":
        response = requests.delete(url, cookies=cookies)
    assert (
        response.status_code == 200
    ), f"Expected 200 OK but received {response.status_code}"
    try:
        json = response.json()
    except Exception:
        json = None
    if json is None:
        assert (
            False
        ), f"received:\n{repr(response.content[:80].decode()+'...')}\nand this is invalid JSON"
    print(f"JSON response {json}")
    return json


class Assignment(AssignmentBase, py4web):
    def __init__(self, folder):
        AssignmentBase.__init__(self, folder, max_grade=12)
        self.start_server(folder + "/apps", "tagged_posts")
        self.browser = make_chrome_driver()

    def goto(self, url):
        print(f"Loading {url}")
        self.browser.get(url)
        self.browser.implicitly_wait(10)
        time.sleep(4)

    def find(self, css):
        print(f'Looking for "{css}" selector in page')
        elements = self.browser.find_elements(By.CSS_SELECTOR, css)
        assert elements, f"element {css} not found"
        print("element found")
        return elements[0]

    def refresh(self):
        self.browser.refresh()
        self.browser.implicitly_wait(4)
        time.sleep(4)

    def step01(self):
        "it chould be made of valid HTML and CSS."
        print("Start grading index/html")
        self.goto(self.url)
        # TODO: check page forces redirect to login

    def step02(self):
        "found the index page"
        sys.path.append(os.path.join(self.apps_folder))
        env = {}
        self.cookies = None
        try:
            exec("import tagged_posts.models as testmodule", env)
        except Exception:
            raise AssertionError("unable to load models.py")
        testmodule = env.get("testmodule")
        assert testmodule and hasattr(testmodule, "db"), "no db defined models.py"
        assert "auth_user" in testmodule.db.tables, "cannot find auth_user table"
        db = testmodule.db
        self.db = db
        db.auth_user.password.writable = True
        res = db.auth_user.validate_and_insert(
            username="tester",
            email="tester@example.com",
            password="1234qwerQWER!@#$",
            first_name="Tester",
            last_name="TESTER",
        )
        db.commit()
        print(res)
        assert res.get("id") == 1, "unable to create user"
        print(db.auth_user[1])
        self.goto(self.url)
        email = self.find("[name='email']")
        password = self.find("[name='password']")
        submit = self.find("[type='submit']")
        assert (
            email and password and submit
        ), "expected a login page, but did not find it"
        email.send_keys("tester")
        password.send_keys("1234qwerQWER!@#$")
        submit.click()
        self.goto(self.url)
        assert "tester" in self.browser.page_source, "unable to login"
        assert "logout" in self.browser.page_source, "unable to login"
        set_cookies = self.browser.get_cookies()
        assert len(set_cookies) >= 1, "server cookies not working"
        print("cookies", set_cookies)
        self.cookies = {"tagged_posts_session": set_cookies[0]["value"]}
        assert (
            "post_item" in testmodule.db.tables
        ), "table post_item not found in models.py"
        post_item = testmodule.db.post_item
        assert "content" in post_item.fields, "post_item has no content field"
        assert "created_on" in post_item.fields, "post_item has no created_on field"
        assert "created_by" in post_item.fields, "post_item has no created_by field"
        assert (
            post_item.created_on.type == "datetime"
        ), "post_item.created_on must be a datetime"
        assert (
            post_item.created_by.type == "reference auth_user"
        ), "post_item.created_by must be a reference"
        self.add_comment("Table post_item defined correctly", 1.0)

        assert (
            "tag_item" in testmodule.db.tables
        ), "table tag_item not found in models.py"
        tag_item = testmodule.db.tag_item
        assert "name" in tag_item.fields, "tag_item has no name field"
        assert "post_item_id" in tag_item.fields, "tag_item has no post_item_id field"
        assert (
            tag_item.post_item_id.type == "reference post_item"
        ), "tag_item.post_item_id must be a reference"
        self.add_comment("Table tag_item defined correctly", 1.0)

    def step03(self):
        "Checking api"
        if not self.cookies:
            raise StopGrading
        db = self.db
        # self.url = "http://127.0.0.1:8000/bird_spotter/"
        try:
            content = "This is a message about #fun #games"
            res = fetch("POST", self.url + "api/posts", {"content": content})
            assert res.get("id") == 1, "unable to store a post_item using API"
        except:
            pass
        else:
            assert False, "I should not have been able to access API without Login"

        content = "This is a message about #fun #games"
        res = fetch(
            "POST", self.url + "api/posts", {"content": content}, cookies=self.cookies
        )
        assert res.get("id") == 1, "unable to store a post_item using API"

        time.sleep(1)

        content = "This is a message about #boring #games"
        res = fetch(
            "POST", self.url + "api/posts", {"content": content}, cookies=self.cookies
        )
        assert res.get("id") == 2, "unable to store a post_item using API"
        self.add_comment("POST to /api/posts works", 1.0)

        res = fetch("GET", self.url + "api/tags", cookies=self.cookies)
        assert res == {
            "tags": ["boring", "fun", "games"]
        }, "Did not receive correct tags"
        self.add_comment("GET to /api/tags works", 1.0)

        res = fetch("GET", self.url + "api/posts", cookies=self.cookies)
        assert "posts" in res, 'expected {"posts": [...]}'
        assert len(res["posts"]) == 2, "expected to posts in response"
        assert (
            "#boring" in res["posts"][0]["content"]
        ), "expected the first post to containt #boring"
        assert (
            "#fun" in res["posts"][1]["content"]
        ), "expected the second post to containt #boring"
        self.add_comment("GET to /api/posts works", 0.4)

        res = fetch("GET", self.url + "api/posts?tags=fun", cookies=self.cookies)
        assert "posts" in res, 'expected {"posts": [...]}'
        assert len(res["posts"]) == 1, "expected to posts in response"
        assert (
            "#fun" in res["posts"][0]["content"]
        ), "expected the second post to containt #boring"
        self.add_comment("GET to /api/posts?tags=fun works", 0.3)

        res = fetch("GET", self.url + "api/posts?tags=fun,boring", cookies=self.cookies)
        assert "posts" in res, 'expected {"posts": [...]}'
        assert len(res["posts"]) == 2, "expected to posts in response"
        self.add_comment("GET to /api/posts?tags=fun,boring works", 0.3)

        res = fetch("DELETE", self.url + "api/posts/1", cookies=self.cookies)
        assert db(db.post_item).count() == 1, "unable to delete post"
        self.add_comment("DELETE to /api/posts works", 1.0)

    def step04(self):
        self.goto(self.url)
        self.find("textarea.post-content")
        self.find("button.submit-content")
        self.find(".feed")
        items = self.browser.find_elements(By.CSS_SELECTOR, ".feed .post_item")
        assert len(items) == 1, "Exepcted to find one post_item"
        assert "#boring" in items[0].get_attribute(
            "innerHTML"
        ), "Exepcted to find a post_item"
        self.add_comment("Feed column works", 1.0)

    def step05(self):
        self.find(".tags")
        tags = self.browser.find_elements(By.CSS_SELECTOR, ".tags .tag")
        assert len(tags) == 2, "did not find the expected tags"
        assert "boring" in tags[0].text, "Exepcted the boring tag"
        assert "games" in tags[1].text, "Exepcted the games tag"
        self.add_comment("Tags column works", 1.0)

    def step06(self):
        db = self.db
        self.goto(self.url)
        content = "#hello #world"
        self.find("textarea.post-content").send_keys(content)
        self.find("button.submit-content").click()
        time.sleep(1)
        assert db(db.post_item).count() == 2, "record not inserted in database"
        self.add_comment("Posting from page works", 0.5)

        self.find(".feed")
        items = self.browser.find_elements(By.CSS_SELECTOR, ".feed .post_item")
        assert len(items) == 2, "Exepcted to find two post_items"
        assert "#hello" in items[0].get_attribute(
            "innerHTML"
        ), "Exepcted to find a post_item"
        assert "#world" in items[0].get_attribute(
            "innerHTML"
        ), "Exepcted to find a post_item"
        self.add_comment("Posting to the feed works", 0.5)

        tags = self.browser.find_elements(By.CSS_SELECTOR, ".tags .tag")
        assert "boring" in tags[0].text, "Exepcted the boring tag"
        assert "games" in tags[1].text, "Exepcted the games tag"
        assert "hello" in tags[2].text, "Exepcted the hello tag"
        assert "world" in tags[3].text, "Exepcted the world tag"
        self.add_comment("Tags refreshed correclty", 1.0)

        tags[0].click()
        time.sleep(1)
        items = self.browser.find_elements(By.CSS_SELECTOR, ".feed .post_item")
        assert len(items) == 1, "Exepcted to find one post_item"
        assert "#boring" in items[0].get_attribute(
            "innerHTML"
        ), "Exepcted to find a post_item"
        assert "#games" in items[0].get_attribute(
            "innerHTML"
        ), "Exepcted to find a post_item"
        self.add_comment("Tags toggling works", 0.5)

        tags[0].click()
        time.sleep(1)
        items = self.browser.find_elements(By.CSS_SELECTOR, ".feed .post_item")
        assert len(items) == 2, "Exepcted to find two post_item"
        self.add_comment("Tags untoggling works", 0.5)

    def step07(self):
        self.goto(self.url)
        items = self.browser.find_elements(By.CSS_SELECTOR, ".feed .post_item")
        buttons = self.browser.find_elements(By.CSS_SELECTOR, ".feed .post_item button")
        assert len(items) == 2, "Expected two post_items"
        assert len(buttons) == 2, "Expected a delete button per item"
        buttons[0].click()
        time.sleep(1)
        items = self.browser.find_elements(By.CSS_SELECTOR, ".feed .post_item")
        assert len(items) == 1, "Expected the item to be deleted"
        self.goto(self.url)
        items = self.browser.find_elements(By.CSS_SELECTOR, ".feed .post_item")
        assert len(items) == 1, "Expected the item to be deleted"
        self.add_comment("Deleting uding the feed button works", 1.0)
