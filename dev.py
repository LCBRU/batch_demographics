#!/usr/bin/env python
from batch_demographics import create_app
from config import DevConfig

app = create_app(DevConfig())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)