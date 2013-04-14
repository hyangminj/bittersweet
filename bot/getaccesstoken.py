import tweepy, webbrowser
import config

if __name__ == '__main__':
  auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
  auth_url = auth.get_authorization_url(signin_with_twitter=True)
  webbrowser.open(auth_url)
  verifier = raw_input('PIN: ').strip()
  auth.get_access_token(verifier)
  print "access_key = '%s'" % auth.access_token.key
  print "access_secret = '%s'" % auth.access_token.secret
