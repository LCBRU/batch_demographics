from sqlalchemy import MetaData, Index, ForeignKey, Table, Column, Integer

meta = MetaData()


def upgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)

    user = Table("user", meta, autoload=True)

    batch = Table("batch", meta, autoload=True)

    user_id = Column("user_id", Integer, ForeignKey("user.id"), nullable=False)
    user_id.create(batch)

    idx_batch_user_id = Index("idx_batch_user_id", batch.c.user_id)
    idx_batch_user_id.create(migrate_engine)


def downgrade(migrate_engine):
    meta = MetaData(bind=migrate_engine)
    batch = Table("batch", meta, autoload=True)

    idx_batch_user_id = Index("idx_batch_user_id", batch.c.user_id)
    idx_batch_user_id.drop(migrate_engine)

    batch.c.user_id.drop()