# pychat
A python server-client chatter room application based on the works of https://gist.github.com/schedutron. 

Major improvements: Error handling and stability.

## Installation
Install python3 on both the server and your client PC.

## Run
On server (e.g. Ubuntu), first you need to open firewall and iptables for chatter listening port, default 33000. 

To add iptables rule, run: iptables -I INPUT -p tcp --dport 33000 -j ACCEPT

then start server application: python3 chat_serv.py

On any windows client PC when you want to join the chatter room, just double-click chat_clnt.py or run: python chat_clnt.py.
