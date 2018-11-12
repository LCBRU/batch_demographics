from sqlalchemy import MetaData, Table, Column, NVARCHAR

meta = MetaData()


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    study = Table("batch", meta, autoload=True)

    filename = Column("filename", NVARCHAR(500))
    filename.create(study)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    study = Table("batch", meta, autoload=True)

    study.c.filename.drop()