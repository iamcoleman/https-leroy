# Libs
import tweepy
# Files
from twitter_keys import getKeys
from random import randint
from drake import drake_lyrics
from fortune import fortunes
from magic8ball import answers

#######################################
# Get Twitter API keys
access_token, access_secret, consumer_key, consumer_secret = getKeys()
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
leroy = tweepy.API(auth)
#######################################

def reply(body, status):
	user = status.author.screen_name
	reply_id = status.id
	juice = body
	reply = "@"+user+" "+juice
	leroy.update_status(reply, in_reply_to_status_id=reply_id)
	print("Reply:")
	print(reply)


def get_user_TL(status):
	user = status.author.screen_name
	print("User: "+user)
	user_timeline = leroy.user_timeline(screen_name=user, count=200)
	print("Number of TL grabs: "+str(len(user_timeline)))
	user_tweets = []
	for tweet in user_timeline:
		if "RT @" not in tweet.text:
			user_tweets.append(tweet)
	print("Number of user tweets: "+str(len(user_tweets)))
	return user_tweets


def basic_stats(status):
	user_tweets = get_user_TL(status)
	num_tweets = len(user_tweets)
	### Retweets ###
	num_retweets = 0
	for tweet in user_tweets:
		num_retweets += tweet.retweet_count
	avg_rt = num_retweets / num_tweets
	avg_rt = round(avg_rt, 3)
	print("Total Number of RTs: "+str(num_retweets))
	print("Average Number of RTs: "+str(avg_rt))
	### Favorites ###
	num_favs = 0
	for tweet in user_tweets:
		num_favs += tweet.favorite_count
	avg_favs = num_favs / num_tweets
	avg_favs = round(avg_favs, 3)
	print("Total Number of Favs: "+str(num_favs))
	print("Average Number of Favs: "+str(avg_favs))
	#################
	body = "Based on your last 200 tweets, you averaged:\n" + str(avg_favs) + " favorites\n" + str(avg_rt) + " retweets"
	reply(body, status)


def retweets(status):
	user = status.author.screen_name
	print("User: "+user)
	user_timeline = leroy.user_timeline(screen_name=user, count=200)
	print("Number of TL grabs: "+str(len(user_timeline)))
	rts = []
	for tweet in user_timeline:
		if "RT @" in tweet.text:
			rts.append(tweet)
	print("Number of RTs: "+str(len(rts)))
	# sets initial kings and prev
	prev = 0
	king_user = ""
	king_num = 0
	for tweet in rts:
		# first iteration
		# sets the current position user and number of rts
		curr_user = tweet.retweeted_status.author.screen_name
		curr_num = 0
		# second iteration
		# checks current user with all tweets and sums number of rts
		i = 0
		while i < len(rts):
			if rts[i].retweeted_status.author.screen_name == curr_user:
				curr_num += 1
			i += 1
		# if the current number of rts is greater than the previous number
		# set the king name and king number, and update the prev to current king
		if curr_num > prev:
			king_user = curr_user
			king_num = curr_num
			prev = curr_num
	# create body
	if king_user == "":
		body = "Based on your last 200 tweets, you haven't retweeted anyone"
	else:
		body = "Based on your last 200 tweets, you retweeted @"+king_user+" ("+str(king_num)+") the most."
	reply(body, status)


def favorites(status):
	user = status.author.screen_name
	print("User: "+user)
	favorites = leroy.favorites(screen_name=user, count=200)
	print("Number of favorite grabs: "+str(len(favorites)))
	favs = []
	for tweet in favorites:
		favs.append(tweet)
	print("Number of favorites: "+str(len(favs)))
	# sets initial kings and prev
	prev = 0
	king_user = ""
	king_num = 0
	for tweet in favs:
		# first iteration
		# sets the current position user and number of favs
		curr_user = tweet.author.screen_name
		curr_num = 0
		# second iteration
		# checks current user with all tweets and sums number of favs
		i = 0
		while i < len(favs):
			if favs[i].author.screen_name == curr_user:
				curr_num += 1
			i += 1
		# if the current number of favs is greater than the previous number
		# set the king name and king number, and update the prev to current king
		if curr_num > prev:
			king_user = curr_user
			king_num = curr_num
			prev = curr_num
	# create body
	if king_user == "":
		body = "You haven't favorited any tweets!"
	else:
		body = "Based on your last 200 favorites, you favorited @"+king_user+" ("+str(king_num)+") the most."
	reply(body, status)


def best_friend(status):
	user_tweets = get_user_TL(status)
	if len(user_tweets) > 10:
		user_tweets = user_tweets[0:9]
	retweeters = []
	#FTN = 0
	for tweet in user_tweets:
		#FTN += 1
		#print("Tweet Number: "+str(FTN))
		results = leroy.retweets(tweet.id)
		results_count = tweet.retweet_count
		#print("Results: "+str(results_count))
		i = 0
		while i < results_count:
			retweeters.append(results[i].user.screen_name)
			i += 1
		#print("Current Retweeters: "+str(len(retweeters)))
	print("Total Retweets: "+str(len(retweeters)))
	# Find The King #
	prev = 0
	king_user = ""
	king_num = 0
	for user in retweeters:
		# first iteration
		# sets the current position user and number of retweets
		curr_user = user
		curr_num = 0
		# second iteration
		# checks current user with all users and sums number of retweets
		i = 0
		while i < len(retweeters):
			if retweeters[i] == curr_user:
				curr_num += 1
			i += 1
		# if the current number of favs is greater than the previous number
		# set the king name and king number, and update the prev to current king
		if curr_num > prev:
			king_user = curr_user
			king_num = curr_num
			prev = curr_num
	# Make the Body #
	if king_user == "":
		body = "Based on your last 10 tweets, no one has retweeted you. \nI'm so sorry..."
	else:
		body = "Based on your last 10 tweets, @"+king_user+" ("+str(king_num)+") retweeted you the most."
	reply(body, status)


def drake(status):
	length = len(drake_lyrics) - 1
	num = randint(0, length)
	body = drake_lyrics[num]
	print("Lyric: "+body)
	reply(body, status)


def fortune(status):
	length = len(fortunes) - 1
	num = randint(0, length)
	body = fortunes[num]
	print("Fortune: "+body)
	reply(body, status)


def thank_you(status):
	user_name = status.author.name
	body = "You're welcome, "+user_name+"!"
	reply(body, status)


def flip_a_coin(status):
	coin = randint(0, 1)
	if coin == 0:
		body = "Heads"
	else:
		body = "Tails"
	reply(body, status)


def magic_8_ball(status):
	length = len(answers) - 1
	i = randint(0, length)
	body = answers[i]
	reply(body, status)


def favorite_words(status):
	user_tweets = get_user_TL(status)
	length = len(user_tweets)
	good_words = []
	for tweet in user_tweets:
		text = tweet.text
		words = text.split()
		for word in words:
			if "@" not in word:
				good_words.append(word)
	print("Number of good_words: "+str(len(good_words)))
	## find top 5 ##
	word_occur = [0, 0, 0, 0, 0]
	king_words = ["", "", "", "", ""]
	for comp_word in good_words:
		curr_occur = 0
		for one_word in good_words:
			if one_word.lower() == comp_word.lower():
				curr_occur += 1
		# test current occurance against all king words
		if curr_occur > word_occur[0]:
			word_occur[0] = curr_occur
			king_words[0] = comp_word.lower()
		elif curr_occur > word_occur[1]:
			word_occur[1] = curr_occur
			king_words[1] = comp_word.lower()
		elif curr_occur > word_occur[2]:
			word_occur[2] = curr_occur
			king_words[2] = comp_word.lower()
		elif curr_occur > word_occur[3]:
			word_occur[3] = curr_occur
			king_words[3] = comp_word.lower()
		elif curr_occur > word_occur[4]:
			word_occur[4] = curr_occur
			king_words[4] = comp_word.lower()
	if (word_occur[0] == 0) or (word_occur[1] == 0) or (word_occur[2] == 0) or (word_occur[3] == 0) or (word_occur[4] == 0):
		body = "You haven't tweeted enough to have any favorite words..."
	else:
		body = "Your favorite words are '"+king_words[0]+"', '"+king_words[1]+"', '"+king_words[2]+"', '"+king_words[3]+"', and '"+king_words[4]
	reply(body, status)





#######################################
def decider(status):
	lower = status.text.lower()
	if "retweet stats" in lower:
		print("Includes retweet stats...")
		retweets(status)
	elif "favorite stats" in lower:
		print("Includes favorite stats...")
		favorites(status)
	elif "basic stats" in lower:
		print("Includes basic stats...")
		basic_stats(status)
	elif "drake" in lower:
		print("Includes drake...")
		drake(status)
	elif "best friend" in lower:
		print("Includes retweet friend...")
		best_friend(status)
	elif "fortune" in lower:
		print("Includes fortune...")
		fortune(status)
	elif ("thank you" in lower) or ("thanks" in lower):
		print("Includes thank you...")
		thank_you(status)
	elif "flip a coin" in lower:
		print("Includes flip a coin")
		flip_a_coin(status)
	elif ("magic 8 ball" in lower) or ("magic eight ball" in lower):
		print("Includes magic 8 ball")
		magic_8_ball(status)
	elif ("favorite words" in lower) or ("favorite word" in lower):
		print("Includes favorite words")
		favorite_words(status)
	else:
		print("Check out all my commands at ...")
#######################################

#######################################
class StreamListener(tweepy.StreamListener):

	def on_status(self, status):
		print("\nIncoming tweet by "+status.author.screen_name+":")
		print(status.text)
		decider(status)


	def on_error(self, status_code):
		if status_code == 420:
			return False
#######################################


#######################################
stream_listener = StreamListener()
print("Stream Starting...\n")
stream = tweepy.Stream(auth=leroy.auth, listener=stream_listener)
stream.filter(track=["@httpsLeroy"])
#######################################
