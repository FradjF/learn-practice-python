import logging

def configure_logging():
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s | %(levelname)s | Module: %(name)s | "
                 "Function: %(funcName)s | Line: %(lineno)s | %(message)s",
        filename="expense_tracker.log",
        encoding = "utf-8"
    )

