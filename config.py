
# Flask configuration searches this module for UPPERCASE objects...
SQLALCHEMY_DATABASE_URI = "sqlite:///hello.db"
SECRET_KEY = "\xd8\x1e\x88\xf4\xb7\xa9@\xb8p\n2v\x1d\xb5\xb9IfA\xf6\x14\x80\x89\xf4F"

logging_config_dict = {
  "version": 1,
  "formatters": {"simple": {"format": "%(asctime)s - %(levelname)s - %(name)s - %(message)s"}},
  "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "simple"}},
  "root": {"level": "DEBUG", "propagate": True, "handlers": ["console"]},
  "disable_existing_loggers": False,
}

