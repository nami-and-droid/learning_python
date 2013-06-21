__tab = '\t'


def __wrapper(val):
    if isinstance(val, basestring):
        return '"%s"' % val
    elif isinstance(val, bool):
        return str(val).lower()
    else:
        return str(val)


def generate(struct, indent=__tab):
    res = ''
    for section in struct:
        if isinstance(struct[section], dict):
            part = generate(struct[section], indent + __tab)
        elif isinstance(struct[section], list):
            part = '[' + ', '.join(map(__wrapper, struct[section])) + ']'
        else:
            part = __wrapper(struct[section])
        res += '\n%s"%s": %s,' % (indent, section, part)
    return "{%s%s}" % (res[:-1], '\n' + indent[:-1] if len(res) else '')
