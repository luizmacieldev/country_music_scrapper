import re
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, MapCompose
from urllib.parse import urljoin
from country.items import ArtistItem

pics_url_base = "https://lastfm.freetls.fastly.net/i/u/770x0/"

class ArtistsSpider(scrapy.Spider):
    name = 'artists'
    start_urls = ['https://www.last.fm/tag/country/artists']

    def parse(self, response):
        artists_info = response.css('div.big-artist-list-item.js-link-block.link-block')
        for artist in artists_info:
            artist_href = artist.css('h3.big-artist-list-title a::attr(href)').get()
            artist_url = response.urljoin(artist_href)
            artist_name = artist.css('h3.big-artist-list-title a::text').get()
            
            yield scrapy.Request(
                url=artist_url,
                callback=self.parse_artist,
                meta={
                    'name': artist_name,
                    'listeners': artist.css('p.big-artist-list-listeners::text').re_first(r'[\d,]+').replace(',', ''),
                    'avatar_url': artist.css('span.big-artist-list-avatar-mobile img::attr(src)').get(),
                    'mini_bio': artist.css('div.big-artist-list-bio p::text').get(),
                    'artist_url': artist_url
                }
            )

        next_page = response.css('li.pagination-next a::attr(href)').get()
        if next_page:
            next_page_url = urljoin(response.url, next_page)
            yield response.follow(next_page_url, callback=self.parse)

    def parse_artist(self, response):
        loader = ItemLoader(item=ArtistItem(), response=response)

        loader.add_value('name', response.meta['name'])
        loader.add_value('listeners', response.meta['listeners'])
        loader.add_value('avatar_url', response.meta['avatar_url'])
        loader.add_value('mini_bio', response.meta['mini_bio'])
        loader.add_value('artist_url', response.meta['artist_url'])
        loader.add_value('principal_tags', response.css('ul.tags-list li.tag a::text').getall())

        # songs
        song_names = response.css('tbody tr td.chartlist-name a::text').getall()
        song_urls = response.css('tbody tr td.chartlist-name a::attr(href)').getall()
        song_listeners_raw = response.css('span.chartlist-count-bar-value::text').getall()
        song_listeners = [re.search(r'([\d,]+)', listener).group(1) for listener in song_listeners_raw if re.search(r'([\d,]+)', listener)]
        
        music_dict = [
            {
                'song': song,
                'url': response.urljoin(url),
                'listeners': int(listeners.replace(',', '')),
            }
            for song, url, listeners in zip(song_names, song_urls, song_listeners)
        ]
        loader.add_value('ten_most_played_songs', music_dict)

        # albums
        album_names = response.css('h3.artist-top-albums-item-name a::text').getall()
        album_links = response.css('h3.artist-top-albums-item-name a::attr(href)').getall()
        album_photos = response.css('span.artist-top-albums-item-image.cover-art img::attr(src)').getall()
        album_listeners = response.css('p.artist-top-albums-item-aux-text.artist-top-albums-item-listeners::text').getall()
        album_years = response.css('p.artist-top-albums-item-aux-text:not(.artist-top-albums-item-listeners)::text').getall()
        album_num_tracks = response.css('p.artist-top-albums-item-aux-text:not(.artist-top-albums-item-listeners)::text').getall()
        social_media_links = response.css('ul.resource-external-links li a::attr(href)').getall()

        album_links = [response.urljoin(url) for url in album_links]
        albumn_listeners = [re.search(r'[\d,]+', album).group(0).replace(',', '') for album in album_listeners]
        album_photos = [photo for photo in album_photos if album_photos]

        albums = [
            {
                'name': name,
                'link': link,
                'listeners': listeners,
                'year': year.split('·')[0].strip(),
                'num_tracks': num_tracks.strip().split('\n')[1].lstrip() if len(num_tracks.strip().split('\n')) > 1 else 'N/A',
                'photo': photo
            }
            for name, link, listeners, year, num_tracks, photo in zip(album_names, album_links, albumn_listeners, album_years, album_num_tracks, album_photos)
        ]
        loader.add_value('most_popular_albums', albums)


        photos_list = [
            response.urljoin(f"{pics_url_base}{item.split('/')[-1]}")
            for item in response.css('li.sidebar-image-list-item a::attr(href)').getall()
        ]
        loader.add_value('photos', photos_list)
        loader.add_value('social_media_links', social_media_links)

        wiki_url = response.url + '/+wiki'
        yield scrapy.Request(
            url=wiki_url,
            callback=self.parse_artist_bio,
            meta={'artist_item': loader.load_item()}
        )

    def parse_artist_bio(self, response):
        bio = response.css('div.wiki-content *::text').getall()
        bio_text = ' '.join(filter(None, (text.strip() for text in bio))).strip()

        artist_item = response.meta['artist_item']
        artist_item['biography'] = bio_text

        yield artist_item
