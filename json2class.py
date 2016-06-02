#coding: utf-8

import urllib2, urllib, os, json

class Clazz:
    def __init__(self, clazz_name, fields=None):
        self.clazz_name = clazz_name
        self.fields = fields

    def add_field(self, field):
        if self.fields is None:
            self.fields = []
        self.fields.append(field)

    def __upper_first_letter(self, s):
        return s[0].upper()+s[1:]

    def __getter_setter(self):
        c = ''
        for field in self.fields:
            u_field = self.__upper_first_letter(field[1])
            c+='\tpublic '+field[0]+' get'+u_field+"(){\n\t\treturn this."+field[1]+';\n\t}\n'
            c+='\tpublic void set'+u_field+'('+field[0]+' '+field[1]+'){\n\t\tthis.'+field[1]+'='+field[1]+';\n\t}\n'
        return c

    def code(self):
        cont = 'public class '+self.clazz_name+' {\n'
        for field in self.fields:
            cont+='\tprivate '+field[0]+' '+field[1]+';\n'
        cont += self.__getter_setter()
        cont += '}\n'
        return cont

def read_json():
    f = open('req.json')
    c = f.read()
    f.close()
    data = json.loads(c, 'utf-8')
    make_class(data,'Parent')

def make_class(data, class_name):
    clazz = Clazz(class_name)
    for k, v in data.items():
        if type(v) == dict:
            clazz_name = upper_first_letter(k)
            make_class(v, clazz_name)
            clazz.add_field((clazz_name, k))
        elif type(v) == list:
            clazz_name = upper_first_letter(k)[:-1]
            make_class(v[0], clazz_name)
            clazz.add_field(('List<%s>' % clazz_name, k))
        elif type(v) == int:
            clazz.add_field(('Integer', k))
        else:
            clazz.add_field(('String', k))
    print clazz.code()

def upper_first_letter(s):
    if len(s)==0:
        return s
    return s[0].upper()+s[1:]

def write_file(file_name, content):
    file_name = 'ota_class'+ os.path.sep+file_name+'.java'
    if os.path.isfile(file_name):
        print file_name + 'exists!'
        return
    f = open(file_name, 'w')
    f.write(content)
    f.close()

if __name__ == '__main__':
    read_json()
