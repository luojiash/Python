#! py -3
# -*- coding: utf-8 -*-

import re
from functools import reduce
from optparse import OptionParser

mapper_template = '''<resultMap id="{resultMapId}" type="{resultMapType}">
{results}</resultMap>
'''

cols_template = '''<sql id="cols">
        {cols}
    </sql>
'''


class MapperParser:
    def __init__(self, path, table='TABLE'):
        self.table = table
        self.fields = []
        f = open(path, encoding='utf-8')
        for line in f:
            if line.startswith('package'):
                package = line.split()[1][:-1]
                break
        self.simple_clazz = path[path.rfind('\\') + 1:path.rfind('.')]
        self.clazz = package + '.' + self.simple_clazz

        r = re.compile(r'(private|public|protected)\s+(\w+)\s+(\w+)\s*[;=]')
        for line in f:
            m = re.search(r, line)
            if m and not m.group(3).startswith('_'):
                # print(m.group(3))
                self.fields.append(m.group(3))
        f.close()

    def gen_mapper(self):
        template = '\t<result column="%s" property="%s"/>\n'
        # list(map(lambda f: print(template % (split_word(f), f)), self.fields))
        rs = ''.join([template % (split_word(f), f) for f in self.fields])
        print(mapper_template.format(
            resultMapId=self.simple_clazz[0].lower() + self.simple_clazz[1:],
            resultMapType=self.clazz, results=rs))

    def gen_cols(self):
        cols = ','.join(list(map(lambda f: split_word(f), self.fields)))
        print(cols_template.format(cols=cols))

    def gen_insert(self):
        s1 = reduce(lambda s, f: '%s#{%s},' % (s, f), self.fields, '')
        s2 = reduce(lambda s, f: '%s%s,' % (s, split_word(f)), self.fields, '')
        print('INSERT INTO ' + self.table + '\n(' + s2[:-1] + ')\nVALUES\n(' + s1[:-1] + ')\n')

    def gen_update(self):
        r = reduce(lambda s, f: '%s%s=#{%s},' % (s, split_word(f), f), self.fields, '')
        print(r[:-1])

    def gen_insert_list(self, item='item'):
        r = reduce(lambda s, f: '%s#{%s.%s},' % (s, item, f), self.fields, '')
        print(r[:-1])

    def gen_sql(self):
        r = reduce(lambda s, f: '%s%s varchar(31) comment \'\',\n' % (s, split_word(f)), self.fields, '')
        print(r[:-2])

    def gen_if_update(self):
        template = '''<if test="{name} != null and {name} !=''">\n\t,{column}=#{{{name}}}\n</if>\n'''
        r = reduce(lambda s, f: s + template.format(name="" + f, column=split_word(f)), self.fields, '')
        print(r[:-1])


def split_word(w):
    r = []
    start = 0
    for i in range(len(w)):
        if w[i].isupper():
            r.append(w[start:i].lower())
            start = i
    r.append(w[start:len(w)].lower())
    return '_'.join(r)


if __name__ == '__main__':
    option_parser = OptionParser()
    option_parser.add_option('-t', '--table', default='TABLE')
    (options, args) = option_parser.parse_args()

    if len(args) != 1:
        option_parser.print_help()
        exit()

    p = args[0]
    parser = MapperParser(p, options.table)
    parser.gen_mapper()
    parser.gen_cols()
    parser.gen_insert()
    parser.gen_update()
    parser.gen_insert_list('banner')
    parser.gen_if_update()
    # parser.gen_sql()

    for field in parser.fields:
        print("dto.set%s();" % (field[0].upper() + field[1:]))
