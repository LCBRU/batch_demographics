from sqlalchemy import MetaData, Table, Column, NVARCHAR

meta = MetaData()


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    batch = Table("batch", meta, autoload=True)

    filename = Column("filename", NVARCHAR(500))
    filename.create(batch)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    batch = Table("batch", meta, autoload=True)

    batch.c.filename.drop()