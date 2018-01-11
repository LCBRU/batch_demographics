# -*- coding: utf-8 -*-

import json
import pytest
from batch_demographics.model import Batch
from batch_demographics.database import db


@pytest.mark.parametrize("batches", [
    (0),
    (1),
    (10),
])
def test_batch_list_empty(client, batches):

    for _ in range(batches):
        db.session.add(Batch())
        db.session.commit()

    resp = client.get('/api/batch/')

    assert resp is not None
    data = json.loads(resp.data.decode('utf8'))
    assert len(data) == batches
