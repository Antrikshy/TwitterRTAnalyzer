TwitterRTAnalyzer
=================
A command line tool that you can use to find Twitter users who can potentially aid you in spreading your idea. It currently uses a very rudimentary algorithm, but it can be kind of effective. My main purpose was to learn how OAuth works. Before I found rauth, I tried to implement the OAuth dance manually. I learned a lot about how it works behind the scenes but I could not get it to work properly.

How to use
----------
Until I release a packaged version, you will need to install Python and rauth on your computer to run this. rauth is the only dependency.

You need to login once. Then search for a keyword. It will pick users from the search results and remove the ones that are below your specified follower count threshold. Then it will give you a list of users, sorted by follower count that interact enough (have a good percentage of replies and retweets in their last 200 tweets).