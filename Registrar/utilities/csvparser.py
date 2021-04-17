import csv
import os

def parser (field, value, row, index):
    return row

def unparser (field, value, row, index):
    return row

class CSVParser (object):
    def __init__ (self, filepath = "", _object = [], parser = parser, unparser = unparser):
        self.filepath = filepath
        self.parser = parser

        if filepath != "":
            self.parseFilepath(filepath)
        elif len(_object) > 0:
            self.parseObject(_object)
        else:
            raise Exception("Invalid arguments provided")

    def parseFilepath (self, filepath):
        self.filepath = filepath
        with open(filepath, "r") as file:
            reader = csv.reader(file)
            self.header = [field for field in next(reader)]
            self.rows = [row for row in reader]
            self.csv = []

        self.parse()

    def parseObject (self, _object):
        self.header = _object[0]
        self.csv = _object
        self.rows = self.csv
        self.parse()

    def _parse (self, field, value, row, index):
        row = self.parser(field, value, row, index)
        self.columns[field].append(row[index])
        return row

    def parse (self):
        self.columns = {field: [] for field in self.header}
        for row in self.rows:
            for field, value in zip(self.header, row):
                row = self._parse(field, value, row, self.header.index(field))
            self.csv.append(row)

    def _unparse (self, field, value, row, index, unparser):
        row = unparser(field, value, row, index)
        self.unparse_columns[field].append(row[index])
        return row

    def unparse (self, unparser):
        self.unparse_columns = {field: [] for field in self.header}
        self.unparse_csv = []
        for row in self.csv:
            for field, value in zip(self.header, row):
                row = self._unparse(field, value, row, self.header.index(field), unparser)
            self.unparse_csv.append(row)

    def select (self, _object, default = "default"):
        returnDict = {"ROW_NUM": [], "columns": {field: [] for field in self.header}, "rows": []}
        index = []

        if not "where" in _object.keys():
            return self.csv

        for key,value in _object["where"].items():
            if key in self.header:
                if (value in self.columns[key]):
                    [index.append(self.columns[key].index(value)) for num in range(0, self.columns[key].count(value))]

        # sorts the list of indexes
        index.sort()

        # mitigates redundancy
        for num in index:
            if index.count(num) > 1:
                index.remove(num)

        # if _object = {"limit": 10}
        if "limit" in _object.keys():
            for num in range(0, _object["limit"]):
                for i in index:
                    returnDict["ROW_NUM"].append(i)

                    # appends the row to returnDict
                    returnDict["rows"].append(self.csv[i])

                    # appends the index from the column to returnDict[column]
                    [returnDict["columns"][field].append(self.columns[field][i]) for field in self.header]
        else:
            for i in index:
                returnDict["ROW_NUM"].append(i)

                # appends the row to returnDict
                returnDict["rows"].append(self.csv[i])

                # appends the index from the column to returnDict[column]
                [returnDict["columns"][field].append(self.columns[field][i]) for field in self.header]

        if (len(returnDict["rows"]) == 0):
            if (default != "default"):
                return default

        return returnDict

    def selectColumn (self, column):
        return self.columns.get(column)

    def selectAll (self):
        return {"ROW_NUM": [num for num in range(0, len(self.csv))], "columns": self.columns, "rows": self.csv}

    def insert (self, data, _object = {}):
        index = []

        if not [key for key in data.keys()].sort() == self.header.copy().sort():
            return False

        # format the data dict to suit the csv field pattern
        data = [data[field] for field in self.header]

        if not "where" in _object.keys():
            # adds the row to the bottom of the csv list and each column
            self.csv.append(data)
            [self.columns[field].append(value) for field, value in zip(self.header, data)]
            return self

        for key,value in _object["where"].items():
            if key in self.header:
                if value in self.columns[key]:
                    [index.append(self.columns[key].index(value)) for num in range(0, self.columns[key].count(value))]

        # sorts the lists of indexes
        index.sort()

        # mitigates redundancy
        for num in index:
            if index.count(num) > 1:
                index.remove(num)

        # if _object = {"limit": 10}
        if "limit" in _object.keys():
            for num in range(0, _object["limit"]):
                for i in index:
                    # inserts the element in the index of the csv list
                    self.csv.insert(i, data)

                    # inserts the element in the index of each column
                    [self.columns[field].insert(i, value) for field, value in zip(self.header, data)]
        else:
            for i in index:
                # inserts the element in the index of the csv list
                self.csv.insert(i, data)

                # inserts the element in the index of each column
                [self.columns[field].insert(i, value) for field, value in zip(self.header, data)]
        return self

    def update (self, data, _object):
        index = []

        if not [key for key in data.keys()].sort() == self.header.copy().sort():
            return False

        # format the data dict to suit the csv field pattern
        data = [data[field] for field in self.header]

        if not "where" in _object.keys():
            # adds the row to the bottom of the csv list and each column
            self.csv.append(data)
            [self.columns[field].append(value) for field, value in zip(self.header, data)]
            return self

        for key,value in _object["where"].items():
            if key in self.header:
                if value in self.columns[key]:
                    [index.append(self.columns[key].index(value)) for num in range(0, self.columns[key].count(value))]

        # sorts the lists of indexes
        index.sort()

        # mitigates redundancy
        for num in index:
            if index.count(num) > 1:
                index.remove(num)

        # if _object = {"limit": 10}
        if "limit" in _object.keys():
            for num in range(0, _object["limit"]):
                for i in index:
                    # inserts the element in the index of the csv list
                    self.csv[i] = data

                    # inserts the element in the index of each column
                    def func (field, value): self.columns[field][i] = value
                    [func(field, value) for field, value in zip(self.header, data)]
        else:
            for i in index:
                # inserts the element in the index of the csv list
                self.csv[i] = data

                # inserts the element in the index of each column
                def func (field, value): self.columns[field][i] = value
                [func(field, value) for field, value in zip(self.header, data)]
        return self

    def delete (self, _object):
        index = []

        if not "where" in _object.keys():
            return self

        for key,value in _object["where"].items():
            if key in self.header:
                if value in self.columns[key]:
                    [index.append(self.columns[key].index(value)) for num in range(0, self.columns[key].count(value))]

        # sorts the lists of indexes
        index.sort()

        # mitigates redundancy
        for num in index:
            if index.count(num) > 1:
                index.remove(num)

        # if _object = {"limit": 10}
        if "limit" in _object.keys():
            for num in range(0, _object["limit"]):
                for i in index:
                    # removes the row from the csv list
                    self.csv.pop(i)

                    # remove each index from the column
                    [self.columns[field].pop(i) for field in self.header]
        else:
            for i in index:
                # removes the row from the csv list
                self.csv.pop(i)

                # remove each index from the column
                [self.columns[field].pop(i) for field in self.header]
        return self

    def deleteAll (self):
        self.csv.clear()
        [self.columns[field].clear() for field in self.header]

    def save (self, filepath = "", unparser = unparser):
        if filepath == "":
            if not self.filepath:
                raise Exception("Invalid file path supplied!")
            filepath = self.filepath

        self.unparse(unparser)

        with open(filepath, "w", newline = "") as file:
            writer = csv.writer(file)
            writer.writerow(self.header)
            writer.writerows(self.unparse_csv)

if __name__ == "__main__":
    # app = CSVParser("students.csv")
    app = CSVParser("sample.csv")

    # print(app.select({"where":{"NAME": "David"}}))
    # print(app.selectAll())
    # app.update({"NAME": "Robin", "HAIR_COLOR": "black"}, {"where":{"HAIR_COLOR": "brown"}})
    # app.insert({"NAME": "Robin", "HAIR_COLOR": "black"}, {"where":{"HAIR_COLOR": "black"})
    # app.insert({"NAME": "Robin", "HAIR_COLOR": "black"}, {"where":{"HAIR_COLOR": "black"}, "limit": 2})
    # app.insert({"NAME": "Robin", "HAIR_COLOR": black})
    # app.delete({"where":{"NAME": "David"}})
    # app.deleteAll()

    app.insert({"NAME": "Test User", "NICKNAME": "test", "AGE": 10, "CLASS": "JSS1"})
    app.save()
    # print(app.selectColumn("NAME"))
    # print(app.csv)
    # print(app.select({"where": {"NICKNAME": "uche"}}))
    # print(app.select({"where": {"NICKNAME": "dave"}}))
    # print(app.select({"where": {"NICKNAME": "josh"}}))
    # print(app.select({"where": {"NICKNAME": "joshua"}}))
