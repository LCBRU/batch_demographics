from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    role = Table(
        "role",
        meta,
        Column("id", Integer, primary_key=True),
        Column("name", NVARCHAR(80), unique=True),
        Column("description", NVARCHAR(255)),
        Column("created_date", DateTime()),
    )

    role.create()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    batch = Table("batch", meta, autoload=True)
    batch.drop()
