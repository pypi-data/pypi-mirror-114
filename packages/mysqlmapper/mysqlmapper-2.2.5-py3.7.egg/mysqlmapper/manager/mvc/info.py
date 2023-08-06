from typing import Dict

from tabledbmapper.engine import TemplateEngine
from tabledbmapper.manager.manager import Manager
from tabledbmapper.manager.xml_config import parse_config_from_string

# noinspection SpellCheckingInspection
_table_xml = """
<xml>
    <mapper column="TABLE_NAME" parameter="Name"/>
    <mapper column="ENGINE" parameter="Engine"/>
    <mapper column="TABLE_COLLATION" parameter="Collation"/>
    <mapper column="TABLE_COMMENT" parameter="Comment"/>
    <mapper column="IFNULL(AUTO_INCREMENT, -1)" parameter="AutoIncrement"/>
    <sql>
        <key>GetList</key>
        <value>
            SELECT
                TABLE_NAME, ENGINE, TABLE_COLLATION, TABLE_COMMENT, IFNULL(AUTO_INCREMENT, -1)
            FROM
                information_schema.TABLES
            WHERE
                TABLE_SCHEMA = #{ data_base_name } AND TABLE_TYPE = 'BASE TABLE'
        </value>
    </sql>
    <sql>
        <key>GetRecord</key>
        <value>
            SELECT
                TABLE_NAME, ENGINE, TABLE_COLLATION, TABLE_COMMENT, IFNULL(AUTO_INCREMENT, -1)
            FROM
                information_schema.TABLES
            WHERE
                TABLE_SCHEMA = #{ data_base_name } AND TABLE_TYPE = 'BASE TABLE'
                AND TABLE_NAME = #{ table_name }
        </value>
    </sql>
</xml>
"""

# noinspection SpellCheckingInspection
_column_xml = """
<xml>
    <mapper column="ORDINAL_POSITION" parameter="Number"/>
    <mapper column="COLUMN_NAME" parameter="Name"/>
    <mapper column="COLUMN_TYPE" parameter="Type"/>
    <mapper column="IS_NULLABLE" parameter="NullAble"/>
    <mapper column="COLUMN_DEFAULT" parameter="Defaule"/>
    <mapper column="COLUMN_COMMENT" parameter="Comment"/>
    <sql>
        <key>GetList</key>
        <value>
            SELECT
                ORDINAL_POSITION,
                COLUMN_NAME,
                COLUMN_TYPE,
                IS_NULLABLE,
                IFNULL(COLUMN_DEFAULT, ''),
                COLUMN_COMMENT
            FROM
                information_schema.COLUMNS
            WHERE
                TABLE_SCHEMA = #{ data_base_name } AND TABLE_NAME = #{ table_name }
        </value>
    </sql>
</xml>
"""

_index_xml = """
<xml>
    <mapper column="INDEX_NAME" parameter="Name"/>
    <mapper column="COLUMN_NAME" parameter="ColumnName"/>
    <mapper column="NON_UNIQUE" parameter="Unique"/>
    <mapper column="INDEX_TYPE" parameter="Type"/>
    <sql>
        <key>GetList</key>
        <value>
            SELECT
                INDEX_NAME,
                COLUMN_NAME,
                NON_UNIQUE,
                INDEX_TYPE
            FROM
                information_schema.STATISTICS
            WHERE
                TABLE_SCHEMA = #{ data_base_name } AND TABLE_NAME = #{ table_name }
        </value>
    </sql>
</xml>
"""

_key_xml = """
<xml>
    <mapper column="COLUMN_NAME" parameter="ColumnName"/>
    <mapper column="REFERENCED_TABLE_NAME" parameter="RelyTable"/>
    <mapper column="REFERENCED_COLUMN_NAME" parameter="RelyColumnName"/>
    <sql>
        <key>GetList</key>
        <value>
            SELECT
                COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME
            FROM
                information_schema.KEY_COLUMN_USAGE
            WHERE
                CONSTRAINT_NAME != 'PRIMARY' AND
                TABLE_SCHEMA = REFERENCED_TABLE_SCHEMA AND
                TABLE_SCHEMA = #{ data_base_name } AND TABLE_NAME = #{ table_name }
        </value>
    </sql>
</xml>
"""

DataBaseInfo = Dict


class DBInfo:
    """
    A tool class for obtaining database information by querying mysql.
    information_ Schema table. Get database table structure information
    """

    def __init__(self, template_engine: TemplateEngine, database_name: str):
        # Read profile
        table_config = parse_config_from_string(_table_xml)
        column_config = parse_config_from_string(_column_xml)
        index_config = parse_config_from_string(_index_xml)
        key_config = parse_config_from_string(_key_xml)

        # builder manager
        self.table_manager = Manager(template_engine, table_config)
        self.column_manager = Manager(template_engine, column_config)
        self.index_manager = Manager(template_engine, index_config)
        self.key_manager = Manager(template_engine, key_config)

        # cache database name
        self.database_name = database_name

    def get_db_info(self) -> DataBaseInfo:
        """
        Get database information
        :return: database information
        """
        table_map = {}
        # Query table structure information
        tables = self.table_manager.query("GetList", {"data_base_name": self.database_name})
        for table in tables:
            table["columns"] = self.column_manager.query(
                "GetList",
                {"data_base_name": self.database_name, "table_name": table["Name"]}
            )
            table["indexs"] = self.index_manager.query(
                "GetList",
                {"data_base_name": self.database_name, "table_name": table["Name"]}
            )
            table["keys"] = self.key_manager.query(
                "GetList",
                {"data_base_name": self.database_name, "table_name": table["Name"]}
            )
            table_map[table["Name"]] = table
        return table_map

    def get_table_info(self, table_name: str) -> DataBaseInfo:
        """
        Get table information
        :return: table information
        """
        # Query table structure information
        tables = self.table_manager.query("GetRecord", {
            "data_base_name": self.database_name,
            "table_name": table_name
        })
        # The indication is specified here, so only one record will be returned
        table = tables[0]
        table["columns"] = self.column_manager.query(
            "GetList",
            {"data_base_name": self.database_name, "table_name": table["Name"]}
        )
        table["indexs"] = self.index_manager.query(
            "GetList",
            {"data_base_name": self.database_name, "table_name": table["Name"]}
        )
        table["keys"] = self.key_manager.query(
            "GetList",
            {"data_base_name": self.database_name, "table_name": table["Name"]}
        )
        return table
