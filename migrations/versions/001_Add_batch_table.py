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

    batch = Table(
        "batch",
        meta,
        Column("id", Integer, primary_key=True),
        Column("created_date", DateTime()),
        Column("name", NVARCHAR(500), unique=True),
    )

    batch.create()

def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    batch = Table("batch", meta, autoload=True)
    batch.drop()
