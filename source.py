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
            if int(heroCurrentHealth) < int(heroMaximumHealth):
                timeNow = calendar.timegm(time.gmtime())
                timeSinceLast = timeNow - int(heroUpdateTimer)
                healthToRegen = math.floor(timeSinceLast/180)
                remainingTime = int(timeSinceLast) % 180
                carryOverTime = int(carryOverTime) + int(remainingTime)
                while int(carryOverTime) >= 180:
                    carryOverTime = int(carryOverTime) - 180
                    healthToRegen += 1
                heroCurrentHealth = int(healthToRegen) + int(heroCurrentHealth)
                if int(heroCurrentHealth) >= int(heroMaximumHealth):
                    heroCurrentHealth = int(heroMaximumHealth)
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
            msg = "Your items:\n\n"
            for i in parseItems:
                currentItem = i
                cursor.execute("SELECT itemName, itemDamage, itemStam, itemStr, itemInt, itemAgi, itemCrit, itemArmor FROM AzerothHeroesItems WHERE itemID = '" + currentItem + "';")
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
            if int(heroCurrentHealth) < int(heroMaximumHealth):
                timeNow = calendar.timegm(time.gmtime())
                timeSinceLast = timeNow - int(heroUpdateTimer)
                healthToRegen = math.floor(timeSinceLast/180)
                remainingTime = int(timeSinceLast) % 180
                carryOverTime = int(carryOverTime) + int(remainingTime)
                while int(carryOverTime) >= 180:
                    carryOverTime = int(carryOverTime) - 180
                    healthToRegen += 1
                heroCurrentHealth = int(healthToRegen) + int(heroCurrentHealth)
                if int(heroCurrentHealth) >= int(heroMaximumHealth):
                    heroCurrentHealth = int(heroMaximumHealth)
                    carryOverTime = 0
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
                                duelInitData = []
                                duelRecipData = []
                                cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + duelInit + "';")
                                conn.commit()
                                query = cursor.fetchall()
                                for row in query:
                                    for col in row:
                                        duelInitData.append("%s" % col)
                                cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + duelRecip + "';")
                                conn.commit()
                                queryRecip = cursor.fetchall()
                                for row in queryRecip:
                                    for col in row:
                                        duelRecipData.append("%s" % col)
                                duelInitClass = duelInitData[3]
                                duelInitCurrentHealth = duelInitData[14]
                                duelInitMaximumHealth = duelInitData[15]
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
                                if int(duelInitCurrentHealth) < int(duelInitMaximumHealth):
                                    timeNow = calendar.timegm(time.gmtime())
                                    duelInittimeSinceLast = timeNow - int(duelInitUpdateTimer)
                                    duelInithealthToRegen = math.floor(duelInittimeSinceLast/180)
                                    duelInitremainingTime = int(duelInittimeSinceLast) % 180
                                    duelInitcarryOverTime = int(duelInitcarryOverTime) + int(duelInitremainingTime)
                                    while int(duelInitcarryOverTime) >= 180:
                                        duelInitcarryOverTime = int(duelInitcarryOverTime) - 180
                                        duelInithealthToRegen += 1
                                    duelInitCurrentHealth = int(duelInithealthToRegen) + int(duelInitCurrentHealth)
                                    if int(duelInitCurrentHealth) >= int(duelInitMaximumHealth):
                                        duelInitCurrentHealth = int(duelInitMaximumHealth)
                                        duelInitcarryOverTime = 0
                                    cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(duelInitCurrentHealth) + "', timeUpdated = '" + str(timeNow) + "', carryOverSeconds = '" + str(duelInitcarryOverTime) + "' WHERE userID = '" + duelInit + "';")
                                    conn.commit()
                                if int(duelRecipCurrentHealth) < int(duelRecipMaximumHealth):
                                    timeNow = calendar.timegm(time.gmtime())
                                    duelReciptimeSinceLast = timeNow - int(duelRecipUpdateTimer)
                                    duelReciphealthToRegen = math.floor(duelReciptimeSinceLast/180)
                                    duelRecipremainingTime = int(duelReciptimeSinceLast) % 180
                                    duelRecipcarryOverTime = int(duelRecipcarryOverTime) + int(duelRecipremainingTime)
                                    while int(duelRecipcarryOverTime) >= 180:
                                        duelRecipcarryOverTime = int(duelRecipcarryOverTime) - 180
                                        duelReciphealthToRegen += 1
                                    duelRecipCurrentHealth = int(duelReciphealthToRegen) + int(duelRecipCurrentHealth)
                                    if int(duelRecipCurrentHealth) >= int(duelRecipMaximumHealth):
                                        duelRecipCurrentHealth = int(duelRecipMaximumHealth)
                                        duelRecipcarryOverTime = 0
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
    if usermessage.startswith('MEGA GAMBLE'):
        print()
    if usermessage.startswith('MEGA DUNGEON'):
        print()
    if usermessage.startswith('MEGA SHOP'):
        print()

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
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Mega Help'))
client.run(TOKEN)