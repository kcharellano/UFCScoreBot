# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import os

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from sys import stdout

class ScoresPipeline:

    def open_spider(self, spider):
        self.exporter_dict = {}
    
    def close_spider(self, spider):
        for exporter in self.exporter_dict.values():
            exporter.finish_exporting()

    def _exporter_for_item(self, item, spider):
        pipe_logger.debug("Getting first and last names")
        first_name = getattr(spider, "first").strip().lower()
        last_name = getattr(spider, "last").strip().lower()
        adapter = ItemAdapter(item)
        record = adapter['record']
        pipe_logger.debug("Opening file")
        PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        FILE_PATH = os.path.join(PROJECT_DIR, "scrapy_output", '{last}_{first}.json'.format(last=last_name, first=first_name))
        f = open(FILE_PATH, 'wb')
        pipe_logger.debug("Exporting file")
        exporter = JsonItemExporter(f)
        exporter.start_exporting()
        self.exporter_dict['{}'.format(first_name)] = exporter
        return self.exporter_dict['{}'.format(first_name)]

    def process_item(self, item, spider):
        pipe_logger.debug("Processing item")
        exporter = self._exporter_for_item(item, spider)
        exporter.export_item(item)
        pipe_logger.debug("Done processing item")
        return item

logging.basicConfig(
        stream=stdout,
        level=logging.DEBUG,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
        )
pipe_logger = logging.getLogger(__name__)