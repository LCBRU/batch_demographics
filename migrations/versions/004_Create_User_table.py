from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
    Boolean,
    DateTime,
)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    user = Table(
        "user",
        meta,
        Column("id", Integer, primary_key=True),
        Column("email", NVARCHAR(255), nullable=False, unique=True),
        Column("password", NVARCHAR(255), nullable=False),
        Column("first_name", NVARCHAR(255)),
        Column("last_name", NVARCHAR(255)),
        Column("active", Boolean()),
        Column("confirmed_at", DateTime()),
        Column("last_login_at", DateTime()),
        Column("current_login_at", DateTime()),
        Column("last_name", NVARCHAR(255)),
        Column("last_login_ip", NVARCHAR(255)),
        Column("current_login_ip", NVARCHAR(255)),
        Column("login_count", Integer()),
        Column("created_date", DateTime(), nullable=False),
    )

    user.create()


def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    user = Table("user", meta, autoload=True)
    user.drop()
