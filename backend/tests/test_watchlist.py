def test_watchlist_local_storage_simulation():
    watchlist = []
    movie_id = "1"

    # Add
    if movie_id not in watchlist:
        watchlist.append(movie_id)
    assert movie_id in watchlist

    # Remove
    watchlist.remove(movie_id)
    assert movie_id not in watchlist
