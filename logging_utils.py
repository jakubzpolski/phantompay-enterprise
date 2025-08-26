import logging

logger = logging.getLogger("phantompay")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s"))
logger.addHandler(handler)

def log_event(event, data=None):
    logger.info(f"EVENT: {event} | DATA: {data}")
