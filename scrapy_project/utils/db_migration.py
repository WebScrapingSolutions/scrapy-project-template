from playhouse.migrate import *

from scrapy_project.utils.utils import CustomDatabaseProxy


def get_migrator():
    # see https://docs.peewee-orm.com/en/latest/peewee/playhouse.html#schema-migrations for reference
    db_uri = ""
    db_handle = CustomDatabaseProxy(db_uri=db_uri)
    migrator = PostgresqlMigrator(db_handle)
    return migrator


def add_fields_to_db_schema():
    migrator = get_migrator()

    # new example field
    title_field = CharField(default="")
    status_field = IntegerField(null=True)

    # actual migration
    migrate(
        migrator.add_column("some_table", "title", title_field),
        migrator.add_column("some_table", "status", status_field),
        migrator.drop_column("some_table", "old_column"),
    )


if __name__ == "__main__":
    add_fields_to_db_schema()
