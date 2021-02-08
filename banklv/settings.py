BOT_NAME = 'banklv'

SPIDER_MODULES = ['banklv.spiders']
NEWSPIDER_MODULE = 'banklv.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'banklv.pipelines.BanklvPipeline': 100,

}