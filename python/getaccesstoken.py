import sys, re
import urllib, urllib2
import getpass

import tweepy
from bs4 import BeautifulSoup

import config

def get_access_token():
	# try - except
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
	auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
	redirect_url = auth.get_authorization_url()

	page = opener.open(redirect_url).read()
	soup = BeautifulSoup(page)

	for tag in soup.find_all('div'):
		if 'class' in tag.attrs and ' '.join(tag['class']) == 'permissions allow':
			print '--------'
			print tag.get_text()
			print '--------'

	print "ok?"
	user_id = raw_input('Username: ')
	password = getpass.getpass()


	# get auth token
	auth_token = ''
	for tag in soup.find_all('input'):
		if tag.name == 'authenticity_token':
			auth_token = tag.value
	# check error
	# if auth_token == '':
	#

	login_params = urllib.urlencode({'authenticity_token': auth_token,
		'session[username_or_email]': user_id,
		'session[password]': password,
		'Authorize app': 'allow'})
	#  try - except
	page = opener.open(redirect_url, login_params)
	soup = BeautifulSoup(page)
	verifier = ''
	for tag in soup.findAll('meta'):
		if 'http-equiv' in tag.attrs and tag['http-equiv'] == 'refresh':
			# try-except
			verifier = re.search(r'oauth_verifier=(\w+)', tag['content']).group(1)
	auth.get_access_token(verifier)

	print
	print "Add below lines into config.py"
	print "access_key = %s\naccess_secret = %s" % (auth.access_token.key, auth.access_token.secret)

if __name__ == '__main__':
	get_access_token()
