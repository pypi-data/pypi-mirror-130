"""Init logger for given python package"""
# Standard library imports
import sys
import logging

# Third party imports
from logging_nice_handlers import JupyterStreamHandler

# Local imports
from . import logger

logger.initialize_project_logger(
    name="outlook_mail_loader",
    path_dir_where_to_store_logs="",
    is_stdout_debug=False,
    is_to_propagate_to_root_logger=False,
)


from .class_mail_dumper import MailFolderDumper
from .mail_listener import listen_outlook_mail_folder
from .class_mail_getter import DumpedMails

__all__ = ["MailFolderDumper", "listen_outlook_mail_folder", "DumpedMails"]
