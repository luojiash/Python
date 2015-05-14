#coding: utf8

import re

def regex_test(pattern, string):
    match = re.findall(pattern, string)
    if match:
        print type(match) #<type 'list'>
        print match
        
def regex_test3(pattern, string):
    match = re.finditer(pattern, string)
    if match:
        print type(match) #<type 'callable-iterator'>
        for it in match:
            print it.group()
        
def regex_test1(pattern, string):
    ''' first way to match '''
    reg = re.compile(pattern)
    match = reg.search(string)
    if match:
        print match.group()

def regex_test2(pattern, string):
    ''' second way to match '''
    match = re.search(pattern, string)
    if match:
        print match.group()    

regex = r'</?[^>]+>' # match all valid or invalid html tag
string = '<div><a href="#">hellp word<invalid></invalid></a></div>'
regex_test(regex, string);
regex_test1(regex, string);
regex_test2(regex, string);
