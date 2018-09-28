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
            await client.send_message(message.channel, "You can create a character!\nSimply respond with (Mega create my orc/human warrior/mage named XXX).")
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
            if 'NAMED' in usermessage and ('warrior' in message.content or 'mage' in message.content) and ('orc' in message.content or 'human' in message.content) and len(message.content.split()) >= 7:
                regexp = re.compile("named (.*)$")
                name = regexp.search(message.content).group(1)
                name = " ".join(name.split()).title()
                for k in name.split("\n"):
                    name = re.sub(r"[^a-zA-Z0-9]+", ' ', k)
                if len(name) < 12:
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
                    heroInventory = heroChest + " " + heroGloves + " " + heroBelt + " " + heroLegs + " " + heroFeet + " " + heroMH + " "
                    cursor.execute("INSERT INTO AzerothHeroes (userID, heroName, heroRace, heroClass, heroHelm, heroShoulders, heroChest, heroGloves, heroBelt, heroLegs, heroFeet, heroMH, heroOH, heroInventory, heroCurrentHealth, heroMaximumHealth, heroStamina, heroArmor, heroInt, heroStr, heroAgi, heroCrit, EXP, level, heroGold, timeUpdated, carryOverSeconds) VALUES ('" + usertoken + "','" + name +"','" + heroRace + "','" + heroClass + "','0','0','" + heroChest + "','" + heroGloves +"','" + heroBelt + "','" + heroLegs + "','" + heroFeet + "','" + heroMH + "','0','" + heroInventory + "','" + heroHealth + "','" + heroHealth + "','" + heroStam + "','" + heroArmor + "','" + heroInt + "','" + heroStr + "','" + heroAgi + "','" + heroCrit + "','0','1','0','" + str(timeNow) + "','0');")
                    conn.commit()
                    await client.send_message(message.channel, "You chose a " + heroRace + " " + heroClass + " named " + name + "! To view your character type in, 'Mega Hero'.")
                else:
                    await client.send_message(message.channel, "Your name was too long! A name cannot be longer than 12 characters.")
            else:
                await client.send_message(message.channel, "Your response was formatted incorrectly. Make sure to include your race, class and name! An example:\nMega create my orc warrior name zugzug.")
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
                heroOffSet = (110,180)
            if heroRace == "human":
                heroHelm = "human" + str(userdata[4])
                heroShoulder = "human" + str(userdata[5])
                heroChest = "human" + str(userdata[6])
                heroGloves = "human" + str(userdata[7])
                heroBelt = "human" + str(userdata[8])
                heroLegs = "human" + str(userdata[9])
                heroFeet = "human" + str(userdata[10])
                heroOffSet = (110,180)
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
            heroGold = userdata[24]
            heroUpdateTimer = userdata[25]
            carryOverTime = userdata[26]
            if int(heroCurrentHealth) < int(heroMaximumHealth):
                timeNow = calendar.timegm(time.gmtime())
                timeSinceLast = timeNow - int(heroUpdateTimer)
                healthToRegen = math.floor(timeSinceLast/180)
                remainingTime = int(timeSinceLast) % 180
                carryOverTime = int(carryOverTime) + int(remainingTime)
                if int(carryOverTime) >= 180:
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
                if int(carryOverTime) >= 180:
                    carryOverTime = int(carryOverTime) - 180
                    healthToRegen += 1
                heroCurrentHealth = int(healthToRegen) + int(heroCurrentHealth)
                if int(heroCurrentHealth) >= int(heroMaximumHealth):
                    heroCurrentHealth = int(heroMaximumHealth)
                    carryOverTime = 0
            healthlost = round(random.uniform(20, 50) - (.1 * int(heroArmor)))
            heroCurrentHealth = int(heroCurrentHealth) - int(healthlost)
            if heroCurrentHealth <= 0:
                MaxMinusOne = (int(heroMaximumHealth) - 1) * 180
                cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(1) + "', timeUpdated = '" + str(timeNow) + "' WHERE userID = '" + usertoken + "';")
                conn.commit()
                msg = 'You suffered fatal damage and earned nothing. Rest up before training again!'.format(message)
                await client.send_message(message.channel, msg)
            else:
                goldGained = round(random.uniform(1, 3) * ((.1 * int(heroStr)) + (.4 * int(heroInt)) + (.3 * int(heroAgi))))
                heroGold = int(heroGold) + int(goldGained)
                heroEXP = int(heroEXP) + 1
                heroLevel = math.floor(heroEXP/(round((0.04*(int(heroLevel)**3))+(0.8*(int(heroLevel)**2))+(2*int(heroLevel))))) + 1
                cursor.execute("UPDATE AzerothHeroes SET heroCurrentHealth = '" + str(heroCurrentHealth) + "', heroGold = '" + str(heroGold) + "', EXP = '" + str(heroEXP) + "', Level = '" + str(heroLevel) + "' WHERE userID = '" + usertoken + "';")
                conn.commit()
                msg = 'You succesfully completed training! You earned 1 EXP and ' + str(goldGained) + ' gold.\nYou lost ' + str(healthlost) + ' health.'.format(message)
                await client.send_message(message.channel, msg)

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
    if usermessage.startswith('MEGA ABORT THIS MISSION'):
        msg = 'Deleting all files and data. I\'m outta here!'.format(message)
        await client.send_message(message.channel, msg)
    if usermessage.startswith('MEGA SHOW ME THE COCK'):
        await client.send_file(message.channel, 'thecock.png')
    conn.close()
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Mega Help'))
client.run(TOKEN)