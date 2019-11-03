#! py -3
# -*- coding: utf-8 -*-

import re

mapper_template = '''<?xml version="1.0" encoding="UTF-8" ?>
<!DOCTYPE mapper PUBLIC "-//mybatis.org//DTD Mapper 3.0//EN" "http://mybatis.org/dtd/mybatis-3-mapper.dtd" >
<mapper namespace="{}">
{}
</mapper>'''


def to_java_name(col):
    parts = col.split('_')
    name = parts[0]
    for i in range(1, len(parts)):
        name += parts[i][0].upper() + parts[i][1:]
    return name


def to_class_name(col):
    name = to_java_name(col)
    return name[0].upper() + name[1:]


class SqlParser(object):
    def __init__(self, sql, exclude_cols=None):
        if exclude_cols is None:
            exclude_cols = []

        table_pattern = re.compile(r"CREATE\s+TABLE\s+`(\w+)`")
        table_match = re.search(table_pattern, sql)
        table_name = table_match.group(1)

        pattern = re.compile(r'^\s+`(\w+)`\s+(\w+)')
        cols = []
        typed_cols = []
        for line in sql.split('\n'):
            match = re.search(pattern, line)
            if match and match.group(1) not in exclude_cols:
                cols.append(match.group(1))
                typed_cols.append((match.group(1), match.group(2)))

        self.cols = cols
        self.typed_cols = typed_cols
        self.table_name = table_name

    def gen_result_map(self):
        result = '<result column="{}" property="{}"/>'
        results = '\n'.join([result.format(col, to_java_name(col)) for col in self.cols])

        map_id = to_java_name(self.table_name)
        map_type = to_class_name(self.table_name)
        return '<resultMap id="{}" type="{}">\n{}\n</resultMap>'.format(map_id, map_type, results)

    def gen_update_sql(self):
        update_sql = '<update id="update">\nUPDATE {} SET id=id\n{}\nWHERE id=#{{id}}\n</update>'

        return update_sql.format(
            self.table_name, '\n'.join([self._gen_update_item(typed_col) for typed_col in self.typed_cols]))

    @staticmethod
    def _gen_update_item(typed_col):
        field = to_java_name(typed_col[0])
        if 'int' in typed_col[1]:
            test = "%s != 0" % field
        elif 'time' in typed_col[1] or 'date' in typed_col[1]:
            test = "%s != null" % field
        else:
            test = "%s != null and %s !=''" % (field, field)

        return '<if test="%s">\n,%s=#{%s}\n</if>' % (test, typed_col[0], to_java_name(typed_col[0]))

    def gen_mapper(self):
        cols_no_id = list(filter(lambda col: col != 'id', self.cols))

        result_map = self.gen_result_map()
        cols_sql = '<sql id="cols">\n{}\n</sql>'.format(','.join(self.cols))
        select_sql = ('<select id="get" resultMap="{}">\n'
                      'SELECT\n<include refid="cols"/>\nFROM {}\nWHERE id=#{{id}}\n'
                      '</select>').format(to_java_name(self.table_name), self.table_name)
        insert_sql = '<insert id="insert">\nINSERT INTO {}\n({})\nVALUES\n({})\n</insert>'.format(
            self.table_name, ','.join(cols_no_id), ','.join('#{%s}' % to_java_name(col) for col in cols_no_id))
        update_sql = self.gen_update_sql()

        return mapper_template.format(to_class_name(self.table_name) + 'Mapper',
                                      "\n\n".join((result_map, cols_sql, select_sql, insert_sql, update_sql)))

    def gen_java_fields(self):
        fields = []
        for typed_col in self.typed_cols:
            field = ['private']
            if 'bigint' == typed_col[1]:
                field.append('long')
            elif 'int' == typed_col[1]:
                field.append('int')
            elif 'int' in typed_col[1]:
                field.append('short')
            elif 'time' in typed_col[1] or 'date' in typed_col[1]:
                field.append('Date')
            elif 'decimal' == typed_col[1]:
                field.append('BigDecimal')
            else:
                field.append('String')
            field.append(to_java_name(typed_col[0]))
            fields.append(field)
        return '\n'.join([' '.join(field) + ';' for field in fields])


if __name__ == '__main__':
    with open('test.sql', encoding='utf-8') as f:
        sql = f.read()
    parser = SqlParser(sql, ['create_date', 'update_date', 'is_deleted'])
    # parser = SqlParser(sql, ['update_date'])
    mapper = parser.gen_mapper()
    print(mapper)
    print()
    print(parser.gen_java_fields())
