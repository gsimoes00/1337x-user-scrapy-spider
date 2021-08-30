# 1337x-user-scrapy-spider
A Scrapy Spider that dumps data from selected pages of the torrent list of a given user from the 1337x torrent site.

## Example Usage
```
scrapy crawl user-1337x -a user=my_name -a start_page=1 -a end_page=2 -a rate=5.0 --output my_output.xml
```
