#  Copyright 2021 Dennis Kreber
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


class DatabaseConnectInformation:
    def __init__(self):
        self.mongodb_url = None
        self.mongodb_db = None
        self.mongodb_collection = None
        self.tinydb_path = None

    def setup_mongodb_connection(self, url, database, collection="runs"):
        self.mongodb_url = url
        self.mongodb_db = database
        self.mongodb_collection = collection

    def setup_tinydb_connection(self, file_path):
        self.tinydb_path = file_path

    def has_mongodb_connection(self):
        return self.mongodb_db is not None and self.mongodb_db is not None

    def has_tinydb_connection(self):
        return self.tinydb_path is not None

    def has_connection(self):
        return self.has_mongodb_connection() or self.has_tinydb_connection()
