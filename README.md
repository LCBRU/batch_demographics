# Batch Demographics

Provide a user interface an API for interacting
with the UHL Batch Demographics service.

## Installation and Running

1. Download the code from github

```bash
git clone https://github.com/LCBRU/batch_demographics.git
```

2. Install the requirements

Go to the `batch_demographics` directory and type the command:

```bash
pip install -r requirements.txt
```

3. Create the database using

Staying in the `batch_demographics` directory and type the command:

```bash
flask db upgrade
```

4. Run the application

Staying in the `batch_demographics` directory and type the command:

```bash
python app.py
```

## Development

### Testing

To test the application, run the following command from the project folder:

```bash
pytest
```

### Database Schema Amendments

After amending the models, run the following command to create the
migrations and apply them to the database:

```bash
flask db migrate
flask db upgrade
```
