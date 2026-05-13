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
        "CONCURRENT_REQUESTS" : 4,
        "ROBOTSTXT_OBEY" : False,
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
                "commments" : post.css("a.comments::text").get(),
                "subreddit" : response.url.split("/")[4],
            }

            comments_url = post.css("a.comments::attr(href)").get()
            if comments_url : 
                yield response.follow(comments_url, callback=self.parse_post, meta={
                    "title" : post_title,
                })

        #pagination
        next_page = response.css('span.nextprev a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)


    def parse_post(self, response):
        for comment in response.css("div.comment"):
            yield {
                "post_title" : response.meta["title"],
                "comment_text" : comment.css("div.md p::text").getall(),
            }
