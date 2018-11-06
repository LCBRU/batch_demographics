from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    Date,
    DateTime,
    ForeignKey,
)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    Table("batch", meta, autoload=True)

    request_details = Table(
        "request_details",
        meta,
        Column("id", Integer, primary_key=True),
        Column("created_date", DateTime()),
        Column("forename", NVARCHAR(100)),
        Column("surname", NVARCHAR(100)),
        Column("dob", Date()),
        Column("sex", NVARCHAR(10)),
        Column("postcode", NVARCHAR(10)),
        Column("nhs_number", NVARCHAR(10)),
        Column("system_number", NVARCHAR(10)),
        Column("address1", NVARCHAR(100)),
        Column("address2", NVARCHAR(100)),
        Column("address3", NVARCHAR(100)),
        Column("address4", NVARCHAR(100)),
        Column("address5", NVARCHAR(100)),
        Column("local_id", NVARCHAR(100)),
        Column("batch_id", Integer, ForeignKey("batch.id"), index=True, nullable=False),
    )

    request_details.create()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    request_details = Table("request_details", meta, autoload=True)
    request_details.drop()
