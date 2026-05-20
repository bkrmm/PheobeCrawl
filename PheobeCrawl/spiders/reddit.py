import scrapy


class RedditSpider(scrapy.Spider):
    name = "reddit"
    allowed_domains = ["old.reddit.com"]
    start_urls = [
        "https://old.reddit.com/r/MachineLearning/top/?t=week",
        "https://old.reddit.com/r/ArtificialInteligence/top/?t=week",
    ]
    custom_settings = {
        "DOWNLOAD_DELAY" : 3,
        "RANDOMIZE_DOWNLOAD_DELAY" : True,
        "CONCURRENT_REQUESTS" : 4,
        "ROBOTSTXT_OBEY" : False,
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "RETRY_HTTP_CODES" : [403],
        "RETRY_TIMES" : 1,
    }


    def parse(self, response):
        for post in response.css("div.thing"):
            post_url = post.css("a.title::attr(href)").get()
            post_title = post.css("a.title::text").get()

            yield {
                "type" : "post",
                "title" : post_title,
                "url" : post_url,
                "score" : post.css("div.score.unvoted::text").get(),
                "comments" : post.css("a.comments::text").get(),
                "subreddit" : response.url.split("/")[4],
            }

            comments_url = post.css("a.comments::attr(href)").get()
            if comments_url:
                # Use the same headers as the main request
                yield response.follow(
                    comments_url,
                    callback=self.parse_post,
                    headers={
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Language": "en-US,en;q=0.5",
                    },
                    meta={"title": post_title},
                )


        #pagination
        next_page = response.css('span.nextprev a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_post(self, response):
        for comment in response.css("div.comment"):
            # Combine all paragraph texts into a single string
            text_parts = comment.css("div.md p::text").getall()
            comment_text = " ".join(text_parts).strip()
            if comment_text:   # skip empty comments
                yield {
                    "post_title": response.meta["title"],
                    "comment_text": comment_text,
                }
