import scrapy
class movie(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        urls = [
            'https://movie.naver.com/movie/running/current.nhn',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 데이터 = response.css("문법")
        moive_sels = response.css('ul."lst_detail_t1>li"')
        for movie_sel in movie_sels:
            title = response.css('.tit > a::text').get()
            print('title', title)