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
    Table("column", meta, autoload=True)

    mapping = Table(
        "mapping",
        meta,
        Column("id", Integer, primary_key=True),
        Column("created_date", DateTime()),
        Column("output_name", NVARCHAR(100)),
        Column("batch_id", Integer, ForeignKey("batch.id"), index=True, nullable=False),
        Column("column_id", Integer, ForeignKey("column.id"), index=True, nullable=False),
        UniqueConstraint('batch_id', 'column_id'),
        UniqueConstraint('batch_id', 'output_name'),
    )

    mapping.create()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    mapping = Table("mapping", meta, autoload=True)
    mapping.drop()
