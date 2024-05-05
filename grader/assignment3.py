import os

from grade import (
    AssignmentBase,
    By,
    Keys,
    Soup,
    StopGrading,
    children,
    make_chrome_driver,
)


class Assignment(AssignmentBase):
    def __init__(self, folder):
        AssignmentBase.__init__(self, folder, max_grade=12)
        self.browser = make_chrome_driver()

    def goto(self, url):
        self.browser.get(url)
        self.browser.implicitly_wait(10)

    def refresh(self):
        self.browser.refresh()
        self.browser.implicitly_wait(4)

    def step01(self):
        "it chould be made of valid HTML and CSS."
        print("Start grading index/html")
        self.goto("file://" + os.path.join(self.folder, "index.html"))
        print("loading index.html")
        assert self.browser.find_element(By.TAG_NAME, "html")
        print("loading index.html ... success")
        self.add_comment("HTML is valid", 1)

    def step02(self):
        "it should use vue.js"
        scripts = self.browser.find_elements(By.TAG_NAME, "script")
        assert len(scripts) == 2, "The code should load two scripts"
        assert "vue" in scripts[0].get_attribute("src") or "vue" in scripts[
            1
        ].get_attribute("src"), "not using vue"
        self.add_comment("Code uses vue.js correcly", 1)

    def step03(self):
        "the UI of the game should consists of 9 cells organized in 3 rows of 3 columns each."
        self.cells = []
        table = self.browser.find_element(By.TAG_NAME, "table")
        assert table, "table not found"
        rows = table.find_elements(By.TAG_NAME, "tr")
        assert len(rows) == 3, "found a number of rows different than 3"
        for k, row in enumerate(rows):
            cols = row.find_elements(By.TAG_NAME, "td")
            self.cells.append(cols)
            assert (
                len(cols) == 3
            ), f"row {k+1} contains a number of cols different than 3"
        self.add_comment("Table found with 3x3 cells", 1)

    def step04(self):
        "each cell chould contain a button of class `cell-i-j` where i,j is the cell index"
        for i in range(3):
            for j in range(3):
                cell = self.cells[i][j]
                name = f"cell-{i}-{j}"
                button = cell.find_element(By.TAG_NAME, "button")
                assert button, f"button {name} not found in tr {i} td {j}"
                classes = button.get_attribute("class").split()
                assert (
                    name in classes
                ), f"button in tr {i} td {j} does not have class {name}"
        self.add_comment("All buttons found and named correcly", 1)

    def get_buttons(self):
        buttons = {}
        for i in range(3):
            for j in range(3):
                buttons[i, j] = self.browser.find_element(
                    By.CSS_SELECTOR, f".cell-{i}-{j}"
                )
        return buttons

    def step05(self):
        "each button should display the state of the correspoding cell '', 'X' or 'O'"
        for i in range(3):
            for j in range(3):
                self.refresh()
                buttons = self.get_buttons()
                buttons[i, j].click()
                assert (
                    buttons[i, j].text == "X"
                ), f"clicked on {i},{j} but not 'X' found"
                counter = 0
                for button in buttons.values():
                    assert (
                        button.text.strip() in "XO"
                    ), "Found an invalid text in a button"
        self.add_comment("All buttons found and contain correct symbols", 1)

    def show(self, buttons):
        board = ""
        for i in range(3):
            board += (
                "["
                + "".join(buttons[i, j].text.strip() or " " for j in range(3))
                + "]\n"
            )
        print(board, end="")

    def step06(self):
        "users can only play empty cells and computers will play immediately after the user."
        for i in range(3):
            for j in range(3):
                print("playing:", i, j)
                self.refresh()
                buttons = self.get_buttons()
                buttons[i, j].click()
                self.show(buttons)
                for button in buttons.values():
                    if button.text.strip() == "O":
                        button.click()
                        assert (
                            button.text.strip() == "O"
                        ), "Cannot override answer from opponent"
        self.add_comment("All buttons seem to work correctly", 3)

    def winner(self, buttons):
        for player in "XO":
            for i in range(3):
                if all(buttons[i, j].text.strip() == player for j in range(3)):
                    return player
                if all(buttons[j, i].text.strip() == player for j in range(3)):
                    return player
            if all(buttons[i, i].text.strip() == player for i in range(3)):
                return player
            if all(buttons[i, 2 - i].text.strip() == player for i in range(3)):
                return player
        return None

    def step07(self):
        "the computer should never lose"
        for game in range(10):
            print("new game")
            self.refresh()
            buttons = self.get_buttons()
            buttons[1, 1].click()
            self.show(buttons)
            for k in range(4):
                xos = sum(button.text.strip() == "X" for button in buttons.values())
                assert xos == k + 1, "Computer did record move"
                oos = sum(button.text.strip() == "O" for button in buttons.values())
                assert oos == k + 1, "Computer did not play"
                for button in buttons.values():
                    if not button.text.strip():
                        button.click()
                        break
                else:
                    break
                self.show(buttons)
                winner = self.winner(buttons)
                assert not winner or winner == "O", "Ouch! computer lost"
                if winner:
                    print("winner", winner)
                    break
                print()
            if k == 5:
                self.add_comment("Got in a loop", 0)
                return
        print("A strange game. The only winning move is not to play.")
        self.add_comment("Computer never lost", 2)

    def step08(self):
        "there should be a button of class reset that when clicked, resets the game"
        reset = self.browser.find_element(By.CSS_SELECTOR, ".reset")
        assert reset, "reset button not found"
        reset.click()
        buttons = self.get_buttons()
        assert all(
            b.text.strip() == "" for b in buttons.values()
        ), "reset did not reset"
        self.add_comment("Successful reset button", 2)
