# Konsumwage-Server
The backend for Konsumwage collecting and redistributing data.
This is still very much work in progress. There's no actual physical scale yet, for example.
## What's Konsumwage?!
Basically an internet enabled scale for measuring consumtion of something you can put on top of it (bottles, a barrel of beer, food, whatever).

The backend recieves this, and relays it to clients using WebSockets.

The Clients recieve all past measurements and real time updates and plots these using Plot.js
