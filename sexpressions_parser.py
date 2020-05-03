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


import re

term_regex = r'''(?mx)
    \s*(?:
        (?P<open>\()|
        (?P<close>\))|
        (?P<sq>"(?:\\\\|\\"|[^"])*")|
        (?P<s>[^(^)\s]+)
       )'''
pattern = re.compile(term_regex)


def parse_sexpression(sexpression):
    stack = []
    out = []
    for terms in pattern.finditer(sexpression):
        term, value = [(t, v) for t, v in terms.groupdict().items() if v][0]
        if term == 'open':
            stack.append(out)
            out = []
        elif term == 'close':
            assert stack, "Trouble with nesting of brackets"
            tmp, out = out, stack.pop(-1)
            out.append(tmp)
        elif term == 'sq':
            out.append(value[1:-1].replace('\\\\', '\\').replace('\\"', '"'))
        elif term == 's':
            out.append(value)
        else:
            raise NotImplementedError("Error: %s, %s" % (term, value))
    assert not stack, "Trouble with nesting of brackets"
    return out[0]
