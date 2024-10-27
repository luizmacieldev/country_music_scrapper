import scrapy
from scrapy.loader.processors import Identity, TakeFirst, MapCompose
from country.utils.common import clean_text, remove_new_lines

class ArtistItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(
        input_processor=MapCompose(clean_text),  
        output_processor=TakeFirst()              
    )
    listeners = scrapy.Field(
        input_processor=MapCompose(int),       
        output_processor=TakeFirst()
    )
    avatar_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    mini_bio = scrapy.Field(
        input_processor=MapCompose(remove_new_lines, clean_text),
        output_processor=TakeFirst()
    )
    artist_url = scrapy.Field(
        output_processor=TakeFirst()
    )
    principal_tags = scrapy.Field(
        output_processor=Identity()
    )
    ten_most_played_songs = scrapy.Field(
        output_processor=Identity()
    )
    photos = scrapy.Field(
        output_processor=Identity()
    )
    most_popular_albums = scrapy.Field(
        output_processor=Identity()
    )
    social_media_links = scrapy.Field(
        output_processor=Identity()
    )
    biography = scrapy.Field(
        input_processor=MapCompose(remove_new_lines, clean_text),
        output_processor=TakeFirst()
    )
