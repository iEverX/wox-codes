# coding: utf-8

import subprocess
import hashlib
import base64
from wox import Wox, WoxAPI


FUNCTIONS = ['md5', 'sha1', 'sha224', 'sha256', 'sha384', 'sha512', 'base64']


class Main(Wox):

    def copy(self, output):
        command = 'echo %s | C:\Windows\system32\clip' % output
        subprocess.Popen(command, shell=True)

    def make_item(self, name, key, output):
        return {
            'Title': output,
            'SubTitle': '%s of %s' % (name, key),
            'IcoPath': 'Images/app.ico',
            'JsonRPCAction': {
                'method': 'copy',
                'parameters': [output],
                'dontHideAfterAction': False
            }
        }

    def hash(self, name, key):
        h = hashlib.new(name.lower())
        h.update(key.encode('utf-8'))
        return self.make_item(name, key, h.hexdigest())

    def b64encode(self, key):
        r = base64.b64encode(key.encode('utf-8')).decode('utf-8')
        return self.make_item('base64', key, r)

    def b64decode(self, key):
        try:
            r = base64.b64decode(key.encode('utf-8')).decode('utf-8')
            return self.make_item('base64 deocde', key, r)
        except:
            return None

    def query(self, key):
        rs = key.split(' ', 1)
        if len(rs) == 1:
            results = [self.hash(x, key) for x in ['md5', 'sha1', 'sha256']]
            results.append(self.b64encode(key))
            return results
        name, key = key.split(' ', 1)
        if name.lower() not in FUNCTIONS:
            return [{
                "Title": "Not supported function - %s " % name,
                "SubTitle": 'supported functions are %s' % ', '.join(FUNCTIONS),         
                "IcoPath":"Images/app.ico"
            }]
        if name.lower() == 'base64':
            results = [self.b64encode(key)]
            d = self.b64decode(key)
            if d:
                results.append(d)
            return results
        else:
            return [self.hash(name, key)]


if __name__ == '__main__':
    Main()