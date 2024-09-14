# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ArtistItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    listeners = scrapy.Field()
    avatar_url = scrapy.Field()
    mini_bio = scrapy.Field()
    artist_url = scrapy.Field()
    principal_tags = scrapy.Field()
    ten_most_played_songs = scrapy.Field()
    photos = scrapy.Field()
    most_popular_albums = scrapy.Field()
    social_media_links = scrapy.Field()
    biography = scrapy.Field()
    
