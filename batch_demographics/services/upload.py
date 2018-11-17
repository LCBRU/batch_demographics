import csv
from batch_demographics.files import batch_file_path
from batch_demographics.model import Column, Mapping
from batch_demographics.database import db

def extract_batch_column_headers(batch):
    
    with open(batch_file_path(batch)) as csvfile:
        dialect = csv.Sniffer().sniff(csvfile.read(10240))
        csvfile.seek(0)
        reader = csv.DictReader(csvfile, dialect=dialect)
        headers = reader.fieldnames

        for i, h in enumerate(headers):
            c = Column(column_index=i, name=h, batch_id=batch.id)
            db.session.add(c)

    db.session.commit()


def automap_batch_columns(batch):
    for c in batch.columns:
        mapping = Mapping.get_mapping(c.name)

        if not mapping or mapping in (c.mapping for c in batch.columns):
            c.mapping = ''
        else:
            c.mapping = mapping
