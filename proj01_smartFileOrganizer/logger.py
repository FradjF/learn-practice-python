import logging

def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | Module: %(name)s | Function: %(funcName)s | Line: %(lineno)d | %(message)s",
        filename="organizer/organizer.log"
#        force=True
    )