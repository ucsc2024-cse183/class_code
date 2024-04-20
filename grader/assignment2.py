import os
import sys
import time

from grade import (
    AssignmentBase,
    By,
    Keys,
    Soup,
    StopGrading,
    children,
    make_chrome_driver,
)


def safe_float(value):
    try:
        return float(value)
    except:
        0


class Assignment(AssignmentBase):
    def __init__(self, folder):
        AssignmentBase.__init__(self, folder, max_grade=12)
        self.browser = make_chrome_driver()

    def goto(self, url):
        self.browser.get(url)
        self.browser.implicitly_wait(10)

    def refresh(self):
        self.browser.refresh()
        self.browser.implicitly_wait(10)

    def append_comment(self, points, comment):
        self._comments.append((points, comment))

    def step01(self):
        print("Start grading index/html")
        self.goto("file://" + os.path.join(self.folder, "index.html"))
        print("loading index.html")
        assert self.browser.find_element(By.TAG_NAME, "html")
        print("loading index.html ... success")
        self.add_comment("HTML is valid", 1)

    def step02(self):
        table = self.browser.find_element(By.CSS_SELECTOR, "table")
        bulma_classes = ["table", "is-striped", "is-fullwidth"]
        assert set(bulma_classes) & set(
            table.get_attribute("class").split()
        ), "Table does not use Bulma CSS"
        self.add_comment("Table uses Bulma CSS", 1)

    def step03(self):
        rows = self.browser.find_elements(By.CSS_SELECTOR, "table tr")
        num_rows = len(rows)
        num_cols = max([len(r.find_elements(By.CSS_SELECTOR, "td")) for r in rows])
        assert (
            num_rows == 14 and num_cols == 3
        ), f"Wrong number of rows and columns: {num_rows} rows, {num_cols} columns"
        self.add_comment("Correct number of rows and columns", 1)

    def step04(self):
        rows = self.browser.find_elements(By.CSS_SELECTOR, "table tr")
        for i, r in enumerate(rows):
            assert (
                r.get_attribute("class") == f"row-{i + 1}"
            ), f"Row {i + 1} does not have the correct class"
        self.add_comment("Row classes are correct", 1)

    def step05(self):
        rows = self.browser.find_elements(By.CSS_SELECTOR, "table tr")
        content = (
            (1, "Income"),
            (7, "Payments, Credits, and Tax"),
            (13, "Refund"),
            (14, "Amount You Owe"),
        )
        for i, c in content:
            assert (
                rows[i - 1].find_element(By.CSS_SELECTOR, "td").text.lower()
                == c.lower()
            ), f"First column header for row {i} is wrong"
        self.add_comment("First column is correct", 1)

    def step06(self):
        rows = self.browser.find_elements(By.CSS_SELECTOR, "table tr")
        for i, r in enumerate(rows):
            cols = r.find_elements(By.CSS_SELECTOR, "td")
            assert len(cols) >= 2, "Row with less than 2 columns"
            second_col = cols[-2].text
            assert second_col.startswith(
                str(i + 1) + " "
            ), f"Row {i + 1} does not start with {i + 1}"
        self.add_comment("Second column is correct", 1)

    def step07(self):
        for i in range(1, 15):
            row = self.browser.find_element(By.CSS_SELECTOR, f".row-{i}")
            assert row, f"count not find row with class row-{i}"
            cols = row.find_elements(By.CSS_SELECTOR, "td")
            assert len(cols) > 0, "Row with less than 1 columns"
            col = cols[-1]
            input_field = col.find_element(By.CSS_SELECTOR, "input")
            assert input_field, f"Row {i} does not have an input field"
            name = input_field.get_attribute("name")
            assert (
                name == f"value-{i}"
            ), f"Input field for row {i} has wrong name {name}"
        self.add_comment("Third column is correct", 1)

    def step08(self):
        ro_fields = [4, 5, 6, 9, 10, 12, 13, 14]
        for i in range(1, 15):
            input_field = self.browser.find_element(By.NAME, f"value-{i}")
            is_readonly = input_field.get_attribute("readonly") is not None
            assert is_readonly == (
                i in ro_fields
            ), f"Input field for row {i} read-only is wrong"
        self.add_comment("The required input fields are read-only.", 1)

    def step09(self):
        test_values = [
            [("1", "2", "3"), 6],
            [("10", "40", "80"), 130],
            [("100000", "3000", "20000"), 123000],
        ]
        for (v1, v2, v3), expected in test_values:
            self.refresh()  # Otherwise, autocomplete breaks the test.
            inp1 = self.browser.find_element(By.NAME, value="value-1")
            inp2 = self.browser.find_element(By.NAME, value="value-2")
            inp3 = self.browser.find_element(By.NAME, value="value-3")
            inp4 = self.browser.find_element(By.NAME, value="value-4")
            inp1.send_keys(v1)
            time.sleep(1)
            inp2.send_keys(v2)
            time.sleep(1)
            inp3.send_keys(v3)
            time.sleep(1)
            self.browser.implicitly_wait(4)
            value_1 = inp1.get_attribute("value")
            value_2 = inp2.get_attribute("value")
            value_3 = inp3.get_attribute("value")
            time.sleep(1)
            value_4 = inp4.get_attribute("value")
            assert (
                safe_float(value_4) == expected
            ), f"Row 4 computation for inputs {value_1}, {value_2}, {value_3}, returned {value_4} instead of {expected}"
        self.add_comment("Row 4 computation correct for all test values", 1)

    def step10(self):
        self.refresh()
        checkbox = self.browser.find_element(
            By.CSS_SELECTOR, '.row-5 input[type="checkbox"]'
        )
        inp = self.browser.find_element(By.NAME, value="value-5")
        value_5 = safe_float(inp.get_attribute("value"))
        assert (
            value_5 == 13850
        ), f"Field 5 value is {value_5} instead of 13850 when checkbox is not checked"
        checkbox.click()
        self.browser.implicitly_wait(10)
        value_5 = safe_float(inp.get_attribute("value"))
        assert (
            value_5 == 27700
        ), f"Field 5 value is {value_5} instead of 27700 when checkbox is checked"
        self.add_comment("The checkbox on row 5 works.", 1)

    def step11(self):
        self.refresh()
        test_values = [
            [10000, 0],
            [30000, 1718],
            [60000, 5460.5],
            [100000, 14260.5],
            [200000, 38400],
            [500000, 142047],
            [1000000, 325207.5],
        ]
        for v, expected in test_values:
            field_1 = self.browser.find_element(By.NAME, value="value-1")
            field_14 = self.browser.find_element(By.NAME, value="value-14")
            field_1.clear()
            field_1.send_keys(str(v))
            value_14 = field_14.get_attribute("value")
            assert (
                safe_float(value_14) == expected
            ), f"Tax computation for input {v}, returned {value_14} instead of {expected}"
        self.add_comment("Tax computation correct for simple test values", 1)

        self.refresh()
        test_values = [
            (
                ((1, 100200), (2, 500), (3, 1200), (7, 8000), (11, 1000)),
                0,
                7678.5,
            ),
            (
                ((1, 100200), (2, 500), (3, 1200), (7, 8000), (8, 500), (11, 1000)),
                0,
                7178.5,
            ),
            (
                ((1, 250000), (2, 1500), (3, 100), (7, 6000), (11, 3000)),
                0,
                52107.0,
            ),
            (
                ((1, 80000), (2, 5500), (3, 1700), (7, 5000), (11, 4000)),
                0,
                10444.5,
            ),
            (
                ((1, 80000), (2, 5500), (3, 1700), (7, 35000), (11, 4000)),
                19555.5,
                0,
            ),
        ]
        for inps, out1, out2 in test_values:
            self.refresh()  # Otherwise, autocomplete breaks the test.
            for i, v in inps:
                field = self.browser.find_element(By.NAME, value=f"value-{i}")
                field.clear()
                field.send_keys(str(v))
            field_13 = self.browser.find_element(By.NAME, value="value-13")
            field_14 = self.browser.find_element(By.NAME, value="value-14")
            out_13 = safe_float(field_13.get_attribute("value"))
            out_14 = safe_float(field_14.get_attribute("value"))
            assert (
                out_13 == out1
            ), f"Row 13 computation for inputs {inps}, returned {out_13} instead of {out1}"
            assert (
                out_14 == out2
            ), f"Row 14 computation for inputs {inps}, returned {out_14} instead of {out2}"
        self.add_comment("Tax computation correct for all test values", 1)
