from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
)


meta = MetaData()

batch = Table(
    "batch",
    meta,
    Column("id", Integer, primary_key=True),
    Column("created_date", DateTime()),
    Column("name", NVARCHAR(500), unique=True),
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    batch.create()

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    batch.drop()
