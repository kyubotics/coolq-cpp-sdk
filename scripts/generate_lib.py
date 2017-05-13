"""CQP Import Library Generator

This script helps you to generate a import library file (not a static library)
corresponding to CQP.dll, so that you can keep your CoolQ C++ SDK as new as it can be.

You should run this script in a "VS Developer Command Prompt",
because "lib.exe" command is needed.
"""

import os
import re
import sys

from size_tbl import SIZE_TABLE


def get_type_size(param_t):
    """Get C Type Size"""
    param_t = re.sub('const|unsigned|signed', '', param_t).strip()

    if param_t.endswith('*'):
        # pointer type
        return 4

    return SIZE_TABLE[param_t]  # if KeyError raised, let it go


def parse_header_file(header_path):
    """Parse Header File

    Parse function definitions in header file, calculate parameters' size,
    write to .def file.
    """
    header_path = os.path.abspath(header_path)
    with open(header_path, 'r', encoding='gbk') as header_f:
        content = header_f.read()

    with open('CQP.def', 'w') as def_f:
        def_f.write('LIBRARY CQP\nEXPORTS\n')

        for func_match in re.finditer(r'CQAPI\s*\(.*?\)\s*'
                                      r'(?P<name>[_A-Za-z0-9]+)\((?P<params>.*?)\);', content):
            def_f.write(func_match.group('name'))

            param_types = list(map(lambda p: re.sub(r'\s*[_A-Za-z0-9]+$', '', p),
                                   map(str.strip, func_match.group('params').split(','))))
            param_size = 0
            for param_t in param_types:
                param_size += get_type_size(param_t)

            def_f.write('@{}\n'.format(param_size))

        def_f.write('cq_start@4')


def generate_lib_file():
    """Generate .lib File

    Really generate the .lib file (which is incorrect right now).
    """
    os.system('lib.exe /def:CQP.def /out:CQP.lib /machine:x86 > NUL 2>&1')


def fix_lib_file():
    """Fix Type Name of .lib File

    Change type name of functions from "no prefix" to "undecorate".
    """
    with open('CQP.lib', 'rb') as lib_f:
        binary = lib_f.read()

    # magic happens here
    # see https://social.msdn.microsoft.com/Forums/vstudio/en-US/d5685e3d-a3f7-4268-9dfe-c7
    # bc2f638972/important-undecorated-dll-import?forum=vcgeneral
    binary = binary.replace(b'\x08\x00\x5f', b'\x0c\x00\x5f')

    with open('CQP.lib', 'wb') as lib_f:
        lib_f.write(binary)


def which(file):
    """Find Command Path"""
    for path in os.environ["PATH"].split(os.pathsep):
        if os.path.exists(os.path.join(path, file)):
            return os.path.join(path, file)
    return None


def main():
    """Command Line Portal"""
    if len(sys.argv) < 2:
        print('Usage: python generate_lib.py C:\\path\\to\\cqp.h')
        return
    if which('lib.exe') is None:
        print('Please run this script in a "VS Developer Command Prompt".')
        return

    print('Parsing header file...')
    parse_header_file(sys.argv[1])

    print('Generating lib file...')
    generate_lib_file()
    fix_lib_file()

    print('Cleaning up...')
    os.remove('CQP.exp')
    os.remove('CQP.def')

    print('OK!')


if __name__ == '__main__':
    main()
