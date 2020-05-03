"""
From the excellent Interactive HTML BOM project
https://github.com/openscopeproject/InteractiveHtmlBom

MIT License

Copyright (c) 2018 qu1ck

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""


class ParserBase:
    DEFAULT_FIELDS = []

    def __init__(self, file_name):
        """
        :param file_name: path to file that should be parsed.
        """
        self.file_name = file_name

    @staticmethod
    def normalize_field_names(data):
        field_map = {f.lower(): f for f in reversed(data[0])}

        def remap(ref_fields):
            return {field_map[f.lower()]: v for (f, v) in
                    sorted(ref_fields.items(), reverse=True)}

        field_data = {r: remap(d) for (r, d) in data[1].items()}
        return field_map.values(), field_data

    def parse(self, normalize_case):
        data = self.get_extra_field_data()
        if data is None:
            return None
        if normalize_case:
            data = self.normalize_field_names(data)
        return sorted(data[0]), data[1]

    def get_extra_field_data(self):
        # type: () -> tuple
        """
        Parses the file and returns a extra field data.
        :return: tuple of the format
            (
                [field_name1, field_name2,... ],
                {
                    ref1: {
                        field_name1: field_value1,
                        field_name2: field_value2,
                        ...
                    ],
                    ref2: ...
                }
            )
        """
        pass
