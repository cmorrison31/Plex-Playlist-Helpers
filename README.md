# Plex Playlist Sorter
Plex playlist sorter is a simple Python script that sorts a given plex 
playlist. Sorting is done with lower case strings in the following sequence:

1. artist name
2. album year
3. album title
4. track number
5. track title

The `sort version` is used for the album and track titles. If the album year 
or track index are not defined, they are skipped.

`Various Artist` albums are a special case. The albums are not sorted by 
`Various Artist` as that would meaninglessly group some albums together. The 
tracks in these albums are not sorted by individual track artists either as we 
want tracks in an album to have contiguity. So instead, this python script 
creates a unique `sorting artist` for albums with the artist as 
`Various Artists`. This `sorting artist` is the alphabetically sorted list of 
all unique artists for all tracks in an album.

## License
This project is licensed under the MIT open source license. See the 
LICENSE.txt file for more information.

## Requirements
This project requires python 3.7+.
See the requirements.txt file for a full list of dependencies.

## Installation
Install the requirements via `pip install requirements.txt` 

## How to Use
Create a file called `config.ini` in the source directory with the following 
information:

```text
['DEFAULT']
username = 'your user name'
password = 'your password'
servername = 'server name'
playlist_name = 'playlist name'
```

Replace the fields above with your information then run the script. That's it!
