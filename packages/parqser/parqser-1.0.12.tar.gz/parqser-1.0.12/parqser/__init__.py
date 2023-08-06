"""
parqser

Finally, a good parser
"""
from .page.base_page import BasePage
from .page.loaded_page import LoadedPage
from .web_component.base_component import BaseComponent
from .parser.base_parser import BaseParser
from .parser.html_parser import HTMLParser
from .saver.base_saver import BaseSaver
from .saver.csv_saver import CSVSaver
from .session.base_session import BaseSession
from .session.empty_session import EmptySession
from .scrapper.base_scrapper import BaseScrapper
from .scrapper.batch_parallel_scrapper import BatchParallelScrapper

__version__ = "1.0.12"
__author__ = 'Ilya Shamov'
