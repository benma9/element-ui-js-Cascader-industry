import json
import pymysql


from pprint import pprint as p
db = pymysql.Connect(host='localhost',port=3306,user='root',db='industry_code')
cursor = db.cursor()
sql = 'select * from Industry '


def query(sql='select * from Industry '):
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

iList = []
for first in query(sql = sql + ' where ParentID is null'):
    f1 = {"label": first[0] + ": " + first[1], "value": first[0], "children": []}
    for second in query(sql=sql + ' where ParentID = "{}"'.format(first[0])):
        f2 = {"label":  second[0] + ": " + second[1], "value": second[0], "children": []}
        for third in query(sql=sql + ' where ParentID = "{}"'.format(second[0])):
            f3 = {"label":  third[0] + ": " + third[1], "value": third[0], "children": []}
            for fourth in query(sql=sql + ' where ParentID = "{}"'.format(third[0])):
                f4 = {"label":  fourth[0] + ": " + fourth[1], "value": fourth[0]}
                f3['children'].append(f4)
            f2['children'].append(f3)
        f1['children'].append(f2)
    iList.append(f1)


for f1 in iList:
    for f2 in f1['children']:
        for f3 in f2['children']:
            if len(f3['children']) == 0:
                f3.pop('children')
        if len(f2['children']) ==0:
            f2.pop('children')


with open('../static/js/industry.js', 'w') as f:
    ins = 'const industryList = ' + json.dumps(iList)
    f.write(ins)
