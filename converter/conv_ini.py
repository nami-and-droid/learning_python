import re
from string import strip
from collections import OrderedDict

pattern_section = re.compile('^\[[\w\d\.]+\]$')
pattern_prop = re.compile('^\w[\w\d\.]*(\[\])? *\t*=.*$')
pattern_float = re.compile('^-?((\d+\.\d*)|(\d*\.\d+))$')
pattern_int = re.compile('^-?[1-9]\d*$')
pattern_comment = re.compile(' *[;#]')


def __get_typed(var):
    if var.startswith('"') and var.endswith('"'):
        return var[1:-1]
    elif pattern_int.match(var):
        return int(var)
    elif pattern_float.match(var):
        return float(var)
    elif var.lower() == 'true':
        return True
    elif var.lower() == 'false':
        return False
    return var


def __add_prop(block, key, val):
    if key not in block:
        block[key] = val
    else:
        if not isinstance(block[key], list):
            block[key] = [block[key]]
        block[key].append(val)


def __check_comment_after_prop(val):
    comment = pattern_comment.search(val)
    #comment symbol is not into quotes
    if comment and ((not val.startswith('"')) or
                    val.find('"', 1, comment.start()) >= 0):
        return comment.start()
    return None


def parse(fname):
    #ignore comment strings and blank lines in file
    nextln = (ln for ln in (ln.rstrip() for ln in open(fname, 'r')) if ln
              and not ln.startswith(('#', ';')))
    struct = OrderedDict()
    for line in nextln:
        if pattern_section.match(line):
            sect_name = line[1:-1]
            struct[sect_name] = OrderedDict()

        elif pattern_prop.match(line) and sect_name:
            key, val = map(strip, line.split('=', 1))
            #handle value transfered to the next line
            while val.endswith('\\'):
                try:
                    val = val[:-1] + next(nextln)
                except StopIteration:
                    #TODO: handle unexpected end of file
                    pass
            #if there is comment after property - remove it
            ind_comm = __check_comment_after_prop(val)
            val = __get_typed(val[:ind_comm] if ind_comm is not None else val)
            __add_prop(struct[sect_name], key, val)

    return struct
