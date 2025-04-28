import logging
from datetime import datetime
from flask import g
from app.models import db, Logs

def setup_logger(app):  
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    class SQLAlchemyHandler(logging.Handler):
        def emit(self, record):
            try:
                with app.app_context(): 
                    log = Logs(
                        username=getattr(g, 'user', 'system'),
                        action=record.getMessage().split(" - ")[0][:100],
                        date=datetime.utcnow(),
                        status=record.levelname,
                        extra_info=record.getMessage()[:255]
                    )
                    db.session.add(log)
                    db.session.commit()
            except Exception as e:
                try:
                    with app.app_context():
                        db.session.rollback()
                except:
                    pass
                print("Failed to write log to DB:", e)

    db_handler = SQLAlchemyHandler()
    db_handler.setLevel(logging.INFO)
    db_handler.setFormatter(formatter)
    logger.addHandler(db_handler)
