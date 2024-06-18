# Werewolf Client - Server

Werewolf Game developed in Python using PyQt and a client-server architecture. This project was completed in collaboration with classmates from various semesters, including first, second, fourth, and eight. Task management and ticket assignments were organized using Jira.

## Instructions to play it

1. Update the IP addresses and ports in both server.py and client.py.
2. Run server.py to start the moderator server.
3. Run client.py for each player, repeating until you have 8 players.
4. The moderator will click "Start Game" to assign roles to the players.
5. The moderator will use the buttons to control the game, including starting and ending voting or day phase, as well as starting and ending the night phase.
6. The night and day phases will repeat until a victory condition is met and then the game will be over.

## Instructions to test to game in local

1. Set the ip address to localhost
2. Run server.py to start the moderator server.
3. Run run_clients.py to start eight clients and test the game in local.

## Additional features

1. Login / Register with Firebase Firestore
2. Leaderboard with Firebase Firestore
