from sqlalchemy import MetaData, Table, Column, Boolean

meta = MetaData()


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    mapping = Table("mapping", meta, autoload=True)

    automapped = Column("automapped", Boolean())
    automapped.create(mapping)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    mapping = Table("mapping", meta, autoload=True)

    mapping.c.automapped.drop()