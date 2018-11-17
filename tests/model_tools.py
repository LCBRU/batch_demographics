from batch_demographics.database import db
from batch_demographics.model import Column


def create_batches(user, number, faker):
    result = []

    for _ in range(number):
        b = faker.batch_details()
        b.user = user
        result.append(b)
        db.session.add(b)

    db.session.commit()

    return result


def update_batch(batch):
    db.session.add(batch)
    db.session.commit()


def create_user(faker):
    u = faker.user_details()
    db.session.add(u)
    db.session.commit()

    return u


def create_columns(batch, columns):
    for i, c in enumerate(columns, 1):
        c = Column(column_index=i, name=c, batch_id=batch.id)
        batch.columns.append(c)

    batch.automap_columns()
    db.session.add(batch)
    db.session.commit()
