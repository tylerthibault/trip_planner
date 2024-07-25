from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask import flash

class Base:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def get_valid_attributes(attributes, data):
        valid_attrs = {}
        for key in data:
            if key in attributes:
                valid_attrs[key] = data[key]
        return valid_attrs

    @staticmethod
    def sanitize(valid_attrs, **data):
        columns = ""
        values = ""
        for index, key in enumerate(valid_attrs):
                columns += key
                values += f"%({key})s"

                if index < len(valid_attrs) - 1:
                    columns += ", "
                    values += ', '
        return {
            'columns': columns, 
            'values':values
        }

    @staticmethod
    def generate_paired(valid_attrs, **data):
        returnString = ""
        for index, key in enumerate(valid_attrs):
            returnString += f"{key}=%({key})s"
            if index < len(valid_attrs) - 1:
                returnString += ', '
        return returnString

    @staticmethod
    def generate_where(**data):
        returnString = ""
        for index, key in enumerate(data):
            returnString += f"{key} = '{data[key]}'"
            if index != len(data) - 1:
                returnString += " AND "
        return returnString

    @classmethod
    def create_one(cls, **data):
        # if not cls.validator(**data):
        #     return False
        valid_attrs = cls.get_valid_attributes(cls.__dict__['attributes'], data)
        info = cls.sanitize(valid_attrs, **data)
        query = f"INSERT INTO {cls.table_name} ({info['columns']}) VALUES ({info['values']});"
        return connectToMySQL(DATABASE).query_db(query, data)
        

    @classmethod
    def get(cls, **data):
        valid_attrs = cls.get_valid_attributes(cls.__dict__['attributes'], data)
        where_data = cls.generate_where(**data)
        query = f"SELECT * FROM {cls.table_name} WHERE {where_data};"
        result = connectToMySQL(DATABASE).query_db(query, data)

        print(result)
        if not result:
            print("base model - get function - no record found")
            return False
        if len(result) > 1:
            list = []
            for item in result:
                list.append(cls(item))
            return list
            
        return cls(result[0])

    @classmethod
    def get_all(cls, where=False, **data):
        if not where:
            query = f"SELECT * FROM {cls.table_name};"
            results = connectToMySQL(DATABASE).query_db(query)
        else:
            where_data = cls.generate_where(**data)
            query = f"SELECT * FROM {cls.table_name} WHERE {where_data};"
            results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            print("base model - get_all function - fail")
            return []
        all_items = []
        for dict in results:
            all_items.append(cls(dict))
        return all_items

    @classmethod
    def update_one(cls, where:dict, **data):
        """Updates a row in the database

        Args:
            where (dict): takes in one or multiple where conditions in order to find a row in the database

            kwargs: takes in key word arguments for the fields in which to update in the database
        """
        valid_attrs = cls.get_valid_attributes(cls.__dict__['attributes'], data)
        info = cls.generate_paired(valid_attrs, **data)

        where_string = cls.generate_where(where)
        query = f"UPDATE {cls.table_name} SET {info} WHERE {where_string};"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete_one(cls, **where:dict) -> None:
        """Deletes a table in the database

        Args:
            where (dict): takes in keys that match the records in which you want to delete
        """
        where_string = cls.generate_where(where)
        query = f"DELETE FROM {cls.table_name} WHERE {where_string};"
        return connectToMySQL(DATABASE).query_db(query)

    @classmethod
    def validator(cls, **data):
        is_valid = True

        for key in data:
            if key in cls.required_attributes:
                print(f"checking key: {key} -> ({data[key]}) on table: {cls.table_name}")
                print(type(data[key]))
                if type(data[key]) == str:
                    if len(data[key]) < 1:
                        print("not valid")
                        is_valid = False
                        flash("*Field is required", f"err_{cls.table_name}_{key}")
        
        return is_valid