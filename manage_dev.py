#!/usr/bin/env python
from migrate.versioning.shell import main
from config import DevConfig

if __name__ == '__main__':
    main(debug='False', repository='migrations', url=DevConfig.SQLALCHEMY_DATABASE_URI)
