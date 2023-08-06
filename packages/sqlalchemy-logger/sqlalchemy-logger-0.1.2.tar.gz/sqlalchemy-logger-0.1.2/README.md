# sqlalchemy-logger

A small library that provides sqlalchemy session logging.

### Installation

`pip install sqlalchemy-logger`

### Get started

How to log sqlalchemy session:

```
from sqlalchemy-logger import Logger

#create Logger instance (where app is your app = Flask(__name__))
logger = Logger(app)

#call the logger before flush
logger.listen_before_flush()

#call the logger after flush
logger.listen_after_flush()

#call the logger after rollback
logger.listen_after_rollback()
```
