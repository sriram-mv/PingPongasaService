PingPongasaService
==================

Ping Pong as a Service lets you select random matches to be played between opponents and maintain a Leaderboard.

Note
========
The credentials.conf needs to be populated with the needed API keys,usernames and passwords (Rackspace)

Running the Service
===================

python scheduler.py


APIs
========
This project makes use of MailGun for notification, ObjectRocket (MongoDB as a service )to store the database in the cloud.Cloud Queuing for Putting messages in the queue (randomly picking 2 people for the match), Mailgun reads from the queue and sends out emails to the players. On Completion of the Match, the App takes input on who won and computes a Leaderboard.

Note: Idea was conceived on a hack day at Rackspace Atlanta.
