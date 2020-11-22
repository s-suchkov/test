import os


import json
from pandas import DataFrame

# import numpy as np
from jsonschema import validate, Draft7Validator, ValidationError

from mytest.mytest.settings import BASE_DIR

files_event = os.listdir(os.path.join(BASE_DIR, 'event'))
files_schema = os.listdir(os.path.join(BASE_DIR, 'schema'))
result = []
for schema in files_schema:
    for event in files_event:
        list = []
        list.append(schema)
        list.append(event)
        with open(os.path.join(BASE_DIR , f'event/{event}'), 'r') as a, open(os.path.join(BASE_DIR , f'schema/{schema}'), 'r') as b:
            json_event = json.load(a)
            json_schema = json.load(b)
        if json_event:
            v = Draft7Validator(json_schema)
            try:
                validate(json_event['data'],json_schema)
                list.append(True)
                # print(f'Для файла {event} соответствует схема {schema}')
            except ValidationError:
                print(v.iter_errors(json_event['data']))
                list.append(False)
                errors = []
                for error in v.iter_errors(json_event['data']):
                    print(error.message)
                    errors.append(error.message)
                list.append(errors)
                print(f'{event} не подходит {schema}')
        else:
            list.append(False)
            list.append('файл пустой')
            print(f'{event} не подходит ни к одной схеме')
        result.append(list)
print(result)
frame = DataFrame(result,
    columns = ['Схема','Экземпляр','Подходит','Ошибки'])
s = ['<HTML>']
s.append('<HEAD><TITLE>My test</TITLE></HEAD>')
s.append('<BODY>')
s.append(frame.to_html())
s.append('</BODY></HTML>')
html = ''.join(s)
with open (os.path.join(BASE_DIR , 'templates/base.html'), 'w') as html_file:
    html_file.write(html)