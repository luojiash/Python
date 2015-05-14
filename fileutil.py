#encoding: utf-8

def save(path, data):
    file = open(path, 'wb')
    file.write(data)
    file.close()
