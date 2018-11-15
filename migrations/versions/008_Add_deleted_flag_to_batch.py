from sqlalchemy import MetaData, Table, Column, Boolean

meta = MetaData()


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    batch = Table("batch", meta, autoload=True)

    deleted = Column("deleted", Boolean())
    deleted.create(batch)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    batch = Table("batch", meta, autoload=True)

    batch.c.deleted.drop()