import sys, json, ConfigParser
from rauth import OAuth1Service

config = ConfigParser.ConfigParser()

def setup_profile():
    print "Connecting to Twitter..."
    twitter = OAuth1Service(name='twitter',
                            consumer_key='M4npIbKMiY91HV1czc21YlfUL',
                            consumer_secret='48d8OkEbCdvlUXPQ4Y5su6Bta5TS2wHQDtPY7InSDO4PUvHXpO',
                            request_token_url='https://api.twitter.com/oauth/request_token',
                            access_token_url='https://api.twitter.com/oauth/access_token',
                            authorize_url='https://api.twitter.com/oauth/authorize',
                            base_url='https://api.twitter.com/1.1/')

    request_token, request_token_secret = twitter.get_request_token()
    authorize_url = twitter.get_authorize_url(request_token)

    print 'Browse to this URL into your browser:\n' + authorize_url
    
    twitter_pin = raw_input('Enter PIN: ')
    
    session = twitter.get_auth_session(request_token,
                                       request_token_secret,
                                       method='POST',
                                       data={'oauth_verifier': twitter_pin})

    user_access_token = session.access_token
    user_access_token_secret = session.access_token_secret

    cfgfile = open('RTAnalyzerUser.ini', 'w')
    
    config.set('Access Tokens', 'user_access_token', user_access_token)
    config.set('Access Tokens', 'user_access_token_secret', user_access_token_secret)

    config.set('Profile', 'profile_set', True)

    config.write(cfgfile)
    cfgfile.close()

    session.close()

def main():
    # Read config file
    config.read('RTAnalyzerUser.ini')

    # First time set up
    if config.getboolean("Profile", "profile_set") == False:
        print "Profile not set. Setting up new profile..."
        setup_profile()

    # Continue program
    access_token = config.get('Access Tokens', 'user_access_token')
    access_token_secret = config.get('Access Tokens', 'user_access_token_secret')

    config.read('RTAnalyzerApp.ini')
    
    twitter = OAuth1Service(name='twitter',
                            consumer_key=config.get('Consumer Keys', 'consumer_key'),
                            consumer_secret=config.get('Consumer Keys', 'consumer_key_secret'),
                            request_token_url='https://api.twitter.com/oauth/request_token',
                            access_token_url='https://api.twitter.com/oauth/access_token',
                            authorize_url='https://api.twitter.com/oauth/authorize',
                            base_url='https://api.twitter.com/1.1/')

    session = twitter.get_session((access_token, access_token_secret))

    try:
        search_query = raw_input("Enter your keywords: ")
    except (KeyboardInterrupt, EOFError):
        print '\n'
        sys.exit()

    try:
        followers_threshold = input("Enter minimum number of followers (0 for no threshold): ")
        if ((followers_threshold < 0) or (type(followers_threshold) != int)):
            raise ValueError
    except (KeyboardInterrupt, EOFError):
        print '\n'
        sys.exit()
    except ValueError:
        print "That was not a valid number! Defaulting to no threshold..."
        followers_threshold = 0

    search_tweet_count = 50

    search_results = session.get('search/tweets.json', params={'q':search_query, 'lang':'en', 'count':search_tweet_count})

    search_results_json_string = search_results.json()
    print json.dumps(search_results_json_string, sort_keys=True, indent=4, separators=(',', ': '))

    tweet_database = [{'screen_name':None, 'followers_count':None} for _ in range(search_tweet_count)]

    for tweet in range(search_tweet_count):
        if search_results_json_string['statuses'][tweet]['user']['followers_count'] > followers_threshold:
            tweet_database[tweet]['screen_name'] = search_results_json_string['statuses'][tweet]['user']['screen_name']
            tweet_database[tweet]['followers_count'] = search_results_json_string['statuses'][tweet]['user']['followers_count']

    tweet_database = [new for new in tweet_database if None not in new.values()]

    # timeline_results = session.get('statuses/user_timeline.json', params={'screen_name':'Antrikshy', 'count':5, 'trim_user':1, 'exclude_replies':1})
    # timeline_results_json_string = timeline_results.json()
    # print json.dumps(timeline_results_json_string, sort_keys=True, indent=4, separators=(',', ': '))

    print tweet_database

    for user_dict in tweet_database:
        user_timeline = session.get('statuses/user_timeline.json', params={'screen_name':user_dict['screen_name'], 'count':5, 'trim_user':1})
        user_timeline_json_string = user_timeline.json()
        

if __name__ == "__main__":
    main()
