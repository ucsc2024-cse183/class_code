import os

from grade import Assignment, Soup, StopGrading


class Assignment0(Assignment):
    def __init__(self, folder):
        Assignment.__init__(self, folder, max_grade=3)

    def step1(self):
        "check if index.html exists"
        self.filename = "index.html"
        print(self.filename)
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
