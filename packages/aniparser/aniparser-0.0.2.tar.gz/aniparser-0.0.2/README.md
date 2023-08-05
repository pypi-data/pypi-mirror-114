This is a simple parser that is built to take a file path and return data based on that file path, to determine some common information about animes.

# Usage

The usage of this is pretty simple, there are two main entry points into grabbing data
from files. To parse through an entire directory (recursively) you can do the following
```
for data in aniparser.parse_directories("/home/user/Anime"):
    print(data)
```

To not search recursively, just provide False to the recursive parameter
```
for data in aniparser.parse_directories("/home/user/Anime/Specific Anime Folder", recursive=False):
    print(data)
```

If you want to parse just a single file
```
data = aniparser.parse("/home/user/Anime/Specicific Anime Folder/Specific Anime Episode.mpv")
print(data)
```

# Details
The idea behind the parsing method in this library is to do the least amount of work possible while maintaining reliance. There are many common things that appear in a filename, and this does try to do them in some kind of "sane" order of commonality. It will only do some extra work when it's needed. Additionally, since this should always have the same output for the same input, as well as that output being a small memory footprint in of itself, this does use some aggressive caching that should help speed things up tremendously in long running uses.