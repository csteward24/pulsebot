import discord
import asyncio
import pickle
import os.path
from datetime import datetime, timedelta, timezone
from xptable import *

levels = [0,10,100]
print("initializing bot")
client = discord.Client()

if(os.path.isfile("pulse_xp.p")):
    print("true")
    xp_table = pickle.load(open("pulse_xp.p","rb"))
else:
    xp_table = XpTable()
    print("false")
    pickle.dump(xp_table, open("pulse_xp.p","wb"))
print(xp_table)



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('p.'):
        command = message.content.split('.', 1)[1]
        args = command.split(" ")
        command = args[0]
        if(command == 'test'):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            async for log in client.logs_from(message.channel, limit=100):
                if log.author == message.author:
                    counter += 1
            
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        elif(command == 'sleep'):
            await asyncio.sleep(5)
            await client.send_message(message.channel, 'Done sleeping')
        elif(command == 'help'):
            await client.send_message(message.channel, '''```Current Commands:
test
help
sleep
frog
xp add (usr)(num)
xp get (usr)
```''')
        elif(command == 'frog'):
            await client.send_message(message.channel, 'FROGS!')
        elif(command == 'xp'):
            args = message.content.split()
            if(xp_table.getKeyByName(args[2]) is not None):
                usr = xp_table.getKeyByName(args[2])
                if args[1] == "add":
                    xp_table[usr] = int(args[3])
                    await client.send_message(message.channel, "gave %s %d points" % (args[2],int(args[3])))
                if args[1] == "get":
                    pts = xp_table[usr]
                    await client.send_message(message.channel, "%s has %d points" % (args[2],pts))
                    i = 0
                    for level in levels:
                        if(xp_table[usr] < level):
                            await client.send_message(message.channel, "%s is level %d" % (args[2],i - 1))
                            break;
                        i += 1
            else:
                await client.send_message(message.channel, "user not found")
    if(message.author != client.user):
        counter = 0
        day = False
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                if(timedelta(days = 1) > datetime.utcnow() - log.timestamp):
                    day = True
                if(timedelta(minutes = 1) > datetime.utcnow() - log.timestamp):
                    counter += 1
            
        xp_table[message.author] = xp_table.setdefault(message.author,0)+day+counter
        print(xp_table)
    pickle.dump(xp_table, open("pulse_xp.p","wb"))
    

    

client.run("its a secret")
