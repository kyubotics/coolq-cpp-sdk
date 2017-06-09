"""CQP C++ Object-oriented Wrapper Generator

This script helps you generate C++ object-oriented wrapper of CoolQ C++ SDK,
which will be handy while using C++ OO to develop plugins instead of pure C.
"""

import os
import re
import sys

TEMPLATE = """#pragma once

#include "cqp.h"

class CQApp {{
public:
    CQApp() {{}};

    CQApp(int32_t authcode) {{
        this->_ac = authcode;
    }}

{}

private:
    int32_t _ac;
}};
"""


def main():
    """Command Line Portal"""
    if len(sys.argv) < 2:
        print('Usage: python generate_hpp.py C:\\path\\to\\cqp.h')
        return

    header_path = os.path.abspath(sys.argv[1])
    with open(header_path, 'r', encoding='gbk') as header_f:
        content = header_f.read()

    functions = ''

    for func_match in re.finditer(r'CQAPI\s*\((?P<return>.*?)\)\s*'
                                  r'(?P<name>[_A-Za-z0-9]+)'
                                  r'\(int32_t\s+.*?(,\s*(?P<params>.*?))?\);', content):
        kwargs = dict(func_match.groupdict())
        if kwargs['params'] is None:
            kwargs['params'] = ''
        kwargs['oo_name'] = kwargs['name'].split('_')[-1]
        print(kwargs['oo_name'])
        if kwargs['params']:
            kwargs['param_names'] = ', ' + ', '.join(
                [re.match(r'^.*?([_A-Za-z0-9]+)\s*$', x).group(1)
                 for x in kwargs['params'].split(',')]
            )
        else:
            kwargs['param_names'] = ''
        kwargs['space1'] = '' if kwargs['return'].endswith('*') else ' '
        functions += ('    {return}{space1}{oo_name}({params}) {{\n'
                      '        return {name}(this->_ac{param_names});\n'
                      '    }}\n\n').format(**kwargs)

    with open('cqp.hpp', 'w', encoding='utf-8') as hpp_f:
        hpp_f.write(TEMPLATE.format(functions.strip('\n')))

    print('OK!')


if __name__ == '__main__':
    main()
