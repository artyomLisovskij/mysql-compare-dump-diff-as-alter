import parse
import os

def same_params(params1, params2):
    list1 = params1.split()
    list2 = params2.split()
    if len(list2) == len(list1):
        for idx, val in enumerate(list1):
            if list2[idx] != val:
                return False
    else:
        return False      
    return True

def compare_two_dicts_and_return_alter(db_dict1, db_dict2):
    output_sql = ''
    for key, value in db_dict1.items():
        if key not in db_dict2:
            # no such table.
            # form create table total
            output_temp = ''
            for key2, value2 in value.items():
                output_temp = '%s\n `%s` %s' % (output_temp, key2, value2) 
            output_sql = '%s\n CREATE TABLE `%s` ( %s ) ENGINE=InnoDB DEFAULT CHARSET=utf8;' % (output_sql, key, output_temp) 
        else:
            # such table exists
            output_temp = ''
            for key2, value2 in value.items():
                if key2 not in db_dict2[key]:
                    # add
                    # ALTER TABLE `tablename` ADD `fieldname` [params];
                    output_temp = '%s\n ALTER TABLE `%s` ADD `%s` %s;' % (output_temp, key, key2, value2) 
                else:
                    # compare params and modify if needed
                    # ALTER TABLE `tablename` MODIFY `fieldname` [params];
                    if not same_params(value2, db_dict2[key][key2]):
                        output_temp = '%s\n ALTER TABLE `%s` MODIFY `%s` %s;' % (output_temp, key, key2, value2) 
            output_sql = '%s %s' % (output_sql, output_temp) 
    return output_sql

def parse_db_to_dict(db_string=''):
    temp_dict = {}
    for table in parse.findall("CREATE TABLE `{}` ({}) ENGINE=InnoDB", db_string):
        # table[0] = tablename
        # table[1] = all table fields
        temp_table_dict = {}
        for field in parse.findall("`{}` {},\n", table[1]):
            # field[0] = field name
            # field[1] = field description
            temp_table_dict[field[0]] = field[1]
        temp_dict[table[0]] = temp_table_dict
    return temp_dict

import argparse

parser = argparse.ArgumentParser(description='Find diff in two MySQL dumps and create diff file with ALTER commands(like migration')
parser.add_argument('db_file1', type=str, nargs=1, help='dbdump1')
parser.add_argument('db_file2', type=str, nargs=1, help='dbdump2')
parser.add_argument('output_file', type=str, nargs=1, help='output file')
args = parser.parse_args()
args = vars(args)

path1 = args['db_file1'][0]
path2 = args['db_file2'][0]
path3 = args['output_file'][0]
with open(path1, 'r') as myfile:
    db1_string=myfile.read()

with open(path2, 'r') as myfile:
    db2_string=myfile.read()

db1_dict = parse_db_to_dict(db1_string)
db2_dict = parse_db_to_dict(db2_string)

diff_sql_alter = compare_two_dicts_and_return_alter(db1_dict, db2_dict)
with open(path3, 'w') as f:
    print(diff_sql_alter, file=f)

print('Success')
