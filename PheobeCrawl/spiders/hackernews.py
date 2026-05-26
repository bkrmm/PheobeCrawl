import scrapy


class HackernewsSpider(scrapy.Spider):
    name = "hackernews"
    allowed_domains = ["news.ycombinator.com"]
    start_urls = ["https://news.ycombinator.com/"]

    custom_settings = {
        "DOWNLOAD_DELAY" : 3,
        "RANDOMIZE_DOWNLOAD_DELAY" : True,
        "CONCURRENT_REQUESTS" : 4,
        "ROBOTSTXT_OBEY" : False,
        "USER_AGENT" : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "RETRY_HTTP_CODES" : [403],
        "RETRY_TIMES" : 1,
    }

    def parse(self, response):
        # HN has a structure where the post is in tr.athing and metadata is in the following tr
        posts = response.css("tr.athing")
        for post in posts:
            post_url = post.css("td.title a::attr(href)").get()
            # The title is inside a span.titleline
            post_title = post.css("span.titleline a::text").get()

            yield {
                "type" : "post",
                "title" : post_title,
                "url" : post_url,
            }

            # Find the subtext row which contains the "discuss" link
            # Using xpath to find the next sibling tr
            subtext = post.xpath('following-sibling::tr[1]')
            discuss_url = subtext.css("a.sitelnk[href*='item?id=']::attr(href)").get()
            
            if discuss_url:
                # Ensure the URL is absolute
                full_discuss_url = response.urljoin(discuss_url)
                yield response.follow(
                    full_discuss_url,
                    callback=self.parse_post,
                    meta={"title": post_title},
                )

        # Pagination
        next_page = response.css("a.morelink::attr(href)").get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_post(self, response):
        # HN comments are in divs with class 'comment'
        for comment in response.css("td.comment"):
            # The actual text is in a div with class 'commenttext'
            text = comment.css("div.commenttext::text").get()
            if text:
                yield {
                    "post_title": response.meta["title"],
                    "comment_text": text.strip(),
                    "type": "comment"
                }
