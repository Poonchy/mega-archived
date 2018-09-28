# Work with Python 3.6
import discord
import time
import calendar
import pymysql
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import io
import os
import re
import datetime

TOKEN = app_id = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_message(message):
    conn = pymysql.connect(os.environ['herokuServer'],os.environ['herokuUser'],os.environ['herokuPass'],os.environ['herokuDB'])
    usermessage = message.content.upper() 
    if message.author == client.user:
        return
    if usermessage.startswith('MEGA HELP'):
        msg = 'Hello, {0.author.mention}, I\'m a Machine Engineered to Guide Anyone, or M.E.G.A! Type "Mega Create Hero" in the discord chat you were in to get started, or "Mega Delete" to delete your hero.'.format(message)
        await client.send_message(message.author, msg)
    if usermessage.startswith('MEGA INTRODUCE YOURSELF'):
        msg = 'Hello, {0.author.mention}, I\'m a Machine Engineered to Guide Anyone, or M.E.G.A! Type "Mega Create Hero" to get started, or "Mega Delete" to delete your hero.'.format(message)
        await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA CREATE HERO'):
        usertoken = '{0.author.mention}'.format(message)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
        conn.commit()
        if not cursor.rowcount:
            await client.send_message(message.channel, "You can create a character!\nSimply respond with (Mega create my orc/human warrior/mage named XXX).")
        else:
            await client.send_message(message.channel, "You already have a character! Type in, 'Mega Hero' to view them!")
    if usermessage.startswith('MEGA CREATE MY'):
        #Checks if user already has a character
        usertoken = '{0.author.mention}'.format(message)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
        conn.commit()
        if not cursor.rowcount:
            if 'NAMED' in usermessage and ('warrior' in message.content or 'mage' in message.content) and ('orc' in message.content or 'human' in message.content) and len(message.content.split()) >= 7:
                regexp = re.compile("named (.*)$")
                name = regexp.search(message.content).group(1)
                name = " ".join(name.split()).title()
                for k in name.split("\n"):
                    name = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
                usertoken = '{0.author.mention}'.format(message)
                cursor = conn.cursor()
                heroClass = ""
                heroRace = ""
                heroChest = ""
                heroGloves = ""
                heroBelt = ""
                heroLegs = ""
                heroFeet = ""
                heroMH = ""
                heroHealth = ""
                heroStam = ""
                heroArmor = ""
                heroInt = ""
                heroStr = ""
                heroAgi = ""
                heroCrit = ""
                if 'warrior' in message.content and len(message.content.split()) >= 7:
                    heroClass = "warrior"
                    heroChest = "31"
                    heroGloves = "41"
                    heroBelt = "51"
                    heroLegs = "61"
                    heroFeet = "71"
                    heroMH = "81"
                    heroHealth = "150"
                    heroStam = "10"
                    heroArmor = "15"
                    heroInt = "0"
                    heroStr = "10"
                    heroAgi = "0"
                    heroCrit = "10"
                if 'mage' in message.content and len(message.content.split()) >= 7:
                    heroClass = "mage"
                    heroChest = "32"
                    heroGloves = "42"
                    heroBelt = "52"
                    heroLegs = "62"
                    heroFeet = "72"
                    heroMH = "82"
                    heroHealth = "100"
                    heroStam = "5"
                    heroArmor = "5"
                    heroInt = "15"
                    heroStr = "0"
                    heroAgi = "0"
                    heroCrit = "20"
                if 'orc' in message.content and len(message.content.split()) >= 7:
                    heroRace = "orc"
                    if 'mage' in message.content:
                        heroInt = str(int(heroInt) + 1)
                    if 'warrior' in message.content:
                        heroStr = str(int(heroStr) + 1)
                if 'human' in message.content and len(message.content.split()) >= 7:
                    heroRace = "human"
                    heroHealth = str(int(heroHealth) + 10)
                    heroStam = str(int(heroStam) + 1)
                heroInventory = heroChest + ", " + heroGloves + ", " + heroBelt + ", " + heroLegs + ", " + heroFeet + ", " + heroMH
                cursor.execute("INSERT INTO AzerothHeroes (userID, heroName, heroRace, heroClass, heroHelm, heroShoulders, heroChest, heroGloves, heroBelt, heroLegs, heroFeet, heroMH, heroOH, heroInventory, heroCurrentHealth, heroMaximumHealth, heroStamina, heroArmor, heroInt, heroStr, heroAgi, heroCrit, EXP, level, timeTrained, healthRegenTimer) VALUES ('" + usertoken + "','" + name +"','" + heroRace + "','" + heroClass + "','0','0','" + heroChest + "','" + heroGloves +"','" + heroBelt + "','" + heroLegs + "','" + heroFeet + "','" + heroMH + "','0','" + heroInventory + "','" + heroHealth + "','" + heroHealth + "','" + heroStam + "','" + heroArmor + "','" + heroInt + "','" + heroStr + "','" + heroAgi + "','" + heroCrit + "','0','1','0','0');")
                conn.commit()
                await client.send_message(message.channel, "You chose a " + heroRace + " " + heroClass + " named " + name + "! To view your character type in, 'Mega Hero'.")
        else:
            await client.send_message(message.channel, "You already have a character! Say, 'Mega Hero' to view them!")
    if usermessage.startswith('MEGA HERO'):
        usertoken = '{0.author.mention}'.format(message)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
        conn.commit()
        query = cursor.fetchall()
        if cursor.rowcount:
            userdata = []
            for row in query:
                for col in row:
                    userdata.append("%s" % col)
            heroName = userdata[1]
            heroRace = userdata[2]
            heroClass = userdata[3]
            if heroRace == "orc":
                heroHelm = "orc" + str(userdata[4])
                heroShoulder = "orc" + str(userdata[5])
                heroChest = "orc" + str(userdata[6])
                heroGloves = "orc" + str(userdata[7])
                heroBelt = "orc" + str(userdata[8])
                heroLegs = "orc" + str(userdata[9])
                heroFeet = "orc" + str(userdata[10])
            if heroRace == "human":
                heroHelm = "human" + str(userdata[4])
                heroShoulder = "human" + str(userdata[5])
                heroChest = "human" + str(userdata[6])
                heroGloves = "human" + str(userdata[7])
                heroBelt = "human" + str(userdata[8])
                heroLegs = "human" + str(userdata[9])
                heroFeet = "human" + str(userdata[10])
            heroMH = userdata[11]
            heroOH = userdata[12]
            heroCurrentHealth = userdata[14]
            heroMaximumHealth = userdata[15]
            heroStam = userdata[16]
            heroArmor = userdata[17]
            heroInt = userdata[18]
            heroStr = userdata[19]
            heroAgi = userdata[20]
            heroCrit = userdata[21]
            heroEXP = userdata[22]
            heroLevel = userdata[23]
            background = Image.open('Items/white.jpg')
            hero = Image.open("Items/" + str(heroRace) + '.png')
            helmet = Image.open("Items/" + str(heroHelm) + '.png')
            shoulders = Image.open("Items/" + str(heroShoulder) + '.png')
            chest = Image.open("Items/" + str(heroChest) + '.png')
            gloves = Image.open("Items/" + str(heroGloves) + '.png')
            belt = Image.open("Items/" + str(heroBelt) + '.png')
            legs = Image.open("Items/" + str(heroLegs) + '.png')
            feet = Image.open("Items/" + str(heroFeet) + '.png')
            mainhand = Image.open("Items/" + str(heroMH) + '.png')
            offhand = Image.open("Items/" + str(heroOH) + '.png')
            healthbar = Image.open("Items/health.png")
            healthbarFrame = Image.open("Items/healthBarFrame.png")
            canvas = Image.new('RGBA', (500,500), (0, 0, 0, 0))
            canvas = Image.new('RGBA', (500,500), (0, 0, 0, 0))
            canvas.paste(background, (0,0))
            canvas.paste(hero, (160, 180), mask=hero)
            canvas.paste(helmet, (160, 180), mask=helmet)
            canvas.paste(shoulders, (160, 180), mask=shoulders)
            canvas.paste(chest, (160, 180), mask=chest)
            canvas.paste(gloves, (160, 180), mask=gloves)
            canvas.paste(belt, (160, 180), mask=belt)
            canvas.paste(legs, (160, 180), mask=legs)
            canvas.paste(feet, (160, 180), mask=feet)
            canvas.paste(mainhand, (160, 180), mask=mainhand)
            canvas.paste(offhand, (160, 180), mask=offhand)
            font = ImageFont.truetype("helvetica.ttf", 20)
            d = ImageDraw.Draw(canvas)
            d.text((10,10), "Hero: " + heroName, fill=(0,0,0), font = font)
            d.text((10,30), "Specialization: " + heroRace.title() + " " + heroClass.title() + ".", fill=(0,0,0), font = font)
            d.text((10,50), "Health: " + heroCurrentHealth + " / " + heroMaximumHealth, fill=(0,0,0), font = font)
            remainingHealth = int((int(heroCurrentHealth) / int(heroMaximumHealth)) * 62)
            ActualHealthBar = healthbar.crop((0,0,remainingHealth,22))
            canvas.paste(ActualHealthBar, (10, 70), mask=ActualHealthBar)
            canvas.paste(healthbarFrame, (10, 70), mask=healthbarFrame)
            d.text((350,70), "Level: " + heroLevel, fill=(0,0,0), font = font)
            d.text((350,90), "EXP: " + heroEXP, fill=(0,0,0), font = font)
            d.text((350,50), "Armor: " + heroArmor, fill=(0,0,0), font = font)
            d.text((350,30), "Stamina: " + heroStam, fill=(0,0,0), font = font)
            if heroClass == "warrior":
                d.text((350,10), "Strength: " + heroStr, fill=(0,0,0), font = font)
            if heroClass == "mage":
                d.text((350,10), "Intellect: " + heroInt, fill=(0,0,0), font = font)
            canvas.save('hero.png', format="png")
            await client.send_file(message.channel, 'hero.png')
            os.remove("hero.png")
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA TRAIN'):
        usertoken = '{0.author.mention}'.format(message)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
        conn.commit()
        query = cursor.fetchall()
        if cursor.rowcount:
            userdata = []
            for row in query:
                for col in row:
                    userdata.append("%s" % col)
            heroName = userdata[1]
            heroClass = userdata[2]
            heroEXP = int(userdata[3])
            heroLevel = int(userdata[4])
            heroTrained = int(userdata[5])
            currentTime = calendar.timegm(time.gmtime())
            timeleft = int(currentTime) - int(heroTrained)
            if timeleft > 43200:
                heroEXP += 1
                cursor.execute("UPDATE AzerothHeroes SET EXP = '" + str(heroEXP) + "' WHERE userID = '%" + usertoken + "%';")
                conn.commit()
                cursor.execute("UPDATE AzerothHeroes SET timeTrained = '" + str(currentTime) + "' WHERE userID = '%" + usertoken + "%';")
                conn.commit()
                await client.send_message(message.channel, "Updated EXP for " + heroName + ".")
                if heroEXP >= 2 and heroLevel <2:
                    heroLevel += 1
                    cursor.execute("UPDATE AzerothHeroes SET level = '" + str(heroLevel) + "' WHERE userID = '%" + usertoken + "%';")
                    conn.commit()
                    await client.send_message(message.channel, "Ding! You leveled up to level " + str(heroLevel) + ".")
                elif heroEXP >= 4 and heroLevel <3:
                    heroLevel += 1
                    cursor.execute("UPDATE AzerothHeroes SET level = '" + str(heroLevel) + "' WHERE userID = '%" + usertoken + "%';")
                    conn.commit()
                    await client.send_message(message.channel, "Ding! You leveled up to level " + str(heroLevel) + ".")
                elif heroEXP >= 8 and heroLevel <4:
                    heroLevel += 1
                    cursor.execute("UPDATE AzerothHeroes SET level = '" + str(heroLevel) + "' WHERE userID = '%" + usertoken + "%';")
                    conn.commit()
                    await client.send_message(message.channel, "Ding! You leveled up to level " + str(heroLevel) + ".")
                elif heroEXP >= 16 and heroLevel <5:
                    heroLevel += 1
                    cursor.execute("UPDATE AzerothHeroes SET level = '" + str(heroLevel) + "' WHERE userID = '%" + usertoken + "%';")
                    conn.commit()
                    await client.send_message(message.channel, "Ding! You leveled up to level " + str(heroLevel) + ".")
                if heroClass == 'knight':
                    im = Image.open('knight.gif')
                    frames = []
                    for frame in ImageSequence.Iterator(im):
                        font = ImageFont.truetype("helvetica.ttf", 20)
                        d = ImageDraw.Draw(frame)
                        d.text((10,10), "Name: " + heroName, font=font)
                        d.text((10,30), "Level: " + str(heroLevel), font=font)
                        d.text((10,50), "EXP: " + str(heroEXP), font=font)
                        del d
                        b = io.BytesIO()
                        frame.save(b, format="GIF")
                        frame = Image.open(b)
                        frames.append(frame)
                    frames[0].save('out.gif', save_all=True, append_images=frames[1:])
                    await client.send_file(message.channel, 'out.gif')
                    os.remove("out.gif")
                if heroClass == 'mage':
                    im = Image.open('mage.gif')
                    frames = []
                    for frame in ImageSequence.Iterator(im):
                        font = ImageFont.truetype("helvetica.ttf", 20)
                        d = ImageDraw.Draw(frame)
                        d.text((10,10), "Name: " + heroName, font=font)
                        d.text((10,30), "Level: " + str(heroLevel), font=font)
                        d.text((10,50), "EXP: " + str(heroEXP), font=font)
                        del d
                        b = io.BytesIO()
                        frame.save(b, format="GIF")
                        frame = Image.open(b)
                        frames.append(frame)
                    frames[0].save('out.gif', save_all=True, append_images=frames[1:])
                    await client.send_file(message.channel, 'out.gif')
                    os.remove("out.gif")
            else:
                timeToCalc = 43200 - (int(currentTime) - int(heroTrained))
                await client.send_message(message.channel, "You have to wait " + str(datetime.timedelta(seconds=timeToCalc)) + " before you can train.")
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA DELETE'):
        usertoken = '{0.author.mention}'.format(message)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
        conn.commit()
        query = cursor.fetchall()

        if cursor.rowcount:
            msg = 'Are you sure you want to delete your hero? This cannot be undone.\nType in "I wish to delete XXX" replacing XXX with your hero\'s name.'.format(message)
            await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('I WISH TO DELETE'):
        usertoken = '{0.author.mention}'.format(message)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
        conn.commit()
        query = cursor.fetchall()
        if cursor.rowcount:
            userdata = []
            for row in query:
                for col in row:
                    userdata.append("%s" % col)
            heroName = userdata[1]

            regexp = re.compile("delete (.*)$")
            name = regexp.search(message.content).group(1)
            name = " ".join(name.split()).title()
            for k in name.split("\n"):
                name = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
            if name == heroName:
                cursor.execute("DELETE FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
                conn.commit()
                msg = 'Your hero has been destroyed. Type "Mega Create Hero" to start your journey.'.format(message)
                await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA SOURCE'):
        msg = 'Created by Poonchy, check out my other works:\nhttps://poonchy.github.io'.format(message)
        await client.send_message(message.channel, msg)
        await client.send_file(message.channel, 'source.py')
    conn.close()
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Mega Help'))
client.run(TOKEN)