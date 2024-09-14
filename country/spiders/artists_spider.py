import re, scrapy
from urllib.parse import urljoin
from country.items import ArtistItem

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
        song_names = response.css('tbody tr td.chartlist-name a::text').getall()
        song_urls = response.css('tbody tr td.chartlist-name a::attr(href)').getall()
        album_names = response.css('h3.artist-top-albums-item-name a::text').getall()
        album_links = response.css('h3.artist-top-albums-item-name a::attr(href)').getall()
        albumn_listeners = response.css('p.artist-top-albums-item-aux-text.artist-top-albums-item-listeners::text').getall()
        album_years = response.css('p.artist-top-albums-item-aux-text:not(.artist-top-albums-item-listeners)::text').getall()
        album_num_tracks = response.css('p.artist-top-albums-item-aux-text:not(.artist-top-albums-item-listeners)::text').getall()
        social_media_links = response.css('ul.resource-external-links li a::attr(href)').getall()

        #cleaning data
        music_dict = dict(zip(map(str, song_names), song_urls))

        photos_list = [response.urljoin(item) for item in response.css('li.sidebar-image-list-item a::attr(href)').getall()]
        album_years = [year.strip().replace(' ', '').split('\n')[0].replace('·', '') for year in album_years]
        album_num_tracks = [tracks.strip().split('\n')[1].lstrip() if len(tracks.strip().split('\n')) > 1 else 'N/A' for tracks in album_num_tracks]
        
        album_links = [response.urljoin(url) for url in album_links]
        albumn_listeners = [re.search(r'[\d,]+', album).group(0).replace(',', '') for album in albumn_listeners]
        
        music_dict = [
            {
                'song':song,
                'url':response.urljoin(url)
            }
            for song, url in zip(song_names,song_urls)
        ]

        albums = [
            {
                'name': name,
                'link': link,
                'listeners': listeners,
                'year': year,
                'num_tracks': num_tracks
            }
            for name, link, listeners, year, num_tracks in zip(album_names, album_links, albumn_listeners, album_years, album_num_tracks)
        ]

        artist_item = ArtistItem()
        artist_item['name'] = response.meta['name']
        artist_item['listeners'] = response.meta['listeners']
        artist_item['avatar_url'] = response.meta['avatar_url']
        artist_item['mini_bio'] = response.meta['mini_bio']
        artist_item['artist_url'] = response.meta['artist_url']
        artist_item['principal_tags'] = response.css('ul.tags-list li.tag a::text').getall()
        artist_item['ten_most_played_songs'] = music_dict
        artist_item['photos'] = photos_list
        artist_item['most_popular_albums'] = albums
        artist_item['social_media_links'] = social_media_links



        wiki_url = response.url + '/+wiki'
        yield scrapy.Request(
            url=wiki_url,
            callback=self.parse_artist_bio,
            meta={'artist_item': artist_item}
        )

    def parse_artist_bio(self, response):
        bio = response.css('div.wiki-content p::text').getall()
        bio_text = ' '.join(bio).strip()

        artist_item = response.meta['artist_item']
        artist_item['biography'] = bio_text


        yield artist_item
