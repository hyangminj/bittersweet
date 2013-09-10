#!/usr/bin/python
# -*- coding:utf-8 -*-

def getaccesstoken():
	import tweepy, webbrowser
	import config
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret, callback='oob')
	auth_url = auth.get_authorization_url(signin_with_twitter=True)
	webbrowser.open(auth_url)
	verifier = raw_input('PIN: ').strip()
	auth.get_access_token(verifier)
	print "access_key = '%s'" % auth.access_token.key
	print "access_secret = '%s'" % auth.access_token.secret
	return

# https://gist.github.com/mtigas/810514
def tweetlist():
	import data
	for v in data.voices:
		v = unicode(v, 'utf-8')
		print v
		print 'Length: ', len(v)
		print

if __name__ == '__main__':
	import sys
	if len(sys.argv) == 2:
		if 'getaccesstoken' == sys.argv[1]:
			getaccesstoken()
		if 'tweetlist' == sys.argv[1]:
			tweetlist()
	else:
		print "Usage: %s getaccesstoken|tweetlist" % sys.argv[0]
		sys.exit(1)
