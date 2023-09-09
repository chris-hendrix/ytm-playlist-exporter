In the function `LibraryMixin.get_library_playlists` in file `library.py`, make the following change:

```
# results = find_object_by_key(nav(response, SINGLE_COLUMN_TAB + SECTION_LIST),
#                              'itemSectionRenderer')
# results = nav(results, ITEM_SECTION + GRID)
results = nav(response, SINGLE_COLUMN_TAB + SECTION_LIST)
results = nav(results, [0] + GRID)
playlists = parse_content_list(results['items'][1:], parse_playlist)
```



