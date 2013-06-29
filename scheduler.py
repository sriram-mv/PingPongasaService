import queuing
import mailgun
import object_rocket
import authentication
import pymongo
import random
import pprint
import json


def get_auth():
    # Get Authentication
	return authentication.auth()

CONNECTION = get_auth()

def pick_random_two_people():
    # Randomly picks two players from the Players collection to have a go at each other!
	creds = object_rocket.get_creds()
	Database = object_rocket.get_connection(creds)
	choice1 = random.randrange(1,object_rocket.get_count_Players(Database))
	choice2 = random.randrange(1,object_rocket.get_count_Players(Database))
	return (Database.Players.find({},{'_id':0}).limit(-1).skip(choice1).next(),Database.Players.find({},{'_id':0}).limit(-1).skip(choice2).next())

def convert_json(Racker1,Racker2):
    # Conversion to json as the cloud queuing API expects a well formed JSON
	Racker1 = json.loads(json.dumps(Racker1))
	Racker2 = json.loads(json.dumps(Racker2))
	return Racker1,Racker2

def email_mode(Racker):
    # Set notification method to be email.
	Racker['Mode'] = 'Email'
	return Racker

def twitter_mode(Racker):
    # todo : Not yet supported
	return {"Mode":"Twitter","Data":Racker}

def schedule():
    # Interact with the queuing API
	Racker1, Racker2 = pick_random_two_people()
	Racker1,Racker2 = convert_json(Racker1,Racker2)
	Racker1_Mode = email_mode(Racker1)
	Racker2_Mode = email_mode(Racker2)
	message1 = json.dumps(queuing.construct_json(Racker1_Mode))
	message2 = json.dumps(queuing.construct_json(Racker2_Mode))
	queuing.insert_messages(CONNECTION,message1,'Ping')
	queuing.insert_messages(CONNECTION,message2,'Ping')

def newqueue():
	queuing.create_queue(CONNECTION,'Ping')

def send_mail(message1,message2):
    # Usr mailgun to belt out an email!! Woot!
	data = {"from": "PingPongBot <PingPongBot@atlraxpingpong.com>",
			"to": [message1['body']['Email'],message2['body']['Email']],
			"subject": "Invitation to Ping Pong Tournament",
			"text" : "Starts Now!! --Preview Test-"}
	response = mailgun.send_simple_message(data)
	if response.status_code == 200:
		print "Invitation Sent!"

def leaderboard_update(winner,score):
    # Update the Leaderboard after getting the results of the match
    creds = object_rocket.get_creds()
    Database = object_rocket.get_connection(creds)
    Database.Leaderboard.update({'first_name' : winner},{"$inc":{'Wins':1}})
    Database.Leaderboard.update({'first_name' : winner},{"$set":{'Best':score}})
    Database.Leaderboard.update({'first_name':message1['body']['first_name']},{"$inc":{'Matches':1}})
    Database.Leaderboard.update({'first_name':message2['body']['first_name']},{"$inc":{'Matches':1}})

def get_result(message1,message2):
    # get results for the match
    winner = raw_input("Enter the Winner\n")
    score = raw_input("Enter the Score\n")
    leaderboard_update(winner,score)

def send_notifactions():
    # claim Messages in the queue
	(claim_response,message_id,claim_id,status_code) = queuing.claim_messages(CONNECTION,queuing.for_claim(),'Ping')
	if status_code == 204:
		print "Queue is Empty"
	claim = claim_response.json()
	message = list()
	for single_claim in claim:
		message.append(json.loads(json.dumps(single_claim)))

	print message[0]['body']['Email'] +" vs "+ message[1]['body']['Email']

	if message[0]['body']['Mode'] == 'Email' and message[1]['body']['Mode'] == 'Email':
		send_mail(message[0],message[1])
        get_result(message[0],message[1])
        get_leaderboard()

def get_leaderboard():
    # Print Leaderbaord
    creds = object_rocket.get_creds()
    Database = object_rocket.get_connection(creds)
    print "\t\t\t\t\t\t\t\tLeaderBoard\n"
    print "\t\t\tName\t\t\tMatches\t\t\tWins\t\t\tBest"
    for posts in Database.Leaderboard.find().sort("Wins",-1):

        print "\t\t\t{0}\t\t\t{1}\t\t\t{2}\t\t\t{3}".format(posts['first_name'].split()[0],posts['Matches'],posts['Wins'],posts['Best']) 


def main():
	get_leaderboard()
	newqueue()
	schedule()
	send_notifactions()

if __name__ == '__main__':
	main()