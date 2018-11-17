from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    Table("batch", meta, autoload=True)

    column = Table(
        "column",
        meta,
        Column("id", Integer, primary_key=True),
        Column("column_index", Integer, index=True),
        Column("created_date", DateTime()),
        Column("name", NVARCHAR(100)),
        Column("mapping", NVARCHAR(100)),
        Column("batch_id", Integer, ForeignKey("batch.id"), index=True, nullable=False),
        UniqueConstraint('batch_id', 'column_index'),
    )

    column.create()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    column = Table("column", meta, autoload=True)
    column.drop()
