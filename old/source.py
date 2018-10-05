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
import random
from random import randint
import math

#TOKEN = app_id = os.environ['TOKEN']
TOKEN = 'NDk0MjA1MjkyMDkxODAxNjEw.DowSyQ.eCbexx0BpoP-5a4GyQeblXhzzVs'

client = discord.Client()

@client.event
async def on_message(message):
    #conn = pymysql.connect(os.environ['herokuServer'],os.environ['herokuUser'],os.environ['herokuPass'],os.environ['herokuDB'])
    conn = pymysql.connect("localhost","root","1999stav","AzerothHeroes")
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
            await client.send_message(message.channel, "You can create a character!\nSimply respond with (Mega create my orc/human warrior/mage/rogue named XXX).")
        else:
            await client.send_message(message.channel, "You already have a character! Type in, 'Mega Hero' to view them!")
    if usermessage.startswith('MEGA CREATE MY'):
        #Checks if user already has a character
        usertoken = '{0.author.mention}'.format(message)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
        conn.commit()
        timeNow = calendar.timegm(time.gmtime())
        if not cursor.rowcount:
            if 'NAMED' in usermessage and ('warrior' in message.content or 'mage' in message.content or 'rogue' in message.content) and ('orc' in message.content or 'human' in message.content) and len(message.content.split()) >= 7:
                regexp = re.compile("named (.*)$")
                name = regexp.search(message.content).group(1)
                name = " ".join(name.split()).title()
                for k in name.split("\n"):
                    name = re.sub(r"[^a-zA-Z0-9]+", '', k)
                if len(name) < 12:
                    heroClass = ""
                    heroRace = ""
                    heroChest = ""
                    heroGloves = ""
                    heroBelt = ""
                    heroLegs = ""
                    heroFeet = ""
                    heroMH = ""
                    heroOH = ""
                    heroHealth = ""
                    heroStam = ""
                    heroArmor = ""
                    heroInt = ""
                    heroStr = ""
                    heroAgi = ""
                    heroCrit = ""
                    heroDamage = ""
                    if 'warrior' in message.content and len(message.content.split()) >= 7:
                        heroClass = "warrior"
                        heroChest = "31"
                        heroGloves = "41"
                        heroBelt = "51"
                        heroLegs = "61"
                        heroFeet = "71"
                        heroMH = "81"
                        heroOH = "0"
                        heroHealth = "150"
                        heroStam = "10"
                        heroArmor = "15"
                        heroInt = "0"
                        heroStr = "10"
                        heroAgi = "0"
                        heroCrit = "5"
                        heroDamage = "5"
                    elif 'mage' in message.content and len(message.content.split()) >= 7:
                        heroClass = "mage"
                        heroChest = "32"
                        heroGloves = "42"
                        heroBelt = "52"
                        heroLegs = "62"
                        heroFeet = "72"
                        heroMH = "82"
                        heroOH = "0"
                        heroHealth = "100"
                        heroStam = "5"
                        heroArmor = "5"
                        heroInt = "15"
                        heroStr = "0"
                        heroAgi = "0"
                        heroCrit = "10"
                        heroDamage = "1"
                    elif 'rogue' in message.content and len(message.content.split()) >= 7:
                        heroClass = "rogue"
                        heroChest = "33"
                        heroGloves = "43"
                        heroBelt = "53"
                        heroLegs = "63"
                        heroFeet = "73"
                        heroMH = "83"
                        heroOH = "91"
                        heroHealth = "120"
                        heroStam = "7"
                        heroArmor = "10"
                        heroInt = "0"
                        heroStr = "0"
                        heroAgi = "14"
                        heroCrit = "20"
                        heroDamage = "4"
                    if 'orc' in message.content and len(message.content.split()) >= 7:
                        heroRace = "orc"
                        if 'warrior' in message.content:
                            heroStr = str(int(heroStr) + 1)
                        elif 'mage' in message.content:
                            heroInt = str(int(heroInt) + 1)
                        elif 'rogue' in message.content:
                            heroAgi = str(int(heroAgi) + 1)
                    elif 'human' in message.content and len(message.content.split()) >= 7:
                        heroRace = "human"
                        heroHealth = str(int(heroHealth) + 10)
                        heroStam = str(int(heroStam) + 1)
                    heroInventory = heroChest + " " + heroGloves + " " + heroBelt + " " + heroLegs + " " + heroFeet + " " + heroMH + " " + heroOH
                    cursor.execute("INSERT INTO AzerothHeroes (userID, heroName, heroRace, heroClass, heroHelm, heroShoulders, heroChest, heroGloves, heroBelt, heroLegs, heroFeet, heroMH, heroOH, heroInventory, heroCurrentHealth, heroMaximumHealth, heroStamina, heroArmor, heroInt, heroStr, heroAgi, heroCrit, EXP, level, heroGold, timeUpdated, carryOverSeconds, heroDamage) VALUES ('" + usertoken + "','" + name +"','" + heroRace + "','" + heroClass + "','0','0','" + heroChest + "','" + heroGloves +"','" + heroBelt + "','" + heroLegs + "','" + heroFeet + "','" + heroMH + "','" + heroOH + "','" + heroInventory + "','" + heroHealth + "','" + heroHealth + "','" + heroStam + "','" + heroArmor + "','" + heroInt + "','" + heroStr + "','" + heroAgi + "','" + heroCrit + "','0','1','0','" + str(timeNow) + "','0', '" + heroDamage + "');")
                    conn.commit()
                    await client.send_message(message.channel, "You chose a " + heroRace + " " + heroClass + " named " + name + "! To view your character type in, 'Mega Hero'.")
                else:
                    await client.send_message(message.channel, "Your name was too long! A name cannot be longer than 12 characters.")
            else:
                await client.send_message(message.channel, "Your response was formatted incorrectly. Make sure to include your race, class and name! An example:\nMega create my orc warrior named zugzug.")
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
            heroOffSet = 0
            if heroRace == "orc":
                heroHelm = "orc" + str(userdata[4])
                heroShoulder = "orc" + str(userdata[5])
                heroChest = "orc" + str(userdata[6])
                heroGloves = "orc" + str(userdata[7])
                heroBelt = "orc" + str(userdata[8])
                heroLegs = "orc" + str(userdata[9])
                heroFeet = "orc" + str(userdata[10])
                heroOH = "orc" + str(userdata[12])
                heroOffSet = (110,180)
            if heroRace == "human":
                heroHelm = "human" + str(userdata[4])
                heroShoulder = "human" + str(userdata[5])
                heroChest = "human" + str(userdata[6])
                heroGloves = "human" + str(userdata[7])
                heroBelt = "human" + str(userdata[8])
                heroLegs = "human" + str(userdata[9])
                heroFeet = "human" + str(userdata[10])
                heroOH = "human" + str(userdata[12])
                heroOffSet = (110,180)
            heroMH = userdata[11]
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
            heroGold = userdata[24]
            heroUpdateTimer = userdata[25]
            carryOverTime = userdata[26]
            timeNow = calendar.timegm(time.gmtime())
            if int(heroCurrentHealth) < int(heroMaximumHealth):
                timerUsed = 3600 / (int(heroMaximumHealth) * .15)
                timeSinceLast = timeNow - int(heroUpdateTimer)
                healthToRegen = math.floor(timeSinceLast/timerUsed)
                remainingTime = int(timeSinceLast) % timerUsed
                carryOverTime = float(carryOverTime) + int(remainingTime)
                while float(carryOverTime) >= timerUsed:
                    carryOverTime = float(carryOverTime) - timerUsed
                    healthToRegen += 1
                heroCurrentHealth = int(healthToRegen) + int(heroCurrentHealth)
                if int(heroCurrentHealth) >= int(heroMaximumHealth):
                    heroCurrentHealth = int(heroMaximumHealth)
                    carryOverTime = 0
            elif int(heroCurrentHealth) == int(heroMaximumHealth):
                carryOverTime = 0
            cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(heroCurrentHealth) + "', timeUpdated = '" + str(timeNow) + "', carryOverSeconds = '" + str(carryOverTime) + "' WHERE userID = '" + usertoken + "';")
            conn.commit()
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
            goldCoin = Image.open("Items/goldcoin.png")
            canvas = Image.new('RGBA', (500,500), (0, 0, 0, 0))
            canvas = Image.new('RGBA', (500,500), (0, 0, 0, 0))
            canvas.paste(background, (0,0))
            canvas.paste(hero, heroOffSet, mask=hero)
            canvas.paste(feet, heroOffSet, mask=feet)
            canvas.paste(legs, heroOffSet, mask=legs)
            canvas.paste(gloves, heroOffSet, mask=gloves)
            canvas.paste(helmet, heroOffSet, mask=helmet)
            canvas.paste(shoulders, heroOffSet, mask=shoulders)
            canvas.paste(chest, heroOffSet, mask=chest)
            canvas.paste(belt, heroOffSet, mask=belt)
            canvas.paste(mainhand, heroOffSet, mask=mainhand)
            canvas.paste(offhand, heroOffSet, mask=offhand)
            font = ImageFont.truetype("helvetica.ttf", 20)
            d = ImageDraw.Draw(canvas)
            d.text((10,10), "Hero: " + heroName, fill=(0,0,0), font = font)
            d.text((10,30), "Specialization: " + heroRace.title() + " " + heroClass.title() + ".", fill=(0,0,0), font = font)
            d.text((10,50), "Health: " + str(heroCurrentHealth) + " / " + str(heroMaximumHealth), fill=(0,0,0), font = font)
            d.text((30,100), heroGold + " gold", fill=(0,0,0), font = font)
            remainingHealth = int((int(heroCurrentHealth) / int(heroMaximumHealth)) * 62)
            ActualHealthBar = healthbar.crop((0,0,remainingHealth,22))
            canvas.paste(ActualHealthBar, (10, 70), mask=ActualHealthBar)
            canvas.paste(healthbarFrame, (10, 70), mask=healthbarFrame)
            canvas.paste(goldCoin, (10, 100), mask=goldCoin)
            d.text((350,70), "Level: " + heroLevel, fill=(0,0,0), font = font)
            d.text((350,90), "EXP: " + heroEXP, fill=(0,0,0), font = font)
            d.text((350,50), "Armor: " + heroArmor, fill=(0,0,0), font = font)
            d.text((350,30), "Stamina: " + heroStam, fill=(0,0,0), font = font)
            if heroClass == "warrior":
                d.text((350,10), "Strength: " + heroStr, fill=(0,0,0), font = font)
            if heroClass == "mage":
                d.text((350,10), "Intellect: " + heroInt, fill=(0,0,0), font = font)
            if heroClass == "rogue":
                d.text((350,10), "Agility: " + heroAgi, fill=(0,0,0), font = font)
            canvas.save('hero.png', format="png")
            await client.send_file(message.channel, 'hero.png')
            os.remove("hero.png")
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA INVENTORY'):
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
            Inventory = userdata[13]
            parseItems = Inventory.split()
            output = []
            msg = "Your items:\n\n```"
            for i in parseItems:
                currentItem = i
                cursor.execute("SELECT itemName, itemDamage, itemStam, itemStr, itemInt, itemAgi, itemCrit, itemArmor FROM AzerothHeroesItems WHERE itemID = '" + str(currentItem) + "';")
                conn.commit()
                itemQuery = cursor.fetchall()
                for rows in itemQuery:
                    for cols in rows:
                        output.append("%s" % cols)
                        if len(output) >= 8:
                            itemName = output[0]
                            itemDamage = output[1]
                            itemStam = output[2]
                            itemStr = output[3]
                            itemInt = output[4]
                            itemAgi = output[5]
                            itemCrit = output[6]
                            itemArmor = output[7]
                            if len(itemName) > 0:
                                msg += itemName
                            if int(itemDamage) > 0:
                                msg += "\nDamage: " + itemDamage
                            if int(itemArmor) > 0:
                                msg += "\nArmor: " + itemArmor
                            if int(itemStam) > 0:
                                msg += "\nStamina: " + itemStam
                            if int(itemStr) > 0:
                                msg += "\nStrength: " + itemStr
                            if int(itemInt) > 0:
                                msg += "\nIntellect: " + itemInt
                            if int(itemAgi) > 0:
                                msg += "\nAgility: " + itemAgi
                            if int(itemCrit) > 0:
                                msg += "\nCritical Hit Chance: " + itemCrit
                            msg += "\n\n"
                            output.clear()
            msg += "```"
            await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA UNEQUIP'):
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
            if len(message.content.split()) >= 3:
                regexp = re.compile("unequip (.*)$")
                name = regexp.search(message.content).group(1)
                name = " ".join(name.split()).title()
                cursor.execute("SELECT itemID FROM AzerothHeroesItems WHERE itemName = '" + name + "';")
                conn.commit()
                if cursor.rowcount:
                    itemID = ""
                    itemSlot = ""
                    output = []
                    itemQuery = cursor.fetchall()
                    for rows in itemQuery:
                        for cols in rows:
                            output.append("%s" % cols)
                    itemID = output[0]
                    if itemID[:1] == "1":
                        itemSlot = "heroHelm"
                    if itemID[:1] == "2":
                        itemSlot = "heroShoulders"
                    if itemID[:1] == "3":
                        itemSlot = "heroChest"
                    if itemID[:1] == "4":
                        itemSlot = "heroGloves"
                    if itemID[:1] == "5":
                        itemSlot = "heroBelt"
                    if itemID[:1] == "6":
                        itemSlot = "heroLegs"
                    if itemID[:1] == "7":
                        itemSlot = "heroFeet"
                    if itemID[:1] == "8":
                        itemSlot = "heroMH"
                    if itemID[:1] == "9":
                        itemSlot = "heroOH"
                    execution = "SELECT " + itemSlot + " FROM AzerothHeroes WHERE userID = '" + usertoken + "';"
                    cursor.execute(execution)
                    conn.commit()
                    if cursor.rowcount:
                        secondExecution = "UPDATE AzerothHeroes SET " + itemSlot + " = " + str(0) + " WHERE userID = '" + usertoken + "';"
                        cursor.execute(secondExecution)
                        conn.commit()
                        heroMaximumHealth = int(userdata[15])
                        heroStam = int(userdata[16])
                        heroArmor = int(userdata[17])
                        heroInt = int(userdata[18])
                        heroStr = int(userdata[19])
                        heroAgi = int(userdata[20])
                        heroCrit = int(userdata[21])
                        heroLevel = int(userdata[23])
                        cursor.execute("SELECT itemName, itemDamage, itemStam, itemStr, itemInt, itemAgi, itemCrit, itemArmor FROM AzerothHeroesItems WHERE itemID = '" + itemID + "';")
                        conn.commit()
                        statQuery = cursor.fetchall()
                        for rows in statQuery:
                            for cols in rows:
                                output.append("%s" % cols)
                                if len(output) >= 9:
                                    print (output)
                                    itemName = output[1]
                                    itemDamage = output[2]
                                    itemStam = output[3]
                                    itemStr = output[4]
                                    itemInt = output[5]
                                    itemAgi = output[6]
                                    itemCrit = output[7]
                                    itemArmor = output[8]
                                    heroArmor -= int(itemArmor)
                                    heroStam -= int(itemStam)
                                    heroStr -= int(itemStr)
                                    heroInt -= int(itemInt)
                                    heroAgi -= int(itemAgi)
                                    heroCrit -= int(itemCrit)
                                    heroMaximumHealth = 30 + (20 * heroLevel) + (10 * heroStam)
                                    output.clear()
                        cursor.execute("UPDATE AzerothHeroes SET heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroStamina = '" + str(heroStam) + "', heroArmor = '" + str(heroArmor) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroAgi = '" + str(heroAgi) + "', heroCrit = '" + str(heroCrit) + "' WHERE userID = '" + usertoken + "';")
                        conn.commit()
                        await client.send_message(message.channel, "Successfully unequiped " + name)
                    else:
                        await client.send_message(message.channel, "You're not wearing that item.")
                else:
                    await client.send_message(message.channel, "We couldn't find your item. Please make sure you typed the full name correctly.")
            else:
                parseItems = [userdata[4],userdata[5],userdata[6],userdata[7],userdata[8],userdata[9],userdata[10],userdata[11],userdata[12]]
                output = []
                msg = "What would you like to unequip? Your current equipment:\n\n"
                for i in parseItems:
                    currentItem = i
                    print (currentItem)
                    cursor.execute("SELECT itemName, itemDamage, itemStam, itemStr, itemInt, itemAgi, itemCrit, itemArmor FROM AzerothHeroesItems WHERE itemID = '" + currentItem + "';")
                    conn.commit()
                    itemQuery = cursor.fetchall()
                    for rows in itemQuery:
                        for cols in rows:
                            output.append("%s" % cols)
                            if len(output) > 7:
                                itemName = output[0]
                                itemDamage = output[1]
                                itemStam = output[2]
                                itemStr = output[3]
                                itemInt = output[4]
                                itemAgi = output[5]
                                itemCrit = output[6]
                                itemArmor = output[7]
                                if len(itemName) > 0:
                                    msg += itemName
                                if int(itemDamage) > 0:
                                    msg += "\nDamage: " + itemDamage
                                if int(itemArmor) > 0:
                                    msg += "\nArmor: " + itemArmor
                                if int(itemStam) > 0:
                                    msg += "\nStamina: " + itemStam
                                if int(itemStr) > 0:
                                    msg += "\nStrength: " + itemStr
                                if int(itemInt) > 0:
                                    msg += "\nIntellect: " + itemInt
                                if int(itemAgi) > 0:
                                    msg += "\nAgility: " + itemAgi
                                if int(itemCrit) > 0:
                                    msg += "\nCritical Hit Chance: " + itemCrit
                                msg += "\n\n"
                                output.clear()
                await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA EQUIP'):
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
            Inventory = userdata[13]
            if len(message.content.split()) >= 3:
                regexp = re.compile("equip (.*)$")
                name = regexp.search(message.content).group(1)
                name = " ".join(name.split()).title()
                cursor.execute("SELECT itemID FROM AzerothHeroesItems WHERE itemName = '" + name + "';")
                conn.commit()
                if cursor.rowcount:
                    itemID = ""
                    itemSlot = ""
                    output = []
                    itemQuery = cursor.fetchall()
                    for rows in itemQuery:
                        for cols in rows:
                            output.append("%s" % cols)
                    itemID = output[0]
                    if itemID[:1] == "1":
                        itemSlot = "heroHelm"
                    if itemID[:1] == "2":
                        itemSlot = "heroShoulders"
                    if itemID[:1] == "3":
                        itemSlot = "heroChest"
                    if itemID[:1] == "4":
                        itemSlot = "heroGloves"
                    if itemID[:1] == "5":
                        itemSlot = "heroBelt"
                    if itemID[:1] == "6":
                        itemSlot = "heroLegs"
                    if itemID[:1] == "7":
                        itemSlot = "heroFeet"
                    if itemID[:1] == "8":
                        itemSlot = "heroMH"
                    if itemID[:1] == "9":
                        itemSlot = "heroOH"
                    if itemID not in Inventory:
                        await client.send_message(message.channel, "You do not own that item.")
                    else:
                        cursor.execute("SELECT " + itemSlot + " FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
                        conn.commit()
                        checkQuery = cursor.fetchall()
                        itemsList = []
                        for rows in checkQuery:
                            for cols in rows:
                                itemsList.append("%s" % cols)
                        itemSlotCheck = itemsList[0]
                        print(itemSlotCheck)
                        if int(itemSlotCheck) == 0:
                            secondExecution = "UPDATE AzerothHeroes SET " + itemSlot + " = " + str(itemID) + " WHERE userID = '" + usertoken + "';"
                            cursor.execute(secondExecution)
                            conn.commit()
                            heroMaximumHealth = int(userdata[15])
                            heroStam = int(userdata[16])
                            heroArmor = int(userdata[17])
                            heroInt = int(userdata[18])
                            heroStr = int(userdata[19])
                            heroAgi = int(userdata[20])
                            heroCrit = int(userdata[21])
                            heroLevel = int(userdata[23])
                            cursor.execute("SELECT itemName, itemDamage, itemStam, itemStr, itemInt, itemAgi, itemCrit, itemArmor FROM AzerothHeroesItems WHERE itemID = '" + itemID + "';")
                            conn.commit()
                            statQuery = cursor.fetchall()
                            for rows in statQuery:
                                for cols in rows:
                                    output.append("%s" % cols)
                                    if len(output) >= 9:
                                        print (output)
                                        itemName = output[1]
                                        itemDamage = output[2]
                                        itemStam = output[3]
                                        itemStr = output[4]
                                        itemInt = output[5]
                                        itemAgi = output[6]
                                        itemCrit = output[7]
                                        itemArmor = output[8]
                                        heroArmor += int(itemArmor)
                                        heroStam += int(itemStam)
                                        heroStr += int(itemStr)
                                        heroInt += int(itemInt)
                                        heroAgi += int(itemAgi)
                                        heroCrit += int(itemCrit)
                                        heroMaximumHealth = 30 + (20 * heroLevel) + (10 * heroStam)
                                        output.clear()
                            cursor.execute("UPDATE AzerothHeroes SET heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroStamina = '" + str(heroStam) + "', heroArmor = '" + str(heroArmor) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroAgi = '" + str(heroAgi) + "', heroCrit = '" + str(heroCrit) + "' WHERE userID = '" + usertoken + "';")
                            conn.commit()
                            await client.send_message(message.channel, "Successfully equiped " + name)
                        else:
                            await client.send_message(message.channel, "You have an item equipped in that slot. Unequip it first.")
                else:
                    await client.send_message(message.channel, "We couldn't find your item. Please make sure you typed the full name correctly.")
            else:
                msg = "What would you like to equip? Type \"Mega Inventory\" to see your items."
                await client.send_message(message.channel, msg)
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
            heroClass = userdata[3]
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
            heroGold = userdata[24]
            heroUpdateTimer = userdata[25]
            carryOverTime = userdata[26]
            heroDamage = userdata[27]
            timeNow = calendar.timegm(time.gmtime())
            if int(heroCurrentHealth) < int(heroMaximumHealth):
                timerUsed = 3600 / (int(heroMaximumHealth) * .15)
                timeSinceLast = timeNow - int(heroUpdateTimer)
                healthToRegen = math.floor(timeSinceLast/timerUsed)
                remainingTime = int(timeSinceLast) % timerUsed
                carryOverTime = float(carryOverTime) + int(remainingTime)
                while float(carryOverTime) >= timerUsed:
                    carryOverTime = float(carryOverTime) - timerUsed
                    healthToRegen += 1
                heroCurrentHealth = int(healthToRegen) + int(heroCurrentHealth)
                if int(heroCurrentHealth) >= int(heroMaximumHealth):
                    heroCurrentHealth = int(heroMaximumHealth)
                    carryOverTime = 0
            elif int(heroCurrentHealth) == int(heroMaximumHealth):
                carryOverTime = 0
            cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(heroCurrentHealth) + "', timeUpdated = '" + str(timeNow) + "', carryOverSeconds = '" + str(carryOverTime) + "' WHERE userID = '" + usertoken + "';")
            conn.commit()
            healthlost = round(random.uniform(20, 50) - (.1 * int(heroArmor)))
            heroCurrentHealth = int(heroCurrentHealth) - int(healthlost)
            if heroCurrentHealth <= 0:
                cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                conn.commit()
                msg = usertoken + ' suffered fatal damage and earned nothing. Rest up before training again!'.format(message)
                await client.send_message(message.channel, msg)
            else:
                goldGained = round(random.uniform(1, 3) * (((.05 * int(heroDamage))+(.1 * int(heroStr))) + ((.05 * int(heroDamage)) +.2 * int(heroInt)) + ((.05 * int(heroDamage)) + .15 * int(heroAgi))))
                heroGold = int(heroGold) + int(goldGained)
                doubleEXP = randint(0, 100)
                expEarned = 0
                if doubleEXP < int(heroCrit):
                    heroEXP = int(heroEXP) + 2
                    expEarned = 2
                else:
                    heroEXP = int(heroEXP) + 1
                    expEarned = 1
                expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                msg = usertoken + ' has succesfully completed training, earning ' + str(expEarned) + ' EXP, ' + str(goldGained) + ' gold and losing ' + str(healthlost) + ' health.'.format(message)
                await client.send_message(message.channel, msg)
                if int(heroEXP)>=int(expNeeded):
                    heroLevel = int(heroLevel) + 1
                    heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                    heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                    heroStam = int(heroStam) + 2
                    heroCrit = int(heroCrit) + 1
                    if heroClass == "warrior":
                        heroStr = int(heroStr) + 1
                    elif heroClass == "mage":
                        heroInt = int(heroInt) + 1
                    elif heroClass == "rogue":
                        heroAgi = int(heroAgi) + 1
                    msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                    await client.send_message(message.channel, msg)
                cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "' WHERE userID = '" + usertoken + "';")
                conn.commit()

        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    
    if usermessage.startswith('MEGA DUEL'):
        duelInit = '{0.author.mention}'.format(message)
        splitUp = message.content.split()
        duelRecip = splitUp[2]
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + duelInit + "';")
        conn.commit()
        if cursor.rowcount:
            duelInitData = []
            query = cursor.fetchall()
            for row in query:
                for col in row:
                    duelInitData.append("%s" % col)
            duelInitCurrentHealth = duelInitData[14]
            duelInitMaximumHealth = duelInitData[15]
            if int(duelInitMaximumHealth) * .20 > int(duelInitCurrentHealth):
                msg = duelInit + ", your health is too low to challenge someone to a duel! Rest up first.".format(message)
                await client.send_message(message.channel, msg)
            else:
                cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + duelRecip + "';")
                conn.commit()
                if cursor.rowcount:
                    if duelInit == duelRecip:
                        msg = "You cannot duel yourself!"
                        await client.send_message(message.channel, msg)
                    else:
                        cursor.execute("SELECT DuelRecip FROM AzerothHeroesDuels WHERE DuelRecip = '" + duelInit + "';") #Check if someone else challenged them
                        conn.commit()
                        if cursor.rowcount:
                            cursor.execute("SELECT DuelInit FROM AzerothHeroesDuels WHERE DuelRecip = '" + duelInit + "';") #get the person who challenged them
                            conn.commit()
                            duelInits = []
                            query = cursor.fetchall()
                            duelBegan = False
                            for row in query:
                                for col in row:
                                    duelInits.append("%s" % col)
                                for i in duelInits:
                                    if i == duelRecip:
                                        duelBegan = True
                                        cursor.execute("DELETE FROM AzerothHeroesDuels WHERE duelInit = '" + duelRecip + "';")
                                        conn.commit()
                                        cursor.execute("DELETE FROM AzerothHeroesDuels WHERE duelInit = '" + duelInit + "';")
                                        conn.commit()
                                        duelRecipData = []
                                        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + duelRecip + "';")
                                        conn.commit()
                                        queryRecip = cursor.fetchall()
                                        for row in queryRecip:
                                            for col in row:
                                                duelRecipData.append("%s" % col)
                                        duelInitClass = duelInitData[3]
                                        duelInitStam = duelInitData[16]
                                        duelInitArmor = duelInitData[17]
                                        duelInitInt = duelInitData[18]
                                        duelInitStr = duelInitData[19]
                                        duelInitAgi = duelInitData[20]
                                        duelInitCrit = duelInitData[21]
                                        duelInitEXP = duelInitData[22]
                                        duelInitLevel = duelInitData[23]
                                        duelInitGold = duelInitData[24]
                                        duelInitUpdateTimer = duelInitData[25]
                                        duelInitcarryOverTime = duelInitData[26]
                                        duelInitDamage = duelInitData[27]
                                        duelRecipClass = duelRecipData[3]
                                        duelRecipCurrentHealth = duelRecipData[14]
                                        duelRecipMaximumHealth = duelRecipData[15]
                                        duelRecipStam = duelRecipData[16]
                                        duelRecipArmor = duelRecipData[17]
                                        duelRecipInt = duelRecipData[18]
                                        duelRecipStr = duelRecipData[19]
                                        duelRecipAgi = duelRecipData[20]
                                        duelRecipCrit = duelRecipData[21]
                                        duelRecipEXP = duelRecipData[22]
                                        duelRecipLevel = duelRecipData[23]
                                        duelRecipGold = duelRecipData[24]
                                        duelRecipUpdateTimer = duelRecipData[25]
                                        duelRecipcarryOverTime = duelRecipData[26]
                                        duelRecipDamage = duelRecipData[27]
                                        timeNow = calendar.timegm(time.gmtime())
                                        if int(duelInitCurrentHealth) < int(duelInitMaximumHealth):
                                            duelInitTimerUsed = 3600 / (int(duelInitMaximumHealth) * .15)
                                            duelInittimeSinceLast = timeNow - int(duelInitUpdateTimer)
                                            duelInithealthToRegen = math.floor(duelInittimeSinceLast/duelInitTimerUsed)
                                            duelInitremainingTime = int(duelInittimeSinceLast) % duelInitTimerUsed
                                            duelInitcarryOverTime = float(duelInitcarryOverTime) + int(duelInitremainingTime)
                                            while float(duelInitcarryOverTime) >= duelInitTimerUsed:
                                                duelInitcarryOverTime = float(duelInitcarryOverTime) - duelInitTimerUsed
                                                duelInithealthToRegen += 1
                                            duelInitCurrentHealth = int(duelInithealthToRegen) + int(duelInitCurrentHealth)
                                            if int(duelInitCurrentHealth) >= int(duelInitMaximumHealth):
                                                duelInitCurrentHealth = int(duelInitMaximumHealth)
                                                duelInitcarryOverTime = 0
                                        elif int(duelInitCurrentHealth) == int(duelInitMaximumHealth):
                                            carryOverTime = 0
                                        cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(duelInitCurrentHealth) + "', timeUpdated = '" + str(timeNow) + "', carryOverSeconds = '" + str(duelInitcarryOverTime) + "' WHERE userID = '" + duelInit + "';")
                                        conn.commit()
                                        if int(duelRecipCurrentHealth) < int(duelRecipMaximumHealth):
                                            duelRecipTimerUsed = 3600 / (int(duelRecipMaximumHealth) * .15)
                                            duelReciptimeSinceLast = timeNow - int(duelRecipUpdateTimer)
                                            duelReciphealthToRegen = math.floor(duelReciptimeSinceLast/duelRecipTimerUsed)
                                            duelRecipremainingTime = int(duelReciptimeSinceLast) % duelRecipTimerUsed
                                            duelRecipcarryOverTime = float(duelRecipcarryOverTime) + int(duelRecipremainingTime)
                                            while float(duelRecipcarryOverTime) >= duelRecipTimerUsed:
                                                duelRecipcarryOverTime = float(duelRecipcarryOverTime) - duelRecipTimerUsed
                                                duelReciphealthToRegen += 1
                                            duelRecipCurrentHealth = int(duelReciphealthToRegen) + int(duelRecipCurrentHealth)
                                            if int(duelRecipCurrentHealth) >= int(duelRecipMaximumHealth):
                                                duelRecipCurrentHealth = int(duelRecipMaximumHealth)
                                                duelRecipcarryOverTime = 0
                                        elif int(duelRecipCurrentHealth) == int(duelRecipMaximumHealth):
                                            carryOverTime = 0
                                        cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(duelRecipCurrentHealth) + "', timeUpdated = '" + str(timeNow) + "', carryOverSeconds = '" + str(duelRecipcarryOverTime) + "' WHERE userID = '" + duelRecip + "';")
                                        conn.commit()
                                        duelInitCritRoll = randint(0, 100)
                                        duelRecipCritRoll = randint(0, 100)
                                        duelInitRoll = 0
                                        duelRecipRoll = 0
                                        while duelInitRoll == duelRecipRoll:
                                            if duelInitCritRoll < int(duelInitCrit):
                                                duelInitRoll = 1.2 * (.75 * int(duelInitLevel)) * ((1.6 * int(duelInitCurrentHealth)) + (.2 * int(duelInitStr)) + (.2 * int(duelInitInt)) + (.2 * int(duelInitAgi)) + (.1 * int(duelInitArmor)) + (.3 * (int(duelInitDamage)))) * random.uniform(1, 5)
                                            else:
                                                duelInitRoll = (.75 * int(duelInitLevel)) * ((1.6 * int(duelInitCurrentHealth)) + (.2 * int(duelInitStr)) + (.2 * int(duelInitInt)) + (.2 * int(duelInitAgi)) + (.1 * int(duelInitArmor)) + (.3 * (int(duelInitDamage)))) * random.uniform(1, 5)
                                            if duelRecipCritRoll < int(duelRecipCrit):
                                                duelRecipRoll = 1.2 * (.75 * int(duelRecipLevel)) * ((1.6 * int(duelRecipCurrentHealth)) + (.2 * int(duelRecipStr)) + (.2 * int(duelRecipInt)) + (.2 * int(duelRecipAgi)) + (.1 * int(duelRecipArmor)) + (.3 * (int(duelRecipDamage)))) * random.uniform(1, 5)
                                            else:
                                                duelRecipRoll = (.75 * int(duelRecipLevel)) * ((1.6 * int(duelRecipCurrentHealth)) + (.2 * int(duelRecipStr)) + (.2 * int(duelRecipInt)) + (.2 * int(duelRecipAgi)) + (.1 * int(duelRecipArmor)) + (.3 * (int(duelRecipDamage)))) * random.uniform(1, 5)
                                        if duelInitRoll > duelRecipRoll:
                                            duelRecipDamageDone = ""
                                            if duelRecipCritRoll < int(duelRecipCrit):
                                                duelRecipDamageDone = round((1.5 * (1.0 * int(duelRecipLevel)) * ((.4 * int(duelRecipStr)) + (.4 * int(duelRecipInt)) + (.4 * int(duelRecipAgi)) + (.5 * (int(duelRecipDamage)))) * random.uniform(2, 6)))
                                            else:
                                                duelRecipDamageDone = round(((1.0 * int(duelRecipLevel)) * ((.4 * int(duelRecipStr)) + (.4 * int(duelRecipInt)) + (.4 * int(duelRecipAgi)) + (.5 * (int(duelRecipDamage)))) * random.uniform(2, 6)))
                                            duelInitCurrentHealth = int(duelInitCurrentHealth) - int(duelRecipDamageDone)
                                            if int(duelInitCurrentHealth) < 2:
                                                duelInitCurrentHealth = "2"
                                            goldEarned = 0
                                            expEarned = 0
                                            if 0 < int(duelRecipGold) < 10:
                                                goldEarned = 1
                                                expEarned = 1
                                            elif 10 <= int(duelRecipGold):
                                                goldEarned = math.ceil(int(duelRecipGold) * .1) + 1
                                                expEarned = math.ceil(int(duelRecipEXP) * .1) + 1
                                            else:
                                                goldEarned = 0
                                            if 0 < int(duelRecipEXP) <= 4:
                                                expEarned = 1
                                            elif 4 < int(duelRecipEXP):
                                                expEarned = math.ceil(int(duelRecipEXP) * .1) + 1
                                            else:
                                                expEarned = 0 
                                            duelInitEXP = int(duelInitEXP) + int(expEarned)
                                            duelInitGold = int(duelInitGold) + int(goldEarned)
                                            duelRecipEXP = int(duelRecipEXP) - int(expEarned)
                                            duelRecipGold = int(duelRecipGold) - int(goldEarned)
                                            duelInitEXPNeeded = math.floor((round((0.04*(int(duelInitLevel)**3))+(0.8*(int(duelInitLevel)**2))+(2*int(duelInitLevel)))))
                                            duelRecipEXPNeeded = math.floor((round((0.04*((int(duelRecipLevel) - 1)**3))+(0.8*((int(duelRecipLevel) - 1)**2))+(2*int(duelRecipLevel) -1 ))))
                                            msg = 'Duel completed!\n' + duelInit + ' has earned ' + str(expEarned) + ' EXP and ' + str(goldEarned) + ' gold and lost ' + str(duelRecipDamageDone) + ' health.'.format(message)
                                            await client.send_message(message.channel, msg)
                                            msg = duelRecip + ' has lost ' + str(expEarned) + ' EXP, ' + str(goldEarned) + ' gold and all of their health. Rest up and train some more!'.format(message)
                                            await client.send_message(message.channel, msg)
                                            if int(duelInitEXP)>=int(duelInitEXPNeeded):
                                                duelInitLevel = int(duelInitLevel) + 1
                                                duelInitMaximumHealth = str(int(duelInitMaximumHealth) + 20)
                                                duelInitCurrentHealth = str(int(duelInitCurrentHealth) + 20)
                                                duelInitStam = int(duelInitStam) + 2
                                                duelInitCrit = int(duelInitCrit) + 1
                                                if duelInitClass == "warrior":
                                                    duelInitStr = int(duelInitStr) + 1
                                                elif duelInitClass == "mage":
                                                    duelInitInt = int(duelInitInt) + 1
                                                elif duelInitClass == "rogue":
                                                    duelInitAgi = int(duelInitAgi) + 1
                                                msg = duelInit + ' has leveled up! ' + duelInit + ' is now level ' + str(duelInitLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat!".format(message)
                                                await client.send_message(message.channel, msg)
                                            if int(duelRecipEXP)<int(duelRecipEXPNeeded) and int(duelRecipLevel) > 1:
                                                duelRecipLevel = int(duelRecipLevel) - 1
                                                duelRecipMaximumHealth = str(int(duelRecipMaximumHealth) - 20)
                                                duelRecipCurrentHealth = str(int(duelRecipCurrentHealth) - 20)
                                                duelRecipStam = int(duelRecipStam) - 2
                                                duelRecipCrit = int(duelRecipCrit) - 1
                                                if duelRecipClass == "warrior":
                                                    duelRecipStr = int(duelRecipStr) - 1
                                                elif duelRecipClass == "mage":
                                                    duelRecipInt = int(duelRecipInt) - 1
                                                elif duelRecipClass == "rogue":
                                                    duelRecipAgi = int(duelRecipAgi) - 1
                                                msg = duelRecip + ' has lost a level! ' + duelRecip + ' is now level ' + str(duelRecipLevel) + " and lost 2 Stamina, 1 Critical Strike Chance and 1 Main Stat!".format(message)
                                                await client.send_message(message.channel, msg)
                                            duelRecipCurrentHealth = "1"
                                            cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(duelInitStam) + "', heroCrit = '" + str(duelInitCrit) + "', heroAgi = '" + str(duelInitAgi) + "', heroInt = '" + str(duelInitInt) + "', heroStr = '" + str(duelInitStr) + "', heroMaximumHealth = '" + str(duelInitMaximumHealth) + "', heroCurrentHealth = '" + str(duelInitCurrentHealth) + "', heroGold = '" + str(duelInitGold) + "', EXP = '" + str(duelInitEXP) + "', Level = '" + str(duelInitLevel) + "' WHERE userID = '" + duelInit + "';")
                                            conn.commit()
                                            cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(duelRecipStam) + "', heroCrit = '" + str(duelRecipCrit) + "', heroAgi = '" + str(duelRecipAgi) + "', heroInt = '" + str(duelRecipInt) + "', heroStr = '" + str(duelRecipStr) + "', heroMaximumHealth = '" + str(duelRecipMaximumHealth) + "', heroCurrentHealth = '" + str(duelRecipCurrentHealth) + "', heroGold = '" + str(duelRecipGold) + "', EXP = '" + str(duelRecipEXP) + "', Level = '" + str(duelRecipLevel) + "' WHERE userID = '" + duelRecip + "';")
                                            conn.commit()
                                        elif duelInitRoll < duelRecipRoll:
                                            duelInitDamageDone = ""
                                            if duelInitCritRoll < int(duelInitCrit):
                                                duelInitDamageDone = round((1.5 * (1.0 * int(duelInitLevel)) * ((.4 * int(duelInitStr)) + (.4 * int(duelInitInt)) + (.4 * int(duelInitAgi)) + (.5 * (int(duelInitDamage)))) * random.uniform(2, 6)))
                                            else:
                                                duelInitDamageDone = round(((1.0 * int(duelInitLevel)) * ((.4 * int(duelInitStr)) + (.4 * int(duelInitInt)) + (.4 * int(duelInitAgi)) + (.5 * (int(duelInitDamage)))) * random.uniform(2, 6)))
                                            duelRecipCurrentHealth = int(duelRecipCurrentHealth) - int(duelInitDamageDone)
                                            if int(duelRecipCurrentHealth) < 2:
                                                duelRecipCurrentHealth = "2"
                                            goldEarned = 0
                                            expEarned = 0
                                            if 0 < int(duelInitGold) < 10:
                                                goldEarned = 1
                                                expEarned = 1
                                            elif 10 <= int(duelInitGold):
                                                goldEarned = math.ceil(int(duelInitGold) * .1) + 1
                                                expEarned = math.ceil(int(duelInitEXP) * .1) + 1
                                            else:
                                                goldEarned = 0
                                            if 0 < int(duelInitEXP) <= 4:
                                                expEarned = 1
                                            elif 4 < int(duelInitEXP):
                                                expEarned = math.ceil(int(duelInitEXP) * .1) + 1
                                            else:
                                                expEarned = 0 
                                            duelRecipEXP = int(duelRecipEXP) + int(expEarned)
                                            duelRecipGold = int(duelRecipGold) + int(goldEarned)
                                            duelInitEXP = int(duelInitEXP) - int(expEarned)
                                            duelInitGold = int(duelInitGold) - int(goldEarned)
                                            duelRecipEXPNeeded = math.floor((round((0.04*(int(duelRecipLevel)**3))+(0.8*(int(duelRecipLevel)**2))+(2*int(duelRecipLevel)))))
                                            duelInitEXPNeeded = math.floor((round((0.04*((int(duelInitLevel) - 1)**3))+(0.8*((int(duelInitLevel) - 1)**2))+(2*(int(duelInitLevel) -1 )))))
                                            msg = 'Duel completed!\n' + duelRecip + ' has earned ' + str(expEarned) + ' EXP, ' + str(goldEarned) + ' gold and lost ' + str(duelInitDamageDone) + ' health.'.format(message)
                                            await client.send_message(message.channel, msg)
                                            msg = duelInit + ' has lost ' + str(expEarned) + ' EXP, ' + str(goldEarned) + ' gold and lost all of their health. Rest up and train some more!'.format(message)
                                            await client.send_message(message.channel, msg)
                                            if int(duelRecipEXP)>=int(duelRecipEXPNeeded):
                                                duelRecipLevel = int(duelRecipLevel) + 1
                                                duelRecipMaximumHealth = str(int(duelRecipMaximumHealth) + 20)
                                                duelRecipCurrentHealth = str(int(duelRecipCurrentHealth) + 20)
                                                duelRecipStam = int(duelRecipStam) + 2
                                                duelRecipCrit = int(duelRecipCrit) + 1
                                                if duelRecipClass == "warrior":
                                                    duelRecipStr = int(duelRecipStr) + 1
                                                elif duelRecipClass == "mage":
                                                    duelRecipInt = int(duelRecipInt) + 1
                                                elif duelRecipClass == "rogue":
                                                    duelRecipAgi = int(duelRecipAgi) + 1
                                                msg = duelRecip + ' has leveled up! ' + duelRecip + ' is now level ' + str(duelRecipLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat!".format(message)
                                                await client.send_message(message.channel, msg)
                                            if int(duelInitEXP)<int(duelInitEXPNeeded) and int(duelInitLevel) > 1:
                                                duelInitLevel = int(duelInitLevel) - 1
                                                duelInitMaximumHealth = str(int(duelInitMaximumHealth) - 20)
                                                duelInitCurrentHealth = str(int(duelInitCurrentHealth) - 20)
                                                duelInitStam = int(duelInitStam) - 2
                                                duelInitCrit = int(duelInitCrit) - 1
                                                if duelInitClass == "warrior":
                                                    duelInitStr = int(duelInitStr) - 1
                                                elif duelInitClass == "mage":
                                                    duelInitInt = int(duelInitInt) - 1
                                                elif duelInitClass == "rogue":
                                                    duelInitAgi = int(duelInitAgi) - 1
                                                msg = duelInit + ' has lost a level! ' + duelInit + ' is now level ' + str(duelInitLevel) + " and lost 2 Stamina, 1 Critical Strike Chance and 1 Main Stat!".format(message)
                                                await client.send_message(message.channel, msg)
                                            duelInitCurrentHealth = "1"
                                            cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(duelRecipStam) + "', heroCrit = '" + str(duelRecipCrit) + "', heroAgi = '" + str(duelRecipAgi) + "', heroInt = '" + str(duelRecipInt) + "', heroStr = '" + str(duelRecipStr) + "', heroMaximumHealth = '" + str(duelRecipMaximumHealth) + "', heroCurrentHealth = '" + str(duelRecipCurrentHealth) + "', heroGold = '" + str(duelRecipGold) + "', EXP = '" + str(duelRecipEXP) + "', Level = '" + str(duelRecipLevel) + "' WHERE userID = '" + duelRecip + "';")
                                            conn.commit()
                                            cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(duelInitStam) + "', heroCrit = '" + str(duelInitCrit) + "', heroAgi = '" + str(duelInitAgi) + "', heroInt = '" + str(duelInitInt) + "', heroStr = '" + str(duelInitStr) + "', heroMaximumHealth = '" + str(duelInitMaximumHealth) + "', heroCurrentHealth = '" + str(duelInitCurrentHealth) + "', heroGold = '" + str(duelInitGold) + "', EXP = '" + str(duelInitEXP) + "', Level = '" + str(duelInitLevel) + "' WHERE userID = '" + duelInit + "';")
                                            conn.commit()
                                if duelBegan == False:
                                    cursor.execute("SELECT DuelInit FROM AzerothHeroesDuels WHERE DuelInit = '" + duelInit + "';") #Check if user has a duel request
                                    conn.commit()
                                    if cursor.rowcount:
                                        cursor.execute("UPDATE AzerothHeroesDuels SET duelRecip = '" + duelRecip + "' where duelInit = '" + duelInit + "';")
                                        conn.commit()
                                        msg = duelInit + " has challenged " + duelRecip + " to a duel! Challenge them back to duel.".format(message)
                                        await client.send_message(message.channel, msg)
                                    else:
                                        cursor.execute("INSERT INTO AzerothHeroesDuels (DuelInit, DuelRecip) VALUES ('" + duelInit + "','" + duelRecip + "');")
                                        conn.commit()
                                        msg = duelInit + " has challenged " + duelRecip + " to a duel! Challenge them back to duel.".format(message)
                                        await client.send_message(message.channel, msg)
                        else:
                            cursor.execute("SELECT DuelInit FROM AzerothHeroesDuels WHERE DuelInit = '" + duelInit + "';") #Check if user has a duel request
                            conn.commit()
                            if cursor.rowcount:
                                cursor.execute("UPDATE AzerothHeroesDuels SET duelRecip = '" + duelRecip + "' where duelInit = '" + duelInit + "';")
                                conn.commit()
                                msg = duelInit + " has challenged " + duelRecip + " to a duel! Challenge them back to duel.".format(message)
                                await client.send_message(message.channel, msg)
                            else:
                                cursor.execute("INSERT INTO AzerothHeroesDuels (DuelInit, DuelRecip) VALUES ('" + duelInit + "','" + duelRecip + "');")
                                conn.commit()
                                msg = duelInit + " has challenged " + duelRecip + " to a duel! Challenge them back to duel.".format(message)
                                await client.send_message(message.channel, msg)
                else:
                    msg = 'The user you challenged does not have a character.'.format(message)
                    await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA SHOP'):
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
        heroClass = userdata[3]
        cursor.execute("SELECT itemName, itemID, itemCost FROM AzerothHeroesShop WHERE itemClass = '" + heroClass + "' OR `itemClass` = 'all';")
        conn.commit()
        itemQuery = cursor.fetchall()
        itemData = []
        msg = "```Welcome to my shop. Broswe my wares!\n\n"
        for row in itemQuery:
            for col in row:
                itemData.append("%s" % col)
            itemName = itemData[0]
            itemID = itemData[1]
            itemCost = itemData[2]
            cursor.execute("SELECT itemDamage, itemStam, itemStr, itemInt, itemAgi, itemCrit, itemArmor FROM AzerothHeroesItems WHERE itemID = '" + itemID + "';")
            conn.commit()
            itemStats = cursor.fetchall()
            if cursor.rowcount:
                for rows in itemStats:
                    for cols in rows:
                        itemData.append("%s" % cols)
                        if len(itemData) >= 10:
                            itemDamage = itemData[3]
                            itemStam = itemData[4]
                            itemStr = itemData[5]
                            itemInt = itemData[6]
                            itemAgi = itemData[7]
                            itemCrit = itemData[8]
                            itemArmor = itemData[9]
                            if len(itemName) > 0:
                                msg += itemName
                            if int(itemDamage) > 0:
                                msg += "\nDamage: " + itemDamage
                            if int(itemArmor) > 0:
                                msg += "\nArmor: " + itemArmor
                            if int(itemStam) > 0:
                                msg += "\nStamina: " + itemStam
                            if int(itemStr) > 0:
                                msg += "\nStrength: " + itemStr
                            if int(itemInt) > 0:
                                msg += "\nIntellect: " + itemInt
                            if int(itemAgi) > 0:
                                msg += "\nAgility: " + itemAgi
                            if int(itemCrit) > 0:
                                msg += "\nCritical Hit Chance: " + itemCrit
                            msg += "\nCost: " + itemCost + " gold.\n\n"
                            itemData.clear()
            else:
                msg += itemName + "\nCost: " + itemCost + " gold.\n\n"
        msg += "Don\'t get any funny ideas. You break it, you buy it!```"
        await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA BUY'):
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
            regexp = re.compile("buy (.*)$")
            name = regexp.search(message.content).group(1)
            name = " ".join(name.split()).title()
            heroClass = userdata[3]
            heroGold = userdata[24]
            Inventory = userdata[13]
            cursor.execute("SELECT * FROM AzerothHeroesShop WHERE itemName = '" + name + "';")
            conn.commit()
            if cursor.rowcount:
                itemQuery = cursor.fetchall()
                itemdata = []
                for row in itemQuery:
                    for col in row:
                        itemdata.append("%s" % col)
                itemCost = itemdata[1]
                itemID = itemdata[2]
                itemClass = itemdata[3]
                if str(itemClass) != str(heroClass) and str(itemClass) != "all":
                    msg = usertoken + ', that item is not sold to your class. Type \'Mega Shop\' to see what you can buy.'.format(message)
                    await client.send_message(message.channel, msg)
                else:
                    if int(itemCost) > int(heroGold):
                        msg = usertoken + ', you cannot afford that item!'.format(message)
                        await client.send_message(message.channel, msg)
                    else:
                        Inventory = Inventory + " " + itemID
                        heroGold = int(heroGold) - int(itemCost)
                        cursor.execute("UPDATE AzerothHeroes SET heroGold = '" + str(heroGold) + "', heroInventory = '" + str(Inventory) + "' WHERE userID = '" + usertoken + "';")
                        conn.commit()
                        msg = usertoken + ', you\'ve succesfully bought ' + name + '.'.format(message)
                        await client.send_message(message.channel, msg)
            else:
                msg = usertoken + ', could not find the item. Make sure you spelled the name correctly.'.format(message)
                await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA DEADMINES'):
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
            heroClass = userdata[3]
            heroInventory = userdata[13]
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
            heroGold = userdata[24]
            heroUpdateTimer = userdata[25]
            carryOverTime = userdata[26]
            heroDamage = userdata[27]
            heroLockout = userdata[28]
            heroRunning = userdata[29]
            heroMH = userdata[11]
            if heroRunning == "yes":
                msg = await client.send_message(message.channel, usertoken + ', you\'re already running a dungeon!'.format(message))
            else:
                timeNow = calendar.timegm(time.gmtime())
                if int(heroCurrentHealth) < int(heroMaximumHealth):
                    timerUsed = 3600 / (int(heroMaximumHealth) * .15)
                    timeSinceLast = timeNow - int(heroUpdateTimer)
                    healthToRegen = math.floor(timeSinceLast/timerUsed)
                    remainingTime = int(timeSinceLast) % timerUsed
                    carryOverTime = float(carryOverTime) + int(remainingTime)
                    while float(carryOverTime) >= timerUsed:
                        carryOverTime = float(carryOverTime) - timerUsed
                        healthToRegen += 1
                    heroCurrentHealth = int(healthToRegen) + int(heroCurrentHealth)
                    if int(heroCurrentHealth) >= int(heroMaximumHealth):
                        heroCurrentHealth = int(heroMaximumHealth)
                        carryOverTime = 0
                elif int(heroCurrentHealth) == int(heroMaximumHealth):
                    carryOverTime = 0
                cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(heroCurrentHealth) + "', timeUpdated = '" + str(timeNow) + "', carryOverSeconds = '" + str(carryOverTime) + "', currentlyRunning = 'yes' WHERE userID = '" + usertoken + "';")
                conn.commit()
                msg = await client.send_message(message.channel, '```You\'ve reached the entrance to The Deadmines, do you wish to enter or flee?```'.format(message))
                await client.add_reaction(msg, '🏃')
                await client.add_reaction(msg, '⚔')
                res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                if "o->DM" not in heroInventory:
                    await client.send_message(message.channel, '```You try to open the door, but no matter how hard you try, the door will not budge. It\'s locked, and the key is no where in sight.\nOut of the corner of your eye, you catch glipse of a merchant, sulking around.\nHe barks, \"Trying to get in there are we? Not without this here key. You want it? Pay up.\"\nYou can view what the merchant sells by typing \'Mega shop\'. ```'.format(message))
                else:
                    try:
                        userReaction = '{0.reaction.emoji}'.format(res)
                        if userReaction == "⚔" and heroLockout == "AAAAAAA":
                            msg = await client.send_message(message.channel, '```You\'re now face to face with Rhahk\'Zor, the mining supervisor.\nDo you wish to engage in combat or flee, and live another day?```'.format(message))
                            await client.add_reaction(msg, '🏃')
                            await client.add_reaction(msg, '⚔')
                            res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                            try: #RhahkZor
                                userReactionRH = '{0.reaction.emoji}'.format(res)
                                if userReactionRH == "⚔":
                                    heroRoll = round(random.uniform(150,180) - ((1 * int(heroLevel)) * ((.2 * int(heroStr)) + (.35 * int(heroInt)) + (.2 * int(heroAgi)) + (.1 * int(heroArmor)) + (.3 * (int(heroDamage)))) * random.uniform(1,2)))
                                    heroCurrentHealth = int(heroCurrentHealth) - int(heroRoll)
                                    if heroCurrentHealth <= 0:
                                        cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                                        conn.commit()
                                        msg = "```Rhahk\'Zor strikes you down with his hammer, cackling as he scoffs \"Is this best heroes can do? Hah!\".\nWith that, your run ends. Rest up before trying again!```".format(message)
                                        await client.send_message(message.channel, msg)
                                    else:
                                        goldGained = randint(10, 20)
                                        heroGold = int(heroGold) + int(goldGained)
                                        expEarned = 3
                                        expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                                        if int(heroEXP)>=int(expNeeded):
                                            heroLevel = int(heroLevel) + 1
                                            heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                                            heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                                            heroStam = int(heroStam) + 2
                                            heroCrit = int(heroCrit) + 1
                                            if heroClass == "warrior":
                                                heroStr = int(heroStr) + 1
                                            elif heroClass == "mage":
                                                heroInt = int(heroInt) + 1
                                            elif heroClass == "rogue":
                                                heroAgi = int(heroAgi) + 1
                                            msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                                            await client.send_message(message.channel, msg)
                                        ifLootDropped = randint(1, 100)
                                        defeat = "```After an intense fight, Rhahk\'zor goes down! He mutters, \"VanCleef not gonna be happy, when he find out!\"\nYou earned " + str(expEarned) + " exp and " + str(goldGained) + " gold."
                                        if ifLootDropped < 16:
                                            if heroClass == "warrior":
                                                heroInventory += " 74"
                                                defeat += "\nLoot dropped! You got Protector Sabatons!```"
                                            elif heroClass == "mage":
                                                heroInventory += " 75"
                                                defeat += "\nLoot dropped! You got Shadow Council Slippers!```"
                                            elif heroClass == "rogue":
                                                heroInventory += " 76"
                                                defeat += "\nLoot dropped! You got Darkened Defias Boots!```"
                                        else:
                                            defeat += "```"
                                        await client.send_message(message.channel, defeat)
                                        print (heroInventory)
                                        cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "', DMLockout = 'XAAAAAA', heroInventory = '" + str(heroInventory) + "' WHERE userID = '" + usertoken + "';")
                                        conn.commit()
                                        msg = await client.send_message(message.channel,"```After dealing with a some lackeys, you look up to a giant mechanical shredder.\n\"Keep it quick, kid, I ain't got all day!\"\nYou now face Sneed, the lumber supervisor. Do you wish to engage, or flee, and live another day?```".format(message))
                                        await client.add_reaction(msg, '🏃')
                                        await client.add_reaction(msg, '⚔')
                                        res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                                        try: #Sneed
                                            userReactionSN = '{0.reaction.emoji}'.format(res)
                                            if userReactionSN == "⚔":
                                                heroRoll = round(random.uniform(170,200) - ((1 * int(heroLevel)) * ((.2 * int(heroStr)) + (.35 * int(heroInt)) + (.2 * int(heroAgi)) + (.1 * int(heroArmor)) + (.3 * (int(heroDamage)))) * random.uniform(1,2)))
                                                heroCurrentHealth = int(heroCurrentHealth) - int(heroRoll)
                                                if heroCurrentHealth <= 0:
                                                    cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                                                    conn.commit()
                                                    msg = "```As Sneed cuts you down, you hear him guffaw, \"Who said you couldn't mix business with pleasure? Now get out of my sight!\"!\nWith that, your run ends. Rest up before trying again!```".format(message)
                                                    await client.send_message(message.channel, msg)
                                                else:
                                                    goldGained = randint(15, 25)
                                                    heroGold = int(heroGold) + int(goldGained)
                                                    expEarned = 3
                                                    expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                                                    if int(heroEXP)>=int(expNeeded):
                                                        heroLevel = int(heroLevel) + 1
                                                        heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                                                        heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                                                        heroStam = int(heroStam) + 2
                                                        heroCrit = int(heroCrit) + 1
                                                        if heroClass == "warrior":
                                                            heroStr = int(heroStr) + 1
                                                        elif heroClass == "mage":
                                                            heroInt = int(heroInt) + 1
                                                        elif heroClass == "rogue":
                                                            heroAgi = int(heroAgi) + 1
                                                        msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                                                        await client.send_message(message.channel, msg)
                                                    ifLootDropped = randint(1, 100)
                                                    defeat = "```With all the might you can muster, Sneed and his shredder goes down. Sneed squirms as he says, \"VanCleef can\'t replace me! I'm Sneed! The... \" and with those words, Sneed dies.\nYou earned " + str(expEarned) + " exp and " + str(goldGained) + " gold."
                                                    if ifLootDropped < 16:
                                                        if heroClass == "warrior":
                                                            heroInventory += " 64"
                                                            defeat += "\nLoot dropped! You got Protector Legguard!```"
                                                        elif heroClass == "mage":
                                                            heroInventory += " 65"
                                                            defeat += "\nLoot dropped! You got Shadow Council Pants!```"
                                                        elif heroClass == "rogue":
                                                            heroInventory += " 66"
                                                            defeat += "\nLoot dropped! You got Darkened Defias Pants!```"
                                                    else:
                                                        defeat += "```"
                                                    await client.send_message(message.channel, defeat)
                                                    print (heroInventory)
                                                    cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "', DMLockout = 'XXAAAAA', heroInventory = '" + str(heroInventory) + "' WHERE userID = '" + usertoken + "';")
                                                    conn.commit()
                                                    msg = await client.send_message(message.channel,"```As you exit the lumberyard, you walk into a massive room, with lava pouring from the ceiling. You can hear a goblin yelling, \"What am I paying you for! Oh, wait, I'm not paying you. Get back to making VanCleef\'s weapons, or you\'re going to regret it!\"\nAs you walk down the spiraling ramp, you happen upon the blacksmith supervisor, Gilnid. Will you engage him? Or flee, and live another day?```".format(message))
                                                    await client.add_reaction(msg, '🏃')
                                                    await client.add_reaction(msg, '⚔')
                                                    res = await client.wait_for_reaction(['🏃', '⚔', '🔴'], user=message.author, message=msg, timeout = 10)
                                                    try: #Gilnid
                                                        userReactionGI = '{0.reaction.emoji}'.format(res)
                                                        if userReactionGI == "⚔":
                                                            heroRoll = round(random.uniform(190,220) - ((1 * int(heroLevel)) * ((.2 * int(heroStr)) + (.35 * int(heroInt)) + (.2 * int(heroAgi)) + (.1 * int(heroArmor)) + (.3 * (int(heroDamage)))) * random.uniform(1,2)))
                                                            heroCurrentHealth = int(heroCurrentHealth) - int(heroRoll)
                                                            if heroCurrentHealth <= 0:
                                                                cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                                                                conn.commit()
                                                                msg = "```Overwhelmed by machines, Gilnid shoots you down as he sneers, \"You\'re of no threat to the brotherhood! Don\'t ever disturb my work again.\"\nWith that, your run ends. Rest up before trying again!```".format(message)
                                                                await client.send_message(message.channel, msg)
                                                            else:
                                                                goldGained = randint(17, 29)
                                                                heroGold = int(heroGold) + int(goldGained)
                                                                expEarned = 4
                                                                expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                                                                if int(heroEXP)>=int(expNeeded):
                                                                    heroLevel = int(heroLevel) + 1
                                                                    heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                                                                    heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                                                                    heroStam = int(heroStam) + 2
                                                                    heroCrit = int(heroCrit) + 1
                                                                    if heroClass == "warrior":
                                                                        heroStr = int(heroStr) + 1
                                                                    elif heroClass == "mage":
                                                                        heroInt = int(heroInt) + 1
                                                                    elif heroClass == "rogue":
                                                                        heroAgi = int(heroAgi) + 1
                                                                    msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                                                                    await client.send_message(message.channel, msg)
                                                                ifLootDropped = randint(1, 100)
                                                                defeat = "```Putting up the best he can, Gilnid finally falls as he squaks. \"You\'ll never get to VanCleef! Never! Haha...\" and dies.\nYou earned " + str(expEarned) + " exp and " + str(goldGained) + " gold."
                                                                if ifLootDropped < 16:
                                                                    if heroClass == "warrior":
                                                                        heroInventory += " 54"
                                                                        defeat += "\nLoot dropped! You got Protector Belt!```"
                                                                    elif heroClass == "mage":
                                                                        heroInventory += " 55"
                                                                        defeat += "\nLoot dropped! You got Shadow Council Belt!```"
                                                                    elif heroClass == "rogue":
                                                                        heroInventory += " 56"
                                                                        defeat += "\nLoot dropped! You got Darkened Defias Buckle!```"
                                                                else:
                                                                    defeat += "```"
                                                                await client.send_message(message.channel, defeat)
                                                                print (heroInventory)
                                                                cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "', DMLockout = 'XXAAAAA', heroInventory = '" + str(heroInventory) + "' WHERE userID = '" + usertoken + "';")
                                                                conn.commit()
                                                                msg = await client.send_message(message.channel,"```Exiting the forgery, you walk onto a dock. In the distance, you see a ship. With a piercing shriek, you hear a dark voice yell \"We\'re under attack! A vast, ye swabs! Repel the invaders!\" Now standing at the ramp to the boat, you\'re greeted by a massive Tauren.\nYou\'re now facing Mr.Smite, VanCleef\'s deckhand. Will you engage combat, or flee, and live another day?```".format(message))
                                                                await client.add_reaction(msg, '🏃')
                                                                await client.add_reaction(msg, '⚔')
                                                                res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                                                                try: #Smite
                                                                    userReactionSM = '{0.reaction.emoji}'.format(res)
                                                                    if userReactionSM == "⚔":
                                                                        heroRoll = round(random.uniform(210,240) - ((1 * int(heroLevel)) * ((.2 * int(heroStr)) + (.35 * int(heroInt)) + (.2 * int(heroAgi)) + (.1 * int(heroArmor)) + (.3 * (int(heroDamage)))) * random.uniform(1,2)))
                                                                        heroCurrentHealth = int(heroCurrentHealth) - int(heroRoll)
                                                                        if heroCurrentHealth <= 0:
                                                                            cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                                                                            conn.commit()
                                                                            msg = "```Beaten by Smite\'s incredible arsenal, he simply looks back and spits on you as he walks back on board.\nWith that, your run ends. Rest up before trying again!```".format(message)
                                                                            await client.send_message(message.channel, msg)
                                                                        else:
                                                                            goldGained = randint(20, 32)
                                                                            heroGold = int(heroGold) + int(goldGained)
                                                                            expEarned = 4
                                                                            expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                                                                            if int(heroEXP)>=int(expNeeded):
                                                                                heroLevel = int(heroLevel) + 1
                                                                                heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                                                                                heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                                                                                heroStam = int(heroStam) + 2
                                                                                heroCrit = int(heroCrit) + 1
                                                                                if heroClass == "warrior":
                                                                                    heroStr = int(heroStr) + 1
                                                                                elif heroClass == "mage":
                                                                                    heroInt = int(heroInt) + 1
                                                                                elif heroClass == "rogue":
                                                                                    heroAgi = int(heroAgi) + 1
                                                                                msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                                                                                await client.send_message(message.channel, msg)
                                                                            ifLootDropped = randint(1, 100)
                                                                            defeat = "```As Mr.Smite duels you to his final breath, he mutters, \"You landlubbers are tougher than i thought. I should have improvised.\" He collapses to the floor, and the way to the dock is cleared.\nYou earned " + str(expEarned) + " exp and " + str(goldGained) + " gold."
                                                                            if ifLootDropped < 16:
                                                                                if heroClass == "warrior":
                                                                                    heroInventory += " 34"
                                                                                    defeat += "\nLoot dropped! You got Protector Armor!```"
                                                                                elif heroClass == "mage":
                                                                                    heroInventory += " 35"
                                                                                    defeat += "\nLoot dropped! You got Shadow Council Robe!```"
                                                                                elif heroClass == "rogue":
                                                                                    heroInventory += " 36"
                                                                                    defeat += "\nLoot dropped! You got Darkened Defias Jenkin!```"
                                                                            else:
                                                                                defeat += "```"
                                                                            await client.send_message(message.channel, defeat)
                                                                            print (heroInventory)
                                                                            cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "', DMLockout = 'XXAAAAA', heroInventory = '" + str(heroInventory) + "' WHERE userID = '" + usertoken + "';")
                                                                            conn.commit()
                                                                            msg = await client.send_message(message.channel,"```Walking on board, you\'re quickly greeted with the sound of rushing footsteps. You hear a murloc gurgling in the distance. Could it be? Cookie and his gang have caught up to you. \"Mrglgrglglrlgl\" he says, with his mallet in hand.\nYou now face Cookie, the chef of the Brotherhood. Will you fight? Or flee, and live another day?```".format(message))
                                                                            await client.add_reaction(msg, '🏃')
                                                                            await client.add_reaction(msg, '⚔')
                                                                            res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                                                                            try: #Cookie
                                                                                userReactionCO = '{0.reaction.emoji}'.format(res)
                                                                                if userReactionCO == "⚔":
                                                                                    heroRoll = round(random.uniform(200,240) - ((1 * int(heroLevel)) * ((.2 * int(heroStr)) + (.35 * int(heroInt)) + (.2 * int(heroAgi)) + (.1 * int(heroArmor)) + (.3 * (int(heroDamage)))) * random.uniform(1,2)))
                                                                                    heroCurrentHealth = int(heroCurrentHealth) - int(heroRoll)
                                                                                    if heroCurrentHealth <= 0:
                                                                                        cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                                                                                        conn.commit()
                                                                                        msg = "```As cookie beats you with his rolling pin, he leaves as a gang of bandits come and finish you off.\nWith that, your run ends. Rest up before trying again!```".format(message)
                                                                                        await client.send_message(message.channel, msg)
                                                                                    else:
                                                                                        goldGained = randint(30, 45)
                                                                                        heroGold = int(heroGold) + int(goldGained)
                                                                                        expEarned = 4
                                                                                        expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                                                                                        if int(heroEXP)>=int(expNeeded):
                                                                                            heroLevel = int(heroLevel) + 1
                                                                                            heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                                                                                            heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                                                                                            heroStam = int(heroStam) + 2
                                                                                            heroCrit = int(heroCrit) + 1
                                                                                            if heroClass == "warrior":
                                                                                                heroStr = int(heroStr) + 1
                                                                                            elif heroClass == "mage":
                                                                                                heroInt = int(heroInt) + 1
                                                                                            elif heroClass == "rogue":
                                                                                                heroAgi = int(heroAgi) + 1
                                                                                            msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                                                                                            await client.send_message(message.channel, msg)
                                                                                        ifLootDropped = randint(1, 100)
                                                                                        defeat = "```As you defeat Cookie, you see a band of thugs run towards you. You hide and avoid them, waiting for the area to clear up.\nYou earned " + str(expEarned) + " exp and " + str(goldGained) + " gold."
                                                                                        if ifLootDropped < 16:
                                                                                            if heroClass == "warrior":
                                                                                                heroInventory += " 34"
                                                                                                defeat += "\nLoot dropped! You got Protector Armor!```"
                                                                                            elif heroClass == "mage":
                                                                                                heroInventory += " 35"
                                                                                                defeat += "\nLoot dropped! You got Shadow Council Robe!```"
                                                                                            elif heroClass == "rogue":
                                                                                                heroInventory += " 36"
                                                                                                defeat += "\nLoot dropped! You got Darkened Defias Jenkin!```"
                                                                                        else:
                                                                                            defeat += "```"
                                                                                        await client.send_message(message.channel, defeat)
                                                                                        print (heroInventory)
                                                                                        cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "', DMLockout = 'XXAAAAA', heroInventory = '" + str(heroInventory) + "' WHERE userID = '" + usertoken + "';")
                                                                                        conn.commit()
                                                                                        msg = await client.send_message(message.channel,"```As you clear the path to the top of the ship, you hear a parrot squak, \"Intruders! Intruders! RAAWK!\" A goblin mutters as he walks over to you, now at the top of the ship. \"You dare step foot on my ship? I\'ll have you skinned!\" The goblin pulls out his spear and charges.\nYou now face Greenskin, captain of the Deadmines. Will you fight? Or flee, and live another day?```".format(message))
                                                                                        await client.add_reaction(msg, '🏃')
                                                                                        await client.add_reaction(msg, '⚔')
                                                                                        res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                                                                                        try: #Captain Greenskin
                                                                                            userReactionGR = '{0.reaction.emoji}'.format(res)
                                                                                            if userReactionGR == "⚔":
                                                                                                heroRoll = round(random.uniform(220,260) - ((1 * int(heroLevel)) * ((.2 * int(heroStr)) + (.35 * int(heroInt)) + (.2 * int(heroAgi)) + (.1 * int(heroArmor)) + (.3 * (int(heroDamage)))) * random.uniform(1,2)))
                                                                                                heroCurrentHealth = int(heroCurrentHealth) - int(heroRoll)
                                                                                                if heroCurrentHealth <= 0:
                                                                                                    cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                                                                                                    conn.commit()
                                                                                                    msg = "```Greenskin skewers you with his spear, snickering to himself. \"What did ye hope to accomplish against the cap\'n? Win? Pathetic! To the locket with you!\"\nWith that, your run ends. Rest up before trying again!```".format(message)
                                                                                                    await client.send_message(message.channel, msg)
                                                                                                else:
                                                                                                    goldGained = randint(30, 45)
                                                                                                    heroGold = int(heroGold) + int(goldGained)
                                                                                                    expEarned = 4
                                                                                                    expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                                                                                                    if int(heroEXP)>=int(expNeeded):
                                                                                                        heroLevel = int(heroLevel) + 1
                                                                                                        heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                                                                                                        heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                                                                                                        heroStam = int(heroStam) + 2
                                                                                                        heroCrit = int(heroCrit) + 1
                                                                                                        if heroClass == "warrior":
                                                                                                            heroStr = int(heroStr) + 1
                                                                                                        elif heroClass == "mage":
                                                                                                            heroInt = int(heroInt) + 1
                                                                                                        elif heroClass == "rogue":
                                                                                                            heroAgi = int(heroAgi) + 1
                                                                                                        msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                                                                                                        await client.send_message(message.channel, msg)
                                                                                                    ifLootDropped = randint(1, 100)
                                                                                                    defeat = "```As you strike down Captain Greenskin, he yells \"VanCleef! They, they have... arrived\"\nYou earned " + str(expEarned) + " exp and " + str(goldGained) + " gold."
                                                                                                    if ifLootDropped < 16:
                                                                                                        if heroClass == "warrior":
                                                                                                            heroInventory += " 34"
                                                                                                            defeat += "\nLoot dropped! You got Protector Armor!```"
                                                                                                        elif heroClass == "mage":
                                                                                                            heroInventory += " 35"
                                                                                                            defeat += "\nLoot dropped! You got Shadow Council Robe!```"
                                                                                                        elif heroClass == "rogue":
                                                                                                            heroInventory += " 36"
                                                                                                            defeat += "\nLoot dropped! You got Darkened Defias Jenkin!```"
                                                                                                    else:
                                                                                                        defeat += "```"
                                                                                                    await client.send_message(message.channel, defeat)
                                                                                                    print (heroInventory)
                                                                                                    cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "', DMLockout = 'XXAAAAA', heroInventory = '" + str(heroInventory) + "' WHERE userID = '" + usertoken + "';")
                                                                                                    conn.commit()
                                                                                                    if heroMH == "0":
                                                                                                        msg = await client.send_message(message.channel,"```Finally at the very top of the ship, you see a shadowy figure step out of the hull. \"None may challenge the brotherhood, least of all you. You won\'t stop this opperation, lest of all the Brotherhood. None will defeat the brotherhood! Forgot your weapon, huh? Time to die!\"\nYou now face VanCleef, leader of the Defias Brotherhood. Will you fight and prevail? Or flee, and live another day?```".format(message))
                                                                                                        await client.add_reaction(msg, '🏃')
                                                                                                        await client.add_reaction(msg, '⚔')
                                                                                                        res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                                                                                                    else:
                                                                                                        msg = await client.send_message(message.channel,"```Finally at the very top of the ship, you see a shadowy figure step out of the hull. \"None may challenge the brotherhood, least of all you. You won\'t stop this opperation, lest of all the Brotherhood. None will defeat the brotherhood! You have the audacity to board this boat with a weapon? Thugs, get him!\"\nYou now face VanCleef, leader of the Defias Brotherhood. Will you fight and prevail? Or flee, and live another day?```".format(message))
                                                                                                        await client.add_reaction(msg, '🏃')
                                                                                                        await client.add_reaction(msg, '⚔')
                                                                                                        res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                                                                                                    try: #VanCleef
                                                                                                        userReactionGR = '{0.reaction.emoji}'.format(res)
                                                                                                        if userReactionGR == "⚔":
                                                                                                            heroRoll = round(random.uniform(260,300) - ((1 * int(heroLevel)) * ((.2 * int(heroStr)) + (.35 * int(heroInt)) + (.2 * int(heroAgi)) + (.1 * int(heroArmor)) + (.3 * (int(heroDamage)))) * random.uniform(1,2)))
                                                                                                            heroCurrentHealth = int(heroCurrentHealth) - int(heroRoll)
                                                                                                            if heroCurrentHealth <= 0:
                                                                                                                cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                                                                                                                conn.commit()
                                                                                                                msg = "```VanCleef mercilessly cuts you down with his sabers. He turns around and smirks as he says, \"You don't have the strength to challenge me, lest of all the brotherhood!\"\nWith that, your run ends. Rest up before trying again!```".format(message)
                                                                                                                await client.send_message(message.channel, msg)
                                                                                                            else:
                                                                                                                goldGained = randint(30, 45)
                                                                                                                heroGold = int(heroGold) + int(goldGained)
                                                                                                                expEarned = 4
                                                                                                                expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                                                                                                                if int(heroEXP)>=int(expNeeded):
                                                                                                                    heroLevel = int(heroLevel) + 1
                                                                                                                    heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                                                                                                                    heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                                                                                                                    heroStam = int(heroStam) + 2
                                                                                                                    heroCrit = int(heroCrit) + 1
                                                                                                                    if heroClass == "warrior":
                                                                                                                        heroStr = int(heroStr) + 1
                                                                                                                    elif heroClass == "mage":
                                                                                                                        heroInt = int(heroInt) + 1
                                                                                                                    elif heroClass == "rogue":
                                                                                                                        heroAgi = int(heroAgi) + 1
                                                                                                                    msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                                                                                                                    await client.send_message(message.channel, msg)
                                                                                                                ifLootDropped = randint(1, 100)
                                                                                                                defeat = "```After an intense duel, VanCleef kneels down, dropping his weapons.\n\"My death means nothing. This brotherhood runs deeper than you think. Strike me down, if you will, but know that your actions change nothing!\"\nYou earned " + str(expEarned) + " exp and " + str(goldGained) + " gold."
                                                                                                                if heroMH == "0":
                                                                                                                    defeat += "\nYou find a key near VanCleef\'. On it the words read, \"The Key to Karazhan\""
                                                                                                                if ifLootDropped < 16:
                                                                                                                    if heroClass == "warrior":
                                                                                                                        heroInventory += " 34"
                                                                                                                        defeat += "\nLoot dropped! You got Protector Armor!```"
                                                                                                                    elif heroClass == "mage":
                                                                                                                        heroInventory += " 35"
                                                                                                                        defeat += "\nLoot dropped! You got Shadow Council Robe!```"
                                                                                                                    elif heroClass == "rogue":
                                                                                                                        heroInventory += " 36"
                                                                                                                        defeat += "\nLoot dropped! You got Darkened Defias Jenkin!```"
                                                                                                                else:
                                                                                                                    defeat += "```"
                                                                                                                await client.send_message(message.channel, defeat)
                                                                                                                print (heroInventory)
                                                                                                                cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "', DMLockout = 'XXAAAAA', heroInventory = '" + str(heroInventory) + "' WHERE userID = '" + usertoken + "';")
                                                                                                                conn.commit()
                                                                                                                msg = await client.send_message(message.channel,"```VanCleef now lays in front of you, bloodied and bruised. He\'s too tired to fight, and has given up. The choice to make is yours.\nDo you kill VanCleef, or spare him?```".format(message))
                                                                                                                await client.add_reaction(msg, '🤝')
                                                                                                                await client.add_reaction(msg, '⚔')
                                                                                                                res = await client.wait_for_reaction(['🤝', '⚔'], user=message.author, message=msg, timeout = 10)
                                                                                                                try: #VanCleef Ending
                                                                                                                    userReactionGR = '{0.reaction.emoji}'.format(res)
                                                                                                                    if userReactionGR == "🤝":
                                                                                                                            expEarned = 4
                                                                                                                            expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                                                                                                                            if int(heroEXP)>=int(expNeeded):
                                                                                                                                heroLevel = int(heroLevel) + 1
                                                                                                                                heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                                                                                                                                heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                                                                                                                                heroStam = int(heroStam) + 2
                                                                                                                                heroCrit = int(heroCrit) + 1
                                                                                                                                if heroClass == "warrior":
                                                                                                                                    heroStr = int(heroStr) + 1
                                                                                                                                elif heroClass == "mage":
                                                                                                                                    heroInt = int(heroInt) + 1
                                                                                                                                elif heroClass == "rogue":
                                                                                                                                    heroAgi = int(heroAgi) + 1
                                                                                                                                msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                                                                                                                                await client.send_message(message.channel, msg)
                                                                                                                            ifLootDropped = randint(1, 100)
                                                                                                                            defeat = "```After an intense duel, VanCleef kneels down, dropping his weapons.\n\"My death means nothing. This brotherhood runs deeper than you think. Strike me down, if you will, but know that your actions change nothing!\"\nYou earned " + str(expEarned) + " exp and " + str(goldGained) + " gold."
                                                                                                                            if heroMH == "0":
                                                                                                                                defeat += "\nYou find a key near VanCleef\'. On it the words read, \"The Key to Karazhan\""
                                                                                                                            if ifLootDropped < 16:
                                                                                                                                if heroClass == "warrior":
                                                                                                                                    heroInventory += " 34"
                                                                                                                                    defeat += "\nLoot dropped! You got Protector Armor!```"
                                                                                                                                elif heroClass == "mage":
                                                                                                                                    heroInventory += " 35"
                                                                                                                                    defeat += "\nLoot dropped! You got Shadow Council Robe!```"
                                                                                                                                elif heroClass == "rogue":
                                                                                                                                    heroInventory += " 36"
                                                                                                                                    defeat += "\nLoot dropped! You got Darkened Defias Jenkin!```"
                                                                                                                            else:
                                                                                                                                defeat += "```"
                                                                                                                            await client.send_message(message.channel, defeat)
                                                                                                                            print (heroInventory)
                                                                                                                            cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "', DMLockout = 'XXAAAAA', heroInventory = '" + str(heroInventory) + "' WHERE userID = '" + usertoken + "';")
                                                                                                                            conn.commit()
                                                                                                                            msg = await client.send_message(message.channel,"```VanCleef now lays in front of you, bloodied and bruised. He\'s too tired to fight, and has given up. The choice to make is yours.\nDo you kill VanCleef, or spare him?```".format(message))
                                                                                                                            await client.add_reaction(msg, '🤝')
                                                                                                                            await client.add_reaction(msg, '⚔')
                                                                                                                            res = await client.wait_for_reaction(['🤝', '⚔'], user=message.author, message=msg, timeout = 10)
                                                                                                                except:
                                                                                                                    await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                                                                                                    cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                                                                                                    conn.commit()
                                                                                                    except:
                                                                                                        await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                                                                                        cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                                                                                        conn.commit()
                                                                                        except:
                                                                                            await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                                                                            cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                                                                            conn.commit()
                                                                            except:
                                                                                await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                                                                cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                                                                conn.commit()
                                                                except:
                                                                    await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                                                    cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                                                    conn.commit()
                                                        elif userReactionGI == "🔴":
                                                            heroRoll = round(random.uniform(250,290) - ((1 * int(heroLevel)) * ((.2 * int(heroStr)) + (.35 * int(heroInt)) + (.2 * int(heroAgi)) + (.1 * int(heroArmor)) + (.3 * (int(heroDamage)))) * random.uniform(1,2)))
                                                            heroCurrentHealth = int(heroCurrentHealth) - int(heroRoll)
                                                            if heroCurrentHealth <= 0:
                                                                cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                                                                conn.commit()
                                                                msg = "```Overwhelmed by machines, Gilnid shoots you down as he sneers, \"You\'ve got no right pushing that button! Don\'t ever disturb my work.\"\nWith that, your run ends. Rest up before trying again!```".format(message)
                                                                await client.send_message(message.channel, msg)
                                                            else:
                                                                goldGained = randint(17, 29)
                                                                heroGold = int(heroGold) + int(goldGained)
                                                                expEarned = 4
                                                                expNeeded = math.floor((round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel)))))
                                                                if int(heroEXP)>=int(expNeeded):
                                                                    heroLevel = int(heroLevel) + 1
                                                                    heroMaximumHealth = str(int(heroMaximumHealth) + 20)
                                                                    heroCurrentHealth = str(int(heroCurrentHealth) + 20)
                                                                    heroStam = int(heroStam) + 2
                                                                    heroCrit = int(heroCrit) + 1
                                                                    if heroClass == "warrior":
                                                                        heroStr = int(heroStr) + 1
                                                                    elif heroClass == "mage":
                                                                        heroInt = int(heroInt) + 1
                                                                    elif heroClass == "rogue":
                                                                        heroAgi = int(heroAgi) + 1
                                                                    msg = 'Ding! ' + usertoken + ' reached level ' + str(heroLevel) + " and gained 2 Stamina, 1 Critical Strike Chance and 1 Main Stat! Type Mega Hero to view your stats.".format(message)
                                                                    await client.send_message(message.channel, msg)
                                                                ifLootDropped = randint(1, 100)
                                                                defeat = "```Putting up the best he can, Gilnid finally falls as he squaks. \"You\'ll never get to VanCleef! Never! Haha...\" and dies.\nYou earned " + str(expEarned) + " exp and " + str(goldGained) + " gold."
                                                                if ifLootDropped < 40:
                                                                    if heroClass == "warrior":
                                                                        heroInventory += " 44"
                                                                        defeat += "\nLoot dropped! You got Protector Gloves!```"
                                                                    elif heroClass == "mage":
                                                                        heroInventory += " 45"
                                                                        defeat += "\nLoot dropped! You got Shadow Council Gloves!```"
                                                                    elif heroClass == "rogue":
                                                                        heroInventory += " 46"
                                                                        defeat += "\nLoot dropped! You got Darkened Defias Gloves!```"
                                                                else:
                                                                    defeat += "```"
                                                                await client.send_message(message.channel, defeat)
                                                                print (heroInventory)
                                                                cursor.execute("UPDATE AzerothHeroes SET heroStamina = '" + str(heroStam) + "', heroCrit = '" + str(heroCrit) + "', heroAgi = '" + str(heroAgi) + "', heroInt = '" + str(heroInt) + "', heroStr = '" + str(heroStr) + "', heroMaximumHealth = '" + str(heroMaximumHealth) + "', heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "', DMLockout = 'XXAAAAA', heroInventory = '" + str(heroInventory) + "' WHERE userID = '" + usertoken + "';")
                                                                conn.commit()
                                                                msg = await client.send_message(message.channel,"```Exiting the forgery as it blows to smitherins, you walk onto a dock. In the distance, you see a ship. With a piercing shriek, you hear a dark voice yell \"We\'re under attack! A vast, ye swabs! Repel the invaders!\" Now standing at the ramp to the boat, you\'re greeted by a massive Tauren.\nYou\'re now facing Mr.Smite, VanCleef\'s deckhand. Will you engage combat, or flee, and live another day?```".format(message))
                                                                await client.add_reaction(msg, '🏃')
                                                                await client.add_reaction(msg, '⚔')
                                                                res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                                                        else:
                                                            await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                                            cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                                            conn.commit()
                                                    except:
                                                        await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                                        cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                                        conn.commit()
                                            else:
                                                await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                                cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                                conn.commit()
                                        except:
                                            await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                            cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                            conn.commit()
                                else:
                                    await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                    cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                    conn.commit()
                            except:
                                await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                conn.commit()
                        else:
                            await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                            cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                            conn.commit()
                    except:
                        await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                        cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                        conn.commit()
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
            msg = usertoken + ', are you sure you want to delete your hero? This cannot be undone.\nType in "I wish to delete my hero".'.format(message)
            await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('I WISH TO DELETE MY HERO'):
        usertoken = '{0.author.mention}'.format(message)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
        conn.commit()
        query = cursor.fetchall()
        if cursor.rowcount:
            cursor.execute("DELETE FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
            conn.commit()
            msg = 'Your hero has been destroyed. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
        else:
            msg = 'You do not have a character. Type "Mega Create Hero" to start your journey.'.format(message)
            await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA RESTART'):
        msg = 'Systems integrity damaged. Shutting d-down...'.format(message)
        await client.send_message(message.channel, msg)
        quit()
    
    if usermessage.startswith('MEGA TEST'):
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
            heroClass = userdata[3]
            heroInventory = userdata[13]
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
            heroGold = userdata[24]
            heroUpdateTimer = userdata[25]
            carryOverTime = userdata[26]
            heroDamage = userdata[27]
            heroLockout = userdata[28]
            heroRunning = userdata[29]
            heroMH = userdata[11]
            if heroRunning == "yes":
                msg = await client.send_message(message.channel, usertoken + ', you\'re already running a dungeon!'.format(message))
            else:
                timeNow = calendar.timegm(time.gmtime())
                if int(heroCurrentHealth) < int(heroMaximumHealth):
                    timerUsed = 3600 / (int(heroMaximumHealth) * .15)
                    timeSinceLast = timeNow - int(heroUpdateTimer)
                    healthToRegen = math.floor(timeSinceLast/timerUsed)
                    remainingTime = int(timeSinceLast) % timerUsed
                    carryOverTime = float(carryOverTime) + int(remainingTime)
                    while float(carryOverTime) >= timerUsed:
                        carryOverTime = float(carryOverTime) - timerUsed
                        healthToRegen += 1
                    heroCurrentHealth = int(healthToRegen) + int(heroCurrentHealth)
                    if int(heroCurrentHealth) >= int(heroMaximumHealth):
                        heroCurrentHealth = int(heroMaximumHealth)
                        carryOverTime = 0
                elif int(heroCurrentHealth) == int(heroMaximumHealth):
                    carryOverTime = 0
                cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(heroCurrentHealth) + "', timeUpdated = '" + str(timeNow) + "', carryOverSeconds = '" + str(carryOverTime) + "', currentlyRunning = 'yes' WHERE userID = '" + usertoken + "';")
                conn.commit()
                msg = await client.send_message(message.channel, '```You\'ve reached the entrance to The Deadmines, do you wish to enter or flee?```'.format(message))
                await client.add_reaction(msg, '🏃')
                await client.add_reaction(msg, '⚔')
                res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                if "o->DM" not in heroInventory: #If no key in inventory
                    await client.send_message(message.channel, '```You try to open the door, but no matter how hard you try, the door will not budge. It\'s locked, and the key is no where in sight.\nOut of the corner of your eye, you catch glipse of a merchant, sulking around.\nHe barks, \"Trying to get in there are we? Not without this here key. You want it? Pay up.\"\nYou can view what the merchant sells by typing \'Mega shop\'. ```'.format(message))
                else:
                    currentlyRunning = True
                    fightingWho = "Entered"
                    while currentlyRunning:
                        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
                        conn.commit()
                        query = cursor.fetchall()
                        userdata = []
                        for row in query:
                            for col in row:
                                userdata.append("%s" % col)
                        heroClass = userdata[3]
                        heroInventory = userdata[13]
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
                        heroGold = userdata[24]
                        heroUpdateTimer = userdata[25]
                        carryOverTime = userdata[26]
                        heroDamage = userdata[27]
                        heroLockout = userdata[28]
                        heroRunning = userdata[29]
                        heroMH = userdata[11]
                        timeNow = calendar.timegm(time.gmtime())
                        if int(heroCurrentHealth) < int(heroMaximumHealth):
                            timerUsed = 3600 / (int(heroMaximumHealth) * .15)
                            timeSinceLast = timeNow - int(heroUpdateTimer)
                            healthToRegen = math.floor(timeSinceLast/timerUsed)
                            remainingTime = int(timeSinceLast) % timerUsed
                            carryOverTime = float(carryOverTime) + int(remainingTime)
                            while float(carryOverTime) >= timerUsed:
                                carryOverTime = float(carryOverTime) - timerUsed
                                healthToRegen += 1
                            heroCurrentHealth = int(healthToRegen) + int(heroCurrentHealth)
                            if int(heroCurrentHealth) >= int(heroMaximumHealth):
                                heroCurrentHealth = int(heroMaximumHealth)
                                carryOverTime = 0
                        elif int(heroCurrentHealth) == int(heroMaximumHealth):
                            carryOverTime = 0
                        cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(heroCurrentHealth) + "', timeUpdated = '" + str(timeNow) + "', carryOverSeconds = '" + str(carryOverTime) + "', currentlyRunning = 'yes' WHERE userID = '" + usertoken + "';")
                        conn.commit()

                            msg = await client.send_message(message.channel,"```fight or flee```".format(message))
                            await client.add_reaction(msg, '🏃')
                            await client.add_reaction(msg, '⚔')
                            res = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=msg, timeout = 10)
                            try:
                                if userReaction == "⚔": #Set what boss they're fighting
                                    if heroLockout = "AAAAAAA":
                                        fightingWho = "RH"
                                    elif heroLockout = "XAAAAAA":
                                        fightingWho = "SN"
                                    elif heroLockout = "XXAAAAA":
                                        fightingWho = "GI"
                                    elif heroLockout = "XXXAAAA":
                                        fightingWho = "SM"
                                    elif heroLockout = "XXXXAAA":
                                        fightingWho = "CO"
                                    elif heroLockout = "XXXXXAA":
                                        fightingWho = "GR"
                                    elif heroLockout = "XXXXXXA":
                                        fightingWho = "VC"
                                    elif heroLockout = "XXXXXXX":
                                        fightingWho = "Cleared"
                                elif userReaction == "🏃":
                                    fightingWho = "Flee"
                                    currentlyRunning = False
                                    await client.send_message(message.channel, '```You flee to live another day.```'.format(message))
                                    cursor.execute("UPDATE AzerothHeroes SET currentlyRunning = 'no' WHERE userID = '" + usertoken + "';")
                                    conn.commit()

                                if fightingWho = "RH":
                                    print()
                                if fightingWho = "SN":
                                    print()
                                if fightingWho = "GI":
                                    print()
                                if fightingWho = "SM":
                                    print()
                                if fightingWho = "CO":
                                    print()
                                if fightingWho = "GR":
                                    print()
                                if fightingWho = "VC":
                                    print()
                            except:

    conn.close()
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Mega Help'))
client.run(TOKEN)