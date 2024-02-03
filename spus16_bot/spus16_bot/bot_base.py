import logging
from models.sqlalchemy import ENGINE, Base

# SEE https://docs.python.org/ja/3/library/logging.html
logging.basicConfig(format='%(asctime)-15s %(levelname)s %(module)s:%(lineno)d %(message)s')

Base.metadata.create_all(ENGINE)
