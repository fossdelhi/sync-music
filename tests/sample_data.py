"""
This file contains dictionaries of data in the format required by the
functions in findmeta. Attachmeta uses only get_tracks function from
findmeta, hence no separate file is needed.
"""

of_get_tracks = {
    "tracks": {
        "items": [
            {
                "album": {
                    "album_type": "single",
                    "artists": [
                        {
                            "name": "Wiz Khalifa",
                            "type": "artist",
                        },
                        {
                            "name": "Charlie Puth",
                            "type": "artist",
                        }
                    ],
                    "id": "5FXIqS1XqbpfOKNoi5VUwS",
                    "images": [
                        {
                            "height": 640,
                            "url": "https://i.scdn.co/image/08aac7ff0c2a42fa6c674dadb8c74762c667b725",
                            "width": 640
                        },
                        {
                            "height": 300,
                            "url": "https://i.scdn.co/image/2d404c487a713d2ac32ad809c496656a47c8de7c",
                            "width": 300
                        },
                        {
                            "height": 64,
                            "url": "https://i.scdn.co/image/43209904884ed685f8c01a553c9a0faa85ea0b8e",
                            "width": 64
                        }
                    ],
                    "name": "See You Again (feat. Charlie Puth)",
                    "release_date": "2015",
                    "release_date_precision": "year",
                    "type": "album",
                    "uri": "spotify:album:5FXIqS1XqbpfOKNoi5VUwS"
                },
                "artists": [
                    {
                        "name": "Wiz Khalifa",
                        "type": "artist",
                    },
                    {
                        "name": "Charlie Puth",
                        "type": "artist",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 229525,
                "id": "2JzZzZUQj3Qff7wapcbKjc",
                "name": "See You Again (feat. Charlie Puth)",
                "popularity": 80,
                "track_number": 1,
                "type": "track",
            }
        ]
    }
}

of_get_categories = {
    "categories": {
        "items": [
            {
                "id": "toplists",
                "name": "Top Lists"
            }
        ]
    }
}

of_get_playlists = {
    "playlists": {
        "items": [
            {
                "id": "37i9dQZF1DXcBWIGoYBM5M",
                "images": [
                    {
                        "height": 300,
                        "url": "https://i.scdn.co/image/1e5031f08a4662e47f40659c1388e847d37d60ec",
                        "width": 300
                    }
                ],
                "name": "Today's Top Hits",
                "owner": {
                    "display_name": "Spotify",
                    "id": "spotify",
                    "type": "user",
                },
                "tracks": {
                    "href": "https://api.spotify.com/v1/users/spotify/playlists/37i9dQZF1DXcBWIGoYBM5M/tracks",
                    "total": 50
                },
                "type": "playlist",
            }
        ]
    }
}

of_get_playlist_tracks = {
    "items": [
        {
            "track": {
                "album": {
                    "album_type": "single",
                    "artists": [
                        {
                            "name": "Dennis Lloyd",
                            "type": "artist",
                        }
                    ],
                    "id": "6c5gDwB7Xo58thk2vap4Ch",
                    "name": "Nevermind",
                    "release_date": "2017-06-30",
                    "release_date_precision": "day",
                    "type": "album",
                },
                "artists": [
                    {
                        "name": "Dennis Lloyd",
                        "type": "artist",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 156600,
                "id": "63SevszngYpZOwf63o61K4",
                "name": "Nevermind",
                "popularity": 92,
                "track_number": 1,
                "type": "track",
            },
        },
        {
            "track": {
                "album": {
                    "album_type": "album",
                    "artists": [
                        {
                            "name": "Cardi B",
                            "type": "artist",
                        }
                    ],
                    "name": "Invasion of Privacy",
                    "release_date": "2018-04-06",
                    "release_date_precision": "day",
                    "type": "album",
                },
                "artists": [
                    {
                        "name": "Cardi B",
                        "type": "artist",
                    },
                    {
                        "name": "Bad Bunny",
                        "type": "artist",
                    },
                    {
                        "name": "J Balvin",
                        "type": "artist",
                    }
                ],
                "disc_number": 1,
                "duration_ms": 253390,
                "id": "58q2HKrzhC3ozto2nDdN4z",
                "name": "I Like It",
                "popularity": 87,
                "track_number": 7,
                "type": "track",
            }
        }
    ]
}

of_get_track_info = {
    "album": {
        "album_type": "single",
        "artists": [
            {
                "name": "Wiz Khalifa",
                "type": "artist",
            },
            {
                "name": "Charlie Puth",
                "type": "artist",
            }
        ],
        "images": [
            {
                "height": 640,
                "url": "https://i.scdn.co/image/08aac7ff0c2a42fa6c674dadb8c74762c667b725",
                "width": 640
            },
            {
                "height": 300,
                "url": "https://i.scdn.co/image/2d404c487a713d2ac32ad809c496656a47c8de7c",
                "width": 300
            },
            {
                "height": 64,
                "url": "https://i.scdn.co/image/43209904884ed685f8c01a553c9a0faa85ea0b8e",
                "width": 64
            }
        ],
        "name": "See You Again (feat. Charlie Puth)",
        "release_date": "2015",
        "release_date_precision": "year",
        "type": "album",
    },
    "artists": [
        {
            "name": "Wiz Khalifa",
            "type": "artist",
        },
        {
            "name": "Charlie Puth",
            "type": "artist",
        }
    ],
    "disc_number": 1,
    "duration_ms": 229525,
    "id": "2JzZzZUQj3Qff7wapcbKjc",
    "name": "See You Again (feat. Charlie Puth)",
    "popularity": 80,
    "track_number": 1,
    "type": "track",
}
