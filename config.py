import os


class DevConfig(object):
    """Standard configuration options"""
    DEBUG = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_FILE = os.path.join(BASE_DIR, 'database.sqlite3')
    print("Database at " + DB_FILE)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + DB_FILE
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    WTF_CSRF_ENABLED = True
    SECRET_KEY = "secret"
    SECURITY_PASSWORD_SALT = "sale"
    SQLALCHEMY_ECHO = False
    SECURITY_TRACKABLE = "True"
    SMTP_SERVER = "localhost"
    ADMIN_EMAIL_ADDRESSES = "rab63@le.ac.uk"
    ERROR_EMAIL_SUBJECT = "Batch Demographics Error"
    MAIL_DEFAULT_SENDER = "lcbruit@leicester.ac.uk"
    SECURITY_EMAIL_SENDER = "lcbruit@leicester.ac.uk"
    SECURITY_CHANGEABLE = True
    SECURITY_RECOVERABLE = True
    SECURITY_SEND_PASSWORD_RESET_EMAIL = False


class TestConfig(DevConfig):
    """Configuration for general testing"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    WTF_CSRF_ENABLED = False
    ADMIN_EMAIL_ADDRESSES = "rab63@le.ac.uk;richard.a.bramley@uhl-tr.nhs.uk"
    SMTP_SERVER = None
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False


class TestConfigCRSF(TestConfig):
    WTF_CSRF_ENABLED = True
