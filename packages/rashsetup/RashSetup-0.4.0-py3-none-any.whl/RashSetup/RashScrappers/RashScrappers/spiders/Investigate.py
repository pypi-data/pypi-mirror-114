import scrapy


class Investigator(scrapy.Spider):
    name = 'Settings'
    allowed_domains = [
        'github.com'
    ]

    def __init__(
            self,
            pipe,
            url

    ):
        super().__init__()

        self.start_urls = url
        self.pipe = pipe
        self.valid = False

        self.pipe["result"] = {}
        self.pipe["failed"] = False

        self.is_py = False

    def start_requests(self):
        yield scrapy.Request(
            self.start_urls, errback=self.pipe_error
        )

    def pipe_error(self, reason):
        self.pipe["result"] = ""
        self.pipe["failed"] = True
        self.pipe["exception"] = str(reason)

    def parse(self, response, *args):
        entities = response.xpath("//div[@class='Box-row Box-row--focus-gray py-2 d-flex position-relative "
                                  "js-navigation-item ']")

        candi = (
            "__init__.py", "README.md", "settings.json"
        )

        for entity in entities:
            name = entity.xpath(".//span/a/text()").get()
            token = candi.index(name) if name in candi else 3

            if token == 0:
                self.is_py = True
                yield {
                    "status": "Found __init__.py hence, Valid Python Module"
                }

            elif token == 1:
                self.pipe["result"]["readme"] = response.xpath("//div[@id='readme']").extract()

                yield {
                    "status": "Extracted raw README.md from %s".format(response.request.url)
                }

            elif token == 2:

                yield scrapy.Request(
                    response.urljoin(
                        entity.xpath(".//span/a/@href").get()
                    ), callback=self.yield_raw, errback=self.pipe_error, meta={"name": name}
                )

    def yield_raw(self, response):
        raw = response.urljoin(response.xpath("//div[@class='BtnGroup']/a/@href").get())

        self.pipe["result"][response.request.meta["name"]] = raw

        yield {
            "name": response.request.meta["name"],
            "raw_link": raw
        }

    def close(self, spider, reason):
        self.pipe["failed"] = self.pipe["failed"] and self.is_py
        self.pipe["result"] = "" if self.pipe["failed"] else self.pipe["result"]
        self.pipe["exception"] = self.pipe["exception"] if self.pipe["failed"] else ""

        return super().close(spider, reason)
