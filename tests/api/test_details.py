# -*- coding: utf-8 -*-

import pytest
from batch_demographics.model import Batch, Details
from batch_demographics.database import db


@pytest.mark.parametrize("num_of_details", [
    (0),
    (1),
    (10),
])
def test_details_list(client, num_of_details):

    batch = Batch(name='')
    db.session.add(batch)

    for _ in range(num_of_details):
        details = Details()
        details.batch = batch
        db.session.add(details)

# Create details for another batch to check that it differentiates
    other_batch = Batch(name='')
    db.session.add(other_batch)
    other_details = Details()
    other_details.batch = other_batch
    db.session.add(other_details)

    db.session.commit()

    resp = client.get('/api/batch/{}/details/'.format(batch.id))

    assert resp is not None
    assert resp.status_code == 200
    data = resp.get_json()
    assert len(data) == num_of_details
