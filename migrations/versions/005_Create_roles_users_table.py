from sqlalchemy import (
    MetaData,
    Table,
    Column,
    Integer,
    NVARCHAR,
    DateTime,
    Boolean,
    DateTime,
    ForeignKey,
)


def upgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine

    role = Table("role", meta, autoload=True)
    user = Table("user", meta, autoload=True)

    roles_users = Table(
        "roles_users",
        meta,
        Column(
            "user_id",
            Integer,
            ForeignKey(user.c.id),
            index=True,
            nullable=False,
            primary_key=True
        ),
        Column(
            "role_id",
            Integer,
            ForeignKey(role.c.id),
            index=True,
            nullable=False,
            primary_key=True
        ),
    )

    roles_users.create()



def downgrade(migrate_engine):
    meta = MetaData()
    meta.bind = migrate_engine
    roles_users = Table("roles_users", meta, autoload=True)
    roles_users.drop()
