import os

class Environ:
    log_level = os.environ.get('log_level', 'DEBUG')
    db_trace = True if os.environ.get('db_trace') else False
    force_update = True if os.environ.get('force_update') else False
    database_uri = os.environ.get('database_uri', "sqlite:///spus16_bot.sqlite3")
    consumer_key = os.environ.get('consumer_key')
    consumer_secret = os.environ.get('consumer_secret')
    access_token_key = os.environ.get('access_token_key')
    access_token_secret = os.environ.get('access_token_secret')
    list_id = os.environ.get('list_id')
    match_word = os.environ.get('match_word')
    place_words = os.environ.get('place_words')
    state_words = os.environ.get('state_words')
    test_mode = os.environ.get('test_mode')
    query = os.environ.get('query')
    subscription_key = os.environ.get('subscription_key')
