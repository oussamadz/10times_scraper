# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.pipelines.images import ImagesPipeline
import hashlib


class _10TimesPipeline:
    def process_item(self, item, spider):
        return item


class MyImagePipeline(ImagesPipeline):

    def file_path(self, request, response=None, info=None, *, item=None):
        """
            this is the main method used to save images in 'images' dir
            and give it a proper name, which is the venue url slug and
            5 digits of image url hash for venues with multiple images.
        """
        numbering = hashlib.shake_256(request.url.encode()).hexdigest(5)
        return item['venue'].split("/")[-1] + "_" + numbering + ".jpg"
