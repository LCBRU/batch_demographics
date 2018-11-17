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
        output_name = Mapping.get_mapping(c.name)

        print(c.name, output_name)

        if not output_name:
            continue

        if output_name in (m.output_name for m in batch.mappings):
            continue

        m = Mapping(output_name=output_name, column=c, batch=batch, automapped=True)
        db.session.add(m)

    db.session.commit()
