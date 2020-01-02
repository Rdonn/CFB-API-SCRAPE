from mpu import io as mio
from re import sub
class TableForTypeORM: 
    def __init__(self, table_name): 
        self.table_name = table_name
        self.column_data = []

    def add_column(self, new_column): 
        self.column_data.append(new_column)
    
    def get_table_source(self): 
        table_source = ""
        table_source += "export class {} ".format(sub(r'[^A-Za-z]', '', self.table_name)) + "{\n\n"

        for decorator, column_name in self.column_data: 
            table_source += "{}\n{};\n".format(decorator, sub(r'[^A-Za-z]', '', column_name) + ":number") + "\n"
        table_source += "@OneToOne(type => Player)\nplayer:Player;\n"
        table_source += "}"
        return table_source

schema = mio.read('fields_for_schema.json')

for table in schema: 
    new_table = TableForTypeORM(table)
    new_table.add_column(("@PrimaryColumn()", "player_id"))
    new_table.add_column(("@PrimaryColumn()", "year_played"))
    for column in schema[table]:
        new_table.add_column(("@Column()", column))
    f = open("typeORM_builder/tables/" + table + ".ts", 'w')
    print(new_table.get_table_source(), file=f)
    f.close()


#just some side work that I don't want to do later... which is establish a relationship between the player table and the new statistics tables
side_work = ""
for table_name in schema: 
    name = sub(r'[^A-Za-z]', '', table_name)
    side_work += "@OneToOne(type => {})\n".format(name)
    side_work += "{}:{};\n".format(name.replace(name[0], name[0].lower(),1), name)

f = open("typeORM_builder/tables/" + "side_work.txt", 'w')
print(side_work, file=f)
f.close()

        


