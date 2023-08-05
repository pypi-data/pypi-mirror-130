from pydantic import BaseModel, Field
import typing
from typing import Iterable, Optional, Union, List, Any
import sqlalchemy
from sqlalchemy import select, func, or_
from pickle import dumps, loads

class _Generic(BaseModel):
    pass

def resolve_missing_attribute(missing_error: str):
    try:
        missing_attr = ''.join(
            missing_error.split("Can't get attribute")[1].split('on <module')
        ).split('from')[0].split(' ')[1][1:-1]

        missing_mod = ''.join(
            missing_error.split("Can't get attribute")[1].split('on <module')
        ).split('from')[0].split(' ')[3][1:-1]

        mod = __import__(missing_mod)
        setattr(mod, missing_attr, _Generic)
    except Exception:
        pass


class BaseMeta:
    translations: dict = {
        str: sqlalchemy.String,
        int: sqlalchemy.Integer,
        float: sqlalchemy.Float,
        bool: sqlalchemy.Boolean,
        dict: sqlalchemy.LargeBinary,
        list: sqlalchemy.LargeBinary,
        tuple: sqlalchemy.LargeBinary
    }
    tables: dict = {}

def PrimaryKey(default=..., ):
    if isinstance(default, type(lambda x: x)):
        return Field(default_factory=default, primary_key=True)
    return Field(default=default, primary_key=True)

def Default(default=...):
    if isinstance(default, type(lambda x: x)):
        return Field(default_factory=default)
    return Field(default=default)
class DataBaseModelCondition:
    def __init__(
        self, 
        description: str,
        condition: sqlalchemy.sql.elements.BinaryExpression,
        values
    ): 
        self.description = description
        self.condition = condition
        self.values = values
    def __repr__(self):
        return self.description
    def str(self):
        return self.description

class DataBaseModelAttribute:
    def __init__(
        self, 
        name: str,
        column: sqlalchemy.sql.schema.Column,
        table,
        serialized: bool = False
    ):
        self.name = name
        self.column = column
        self.table = table
        self.serialized = serialized
    def process_value(self, value):
        if self.name in self.table['foreign_keys']:
            foreign_table_name = value.__class__.__name__
            primary_key = value.__class__.__metadata__.tables[foreign_table_name]['primary_key']
            return getattr(value, primary_key)
        if self.serialized:
            return dumps(value)

        return value

    def __lt__(self, value) -> DataBaseModelCondition:
        values = self.process_value(value)
        return DataBaseModelCondition(
            f"{self.name} < {values}",
            self.column < self.process_value(value),
            (values,)
        )

    def __le__(self, value) -> DataBaseModelCondition:
        values = self.process_value(value)
        return DataBaseModelCondition(
            f"{self.name} <= {values}",
            self.column <= self.process_value(value),
            (values,)
        )

    def __gt__(self, value) -> DataBaseModelCondition:
        values = self.process_value(value)
        return DataBaseModelCondition(
            f"{self.name} > {values}",
            self.column > self.process_value(value),
            (values,)
        )

    def __ge__(self, value) -> DataBaseModelCondition:
        values = self.process_value(value)
        return DataBaseModelCondition(
            f"{self.name} >= {values}",
            self.column >= self.process_value(value),
            (values,)
        )

    def __eq__(self, value) -> DataBaseModelCondition:
        values = self.process_value(value)
        return DataBaseModelCondition(
            f"{self.name} == {values}",
            self.column == self.process_value(value),
            (values,)
        )

    def matches(self, choices: List[Any]) -> DataBaseModelCondition:
        choices = [self.process_value(value) for value in choices]
        return DataBaseModelCondition(
            f"{self.name} in {choices}",
            self.column.in_(choices),
            tuple(choices)
        )

class DataBaseModel(BaseModel):
    __metadata__: BaseMeta = BaseMeta()

    @classmethod
    def check_if_subtype(cls, field):

        database_model = None
        if isinstance(field['type'], typing._GenericAlias):
            for sub in field['type'].__args__:
                if issubclass(sub, DataBaseModel):
                    if database_model:
                        raise Exception(f"Cannot Specify two DataBaseModels in Union[] for {field['name']}")
                    database_model = sub
        elif issubclass(field['type'], DataBaseModel):
            return field['type']
        return database_model
            
        

    @classmethod
    async def refresh_models(cls):
        """
        convert rows into .dict() & save back to DB, refreshing any changed 
        models
        """
        rows = await cls.all()
        rows_dict = [row.dict() for row in rows]
        rows_model = [cls(**row) for row in rows_dict]
        for row in rows_model:
            await row.update()

    @classmethod
    def setup(cls, database):
        
        if not hasattr(cls.__metadata__, 'metadata'):
            cls.init_set_metadata(database.metadata)
            cls.init_set_database(database)
        if cls.__name__ not in cls.__metadata__.tables:
            cls.generate_sqlalchemy_table()
        
    @classmethod
    def init_set_metadata(cls, metadata):
        """
        Applies an instantiated sqlalchemy.MetaData() instance to __metadata__.metadata
        """
        cls.__metadata__.metadata = metadata
    
    @classmethod
    def init_set_database(cls, database):
        """
        Applies an instantiated easydb.Database() instance to __metadata__.database
        """
        cls.__metadata__.database = database

    @classmethod
    def generate_sqlalchemy_table(cls):
        if not hasattr(cls.__metadata__, 'metadata'):
            raise Exception(f"No connected sqlalchemy.MetaData() instance yet, first run {cls}.init_set_metadata()")
        name = cls.__name__

        cls.__metadata__.tables[name]['table'] = sqlalchemy.Table(
            name,
            cls.__metadata__.metadata,
            *cls.convert_fields_to_columns()
        )
        cls.generate_model_attributes()
    @classmethod 
    def generate_model_attributes(cls):
        name = cls.__name__
        for c, column in cls.__metadata__.tables[name]['column_map'].items():
            sql_c = c
            if c in cls.__metadata__.tables[name]['foreign_keys']:
                sql_c = cls.__metadata__.tables[name]['foreign_keys'][c]
            setattr(
                cls, 
                c, 
                DataBaseModelAttribute(
                    c,
                    cls.__metadata__.tables[name]['table'].c[sql_c],
                    cls.__metadata__.tables[name],
                    column[2]
                )
            )

        
    @classmethod
    def convert_fields_to_columns(
        cls, 
        model_fields: list = None, 
        include: list = None,
        alias: dict = None,
        update: bool = False
    ):
        """
        primary key is assumed to be first field, #TODO - add override later
        """
        if not alias:
            alias = {}
        if not include:
            include = [f for f in cls.__fields__]

        primary_key = None
        array_fields = set()

        for property, config in cls.schema()['properties'].items():
            
            if 'primary_key' in config:
                if primary_key:
                    raise Exception(f"Duplicate Primary Key Specified for {cls.__name__}")
                primary_key = property
            if 'type' in config and config['type'] == 'array':
                array_fields.add(property)

        if not model_fields:
            model_fields_list = [
                f for _,f in cls.__fields__.items() 
                if f.name in include or f.name in alias
            ]
            model_fields = []
            for field in model_fields_list:
                field_name = field.name
                if field.name in alias:
                    field_name = alias[field.name]
                model_fields.append({'name': field_name, 'type': field.type_, 'required': field.required})

        name = cls.__name__
        primary_key = model_fields[0]['name'] if not primary_key else primary_key
        if name not in cls.__metadata__.tables or update:

            cls.__metadata__.tables[name] = {
                'primary_key': primary_key,
                'column_map': {},
                'foreign_keys': {},
            }

        columns = []
        for i, field in enumerate(model_fields):
            data_base_model = cls.check_if_subtype(field)
            if data_base_model:
                # ensure DataBaseModel also exists in Database, even if not already
                # explicity added
                cls.__metadata__.database.add_table(data_base_model)

                # create a string or foreign table column to be used to reference 
                # other table
                foreign_table_name = data_base_model.__name__
                foreign_primary_key_name = data_base_model.__metadata__.tables[foreign_table_name]['primary_key']
                foreign_key_type = data_base_model.__metadata__.tables[foreign_table_name]['column_map'][foreign_primary_key_name][1]

                serialize = field['name'] in array_fields

                cls.__metadata__.tables[name]['column_map'][field['name']] = (
                    cls.__metadata__.database.get_translated_column_type(foreign_key_type if not serialize else list)[0],
                    data_base_model,
                    serialize
                )

                # store field name in map to quickly determine attribute is tied to 
                # foreign table
                cls.__metadata__.tables[name]['foreign_keys'][field['name']] =  (
                    f'fk_{foreign_table_name}_{foreign_primary_key_name}'.lower()
                )
                foreign_type_config = cls.__metadata__.tables[name]['column_map'][field['name']][0]
                columns.append(
                    sqlalchemy.Column(
                        cls.__metadata__.tables[name]['foreign_keys'][field['name']],
                        foreign_type_config['column_type'](
                            *foreign_type_config['args'],
                            **foreign_type_config['kwargs']
                        )
                    )
                )
                continue

            # get sqlalchemy column type based on field type & if primary_key
            # as well as determine if data should be serialized & de-serialized
            sqlalchemy_model, serialize = cls.__metadata__.database.get_translated_column_type(
                field['type'],
                primary_key = field['name'] == primary_key
            )
            cls.__metadata__.tables[name]['column_map'][field['name']] = (
                sqlalchemy_model,
                field['type'],
                serialize
            )

            column_type_config = cls.__metadata__.tables[name]['column_map'][field['name']][0]
            columns.append(
                sqlalchemy.Column(
                    field['name'], 
                    column_type_config['column_type'](
                        *column_type_config['args'], 
                        **column_type_config['kwargs']
                    ),
                    primary_key = field['name'] == primary_key
                )
            )

        return columns
    
    @classmethod
    def normalize(cls, results: list):
        """
        ensure results of db querries are dict before parsing
        """
        return [dict(r) for r in results]

    async def serialize(self, data: dict, insert: bool = False, alias=None):
        """
        expects
            `data` - data to be serialized
        """
        if not alias:
            alias = {}

        values = {**data}

        for k, v in data.items():
            
            name = self.__class__.__name__
            serialize = self.__metadata__.tables[name]['column_map'][k][2]

            if k in self.__metadata__.tables[name]['foreign_keys']:

                # use the foreign DataBaseModel's primary key / value 
                foreign_type = self.__metadata__.tables[name]['column_map'][k][1]
                foreign_primary_key = foreign_type.__metadata__.tables[foreign_type.__name__]['primary_key']
                
                foreign_values = [v] if not isinstance(v, list) else v
                fk_values = []

                for v in foreign_values:
                    foreign_model = foreign_type(**v)
                    foreign_primary_key_value = getattr(foreign_model, foreign_primary_key)

                    fk_values.append(foreign_primary_key_value)
                    
                    if insert:
                        exists = await foreign_type.exists(**{foreign_primary_key: foreign_primary_key_value})
                        if not exists:
                            await foreign_model.insert()
                del values[k]

                values[f'fk_{foreign_type.__name__}_{foreign_primary_key}'.lower()] = fk_values[0] if not serialize else dumps(fk_values)

                continue
            
            serialize = self.__metadata__.tables[name]['column_map'][k][2]

            if serialize:
                values[k] = dumps(getattr(self, k))
                continue
            values[k] = v

        return values

    async def save(self):
        primary_key = self.__metadata__.tables[self.__class__.__name__]['primary_key']
        exists = await self.__class__.exists(
            **{primary_key: getattr(self, primary_key)}
        )
        if not exists:
            return await self.insert()
        return await self.update()
    
    @classmethod
    def where(cls, query, where: dict, *conditions):
        table = cls.get_table()
        conditions = list(conditions)

        
        for cond, value in where.items():
            if not isinstance(cond, DataBaseModelAttribute) and  hasattr(cls, cond):
                cond = getattr(cls, cond)
            else:
                raise Exception(f"{cond} is not a valid column in {table}")
            
            conditions.append(cond == value)
            query_value = value
            if cond.serialized:
                query_value = dumps(value)
        values = []
        for condition in conditions:
            query = query.where(condition.condition)
            if isinstance(condition.values, tuple):
                values.extend(condition.values)

        return query, tuple(values)

    @classmethod
    def get_table(cls):
        if cls.__name__ not in cls.__metadata__.tables:
            cls.generate_sqlalchemy_table()

        return cls.__metadata__.tables[cls.__name__]['table']

    @classmethod
    def OR(cls, *conditions, **filters) -> DataBaseModelCondition:
        table = cls.get_table()
        conditions = list(conditions)

        for cond, value in filters.items():
            if not isinstance(cond, DataBaseModelAttribute) and  hasattr(cls, cond):
                cond = getattr(cls, cond)
            else:
                raise Exception(f"{cond} is not a valid column in {table}")

            conditions.append(cond == value)
        values = []
        for cond in conditions:
            if isinstance(cond.values, tuple):
                values.extend(cond.values)

        return DataBaseModelCondition(
            " OR ".join([str(cond) for cond in conditions]),
            or_(*[cond.condition for cond in conditions]),
            values=tuple(values)
        )
        

    @classmethod
    def gt(cls, column, value) -> DataBaseModelCondition:
        table = cls.get_table()
        if not column in table.c:
            raise Exception(f"{column} is not a valid column in {table}")
        
        return DataBaseModelCondition(
            f"{column} > {value}",
            table.c[column] > value,
            value
        )

    @classmethod
    def gte(cls, column, value) -> DataBaseModelCondition:
        table = cls.get_table()
        if not column in table.c:
            raise Exception(f"{column} is not a valid column in {table}")
        return DataBaseModelCondition(
            f"{column} >= {value}",
            table.c[column] >= value,
            value
        )
        

    @classmethod
    def lt(cls, column, value) -> DataBaseModelCondition:
        table = cls.get_table()
        if not column in table.c:
            raise Exception(f"{column} is not a valid column in {table}")
        return DataBaseModelCondition(
            f"{column} < {value}",
            table.c[column] < value,
            value
        )

    @classmethod
    def lte(cls, column, value) -> DataBaseModelCondition:
        table = cls.get_table()
        if not column in table.c:
            raise Exception(f"{column} is not a valid column in {table}")
        return DataBaseModelCondition(
            f"{column} <= {value}",
            table.c[column] >= value,
            value
        )

    @classmethod
    def contains(cls, column, value) -> DataBaseModelCondition:
        table = cls.get_table()
        if not column in table.c:
            raise Exception(f"{column} is not a valid column in {table}")

        return DataBaseModelCondition(
            f"{value} in {column}",
            table.c[column].contains(value),
            value
        )

    @classmethod
    def desc(cls, column):
        table = cls.get_table()
        if not column in table.c:
            raise Exception(f"{column} is not a valid column in {table}")
        return table.c[column].desc()

    @classmethod
    def asc(cls, column):
        table = cls.get_table()
        if not column in table.c:
            raise Exception(f"{column} is not a valid column in {table}")
        return table.c[column].asc()
    
    @classmethod
    async def exists(cls,
        **column_values: dict
    ) -> bool:

        table = cls.get_table()
        primary_key = cls.__metadata__.tables[cls.__name__]['primary_key']

        for k in column_values:
            if k not in table.c:
                raise Exception(f"{k} is not a valid column in  {table} ")


        sel = select([table.c[primary_key]])

        sel, values = cls.where(sel, column_values)

        database = cls.__metadata__.database

        results = await database.fetch(sel, cls.__name__, values)

        return bool(results)
        
    @classmethod
    async def select(cls,
        *selection,
        where: Optional[Union[dict, None]] = None,
        alias: Optional[dict] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = 0,
        order_by = None
    ) -> List[dict]:
        if alias is None:
            alias = {}

        table = cls.get_table()
        database = cls.__metadata__.database

        if selection[0] == '*':
            selection = [k for k in cls.__metadata__.tables[cls.__name__]['column_map']]

        #
        items_to_select = []
        for _sel in selection:
            column_name = _sel

            if column_name in cls.__metadata__.tables[cls.__name__]['foreign_keys']:
                fk_name = cls.__metadata__.tables[cls.__name__]['foreign_keys'][column_name]
                items_to_select.append(table.c[fk_name])
                continue

            if column_name not in table.c:
                raise Exception(f"{column_name} is not a valid column in {table} - columns: {[k for k in table.c]}")
            items_to_select.append(table.c[column_name])
        #
        sel = select(items_to_select)

        values = None
        if where:
            sel, values = cls.where(sel, where)

        sel, values = cls.check_limit_offset(sel, values, limit, offset)

        if order_by is not None:
            sel = sel.order_by(order_by)

        decoded_results = []
        
        results = await database.fetch(sel, cls.__name__, values)

        for result in cls.normalize(results):
            values = {}
            for sel, value in zip(selection, result):
                serialized = cls.__metadata__.tables[cls.__name__]['column_map'][sel][2]

                if sel in cls.__metadata__.tables[cls.__name__]['foreign_keys']:

                    foreign_type = cls.__metadata__.tables[cls.__name__]['column_map'][sel][1]
                    foreign_primary_key = foreign_type.__metadata__.tables[foreign_type.__name__]['primary_key']

                    foreign_primary_key_values = loads(result[value]) if serialized else [result[value]]
                    values[sel] = []
                    for foreign_primary_key_value in foreign_primary_key_values:
                        fk_query_results = await foreign_type.select(
                            '*', 
                            where={foreign_primary_key: foreign_primary_key_value},
                        )
                        values[sel].extend(fk_query_results)
                    if serialized:
                        values[sel] = values[sel]
                        continue

                    values[sel] = values[sel][0] if values[sel] else None
                    continue 

                if serialized:
                    try:
                        values[sel] = loads(result[value])
                    except AttributeError as e:
                        resolve_missing_attribute(
                            str(repr(e))
                        )
                        values[sel] = loads(result[value])
                    
                    continue

                values[sel] = result[value]

                if sel in alias:
                    values[alias[sel]] = values.pop(sel)
            
            if values:
                decoded_results.append(
                    cls(**values)
                )

        return decoded_results

    @classmethod
    def check_limit_offset(cls, query, values, limit, offset):
        values = list(values) if values else []

        if limit:
            query = query.limit(limit)

        if offset:
            query = query.offset(offset)
        
        if not values:
            values = [limit, offset]
        elif values and (limit or offset):
            values.extend([limit, offset])

        return query, values

    @classmethod
    async def all(
        cls, 
        limit: int = None, 
        offset: int = 0,
        order_by = None
    ):
        parameters = {}
        if limit:
            parameters['limit'] = limit
        if offset:
            parameters['offset'] = offset
        if order_by is not None:
            parameters['order_by'] = order_by

        return await cls.select('*', **parameters)

    @classmethod
    async def count(cls):
        table = cls.get_table()
        database = cls.__metadata__.database
        sel = select([func.count()]).select_from(table)
        results = await database.fetch(sel, cls.__name__)
        return results[0][0] if results else 0

    @classmethod
    async def filter(
        cls, 
        *conditions, 
        limit: int = None, 
        offset: int = 0,
        order_by = None, 
        count_rows: bool = False,
        **column_filters
    ):
        table = cls.get_table()
        database = cls.__metadata__.database

        columns = [k for k in cls.__fields__]
        if not column_filters and not conditions:
            raise Exception(f"{cls.__name__}.filter() expects keyword arguments for columns: {columns} or conditions")
        sel = table.select() if not count_rows else select([func.count()]).select_from(table)

        sel, values = cls.where(sel, column_filters, *conditions)

        sel, values = cls.check_limit_offset(sel, values, limit, offset)
        
        if count_rows:
            row_count = await database.fetch(sel, cls.__name__)
            return row_count[0][0] if row_count else 0

        if not order_by is None:
            sel = sel.order_by(order_by)

        results = await database.fetch(sel, cls.__name__, tuple(values))

        normalized_results = cls.normalize(results)

        rows = []
        for result in cls.normalize(results):
            values = {}
            for sel, value in zip(columns, result):
                serialized = cls.__metadata__.tables[cls.__name__]['column_map'][sel][2]

                if sel in cls.__metadata__.tables[cls.__name__]['foreign_keys']:
                    foreign_type = cls.__metadata__.tables[cls.__name__]['column_map'][sel][1]
                    foreign_primary_key = foreign_type.__metadata__.tables[foreign_type.__name__]['primary_key']
                    result[value] = loads(result[value]) if serialized else [result[value]]

                    foreign_values = []
                    for foreign_pkey in result[value]:
                        foreign_result = await foreign_type.select(
                            '*', where={foreign_primary_key: foreign_pkey}
                        )
                        foreign_values.extend(foreign_result)
                    
                    if serialized:
                        values[sel] = foreign_values
                        continue

                    values[sel] =  foreign_values[0] if foreign_values else None
                    continue 
                
                
                if serialized:
                    try:
                        values[sel] = loads(result[value])
                    except AttributeError as e:
                        resolve_missing_attribute(
                            str(repr(e))
                        )
                        values[sel] = loads(result[value])
                    continue
                values[sel] = result[value]
            try:
                rows.append(
                    cls(**values)
                )
            except Exception as e:
                pass
        return rows

    async def update(self,
        where: dict = None,
        **to_update
    ):
        self.__class__.get_table()

        table_name = self.__class__.__name__
        primary_key = self.__metadata__.tables[table_name]['primary_key']

        if not to_update:
            to_update = self.dict()
            del to_update[primary_key]

        where_ = dict(*where or {})
        if not where_:
            where_ = {primary_key: getattr(self, primary_key)}

        table = self.__metadata__.tables[table_name]['table']
        for column in to_update.copy():
            if column in self.__metadata__.tables[table_name]['foreign_keys']:
                continue
            if column not in table.c:
                raise Exception(f"{column} is not a valid column in {table}")

        query, _ = self.where(table.update(), where_)
        
        to_update = await self.serialize(to_update, insert=True)

        query = query.values(**to_update)

        await self.__metadata__.database.execute(query, to_update)

            
    async def delete(self):
        table_name = self.__class__.__name__
        table = self.__metadata__.tables[table_name]['table']
        primary_key = self.__metadata__.tables[table_name]['primary_key']

        query, _ = self.where(table.delete(table), {primary_key: getattr(self, primary_key)})

        return await self.__metadata__.database.execute(query, None)
    
    async def insert(self):
        table = self.__class__.get_table()
        
        values = await self.serialize(self.dict(), insert=True)
        query = table.insert()

        return await self.__metadata__.database.execute(
            query, values
        )

    @classmethod
    async def get(cls, *p_key_condition, **p_key):
        if not p_key_condition:
            for k in p_key:
                primary_key = cls.__metadata__.tables[cls.__name__]['primary_key']
                if k != cls.__metadata__.tables[cls.__name__]['primary_key']:
                    raise f"Expected primary key {primary_key}=<value>"
                p_key_condition = [getattr(cls, primary_key)  == p_key[k]]
            
        result = await cls.filter(*p_key_condition)
        return result[0] if result else None

    @classmethod
    async def create(cls, **column_args):
        new_obj = cls(**column_args)
        await new_obj.insert()
        return new_obj


class TableMeta(DataBaseModel):
    table_name: str = PrimaryKey()
    model: dict
    columns: list

class DatabaseInit(DataBaseModel):
    database_url: str = PrimaryKey()
    status: Optional[str]
    reservation: Optional[str]
