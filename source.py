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
import sys

TOKEN = app_id = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_message(message):
    conn = pymysql.connect(os.environ['herokuServer'],os.environ['herokuUser'],os.environ['herokuPass'],os.environ['herokuDB'])
    cursor = conn.cursor()
    userData, usertoken, itemData = {}, '{0.author.mention}'.format(message), {}    
    duelData = {}
    #Functions to retrieve data
    def findUserData(userID):
        cursor.execute("SELECT * FROM AzerothHeroes WHERE userID = '" + userID + "';")
        conn.commit()
        query = cursor.fetchall()
        tempdata = []
        for row in query:
            for col in row:
                tempdata.append("%s" % col)
        userData["heroName"] = tempdata[1]
        userData["heroRace"] = tempdata[2]
        userData["heroClass"] = tempdata[3]
        userData["heroHelmet"] = tempdata[4]
        userData["heroShoulder"] = tempdata[5]
        userData["heroChest"] = tempdata[6]
        userData["heroGloves"] = tempdata[7]
        userData["heroBelt"] = tempdata[8]
        userData["heroLegs"] = tempdata[9]
        userData["heroFeet"] = tempdata[10]
        userData["heroMH"] = tempdata[11]
        userData["heroOH"] = tempdata[12]
        userData["heroInventory"] = tempdata[13]
        userData["heroCurrentHealth"] = tempdata[14]
        userData["heroMaximumHealth"] = tempdata[15]
        userData["heroStam"] = tempdata[16]
        userData["heroArmor"] = tempdata[17]
        userData["heroInt"] = tempdata[18]
        userData["heroStr"] = tempdata[19]
        userData["heroAgi"] = tempdata[20]
        userData["heroCrit"] = tempdata[21]
        userData["heroEXP"] = tempdata[22]
        userData["heroLevel"] = tempdata[23]
        userData["heroGold"] = tempdata[24]
        userData["heroUpdateTimer"] = tempdata[25]
        userData["carryOverTime"] = tempdata[26]
        userData["heroDamage"] = tempdata[27]
        userData["heroDMLockout"] = tempdata[28]
        userData["heroRunning"] = tempdata[29]
    def findItemData(itemID):
        if len(itemID) <= 3:
            cursor.execute("SELECT * FROM AzerothHeroesItems WHERE itemID = '" + itemID + "';")
        else:
            cursor.execute("SELECT * FROM AzerothHeroesItems WHERE itemName = '" + itemID + "';")
        conn.commit()
        query = cursor.fetchall()
        tempdata = []
        for row in query:
            for col in row:
                tempdata.append("%s" % col)
        itemData["itemID"] = tempdata[0]
        itemData["itemName"] = tempdata[1]
        itemData["itemDamage"] = tempdata[2]
        itemData["itemStam"] = tempdata[3]
        itemData["itemStr"] = tempdata[4]
        itemData["itemInt"] = tempdata[5]
        itemData["itemAgi"] = tempdata[6]
        itemData["itemCrit"] = tempdata[7]
        itemData["itemArmor"] = tempdata[8]
        itemData["itemSlot"] = tempdata[9]
    def pullUpInventory(userID):
        findUserData(userID)
        parseItems = userData["heroInventory"].split()
        outMsg = userID + "'s items:```"
        for i in parseItems:
            print (i)
            findItemData(i)
            if len(itemData["itemName"]) > 0:
                outMsg += itemData["itemName"]
            if int(itemData["itemDamage"]) > 0:
                outMsg += "\nDamage: " + itemData["itemDamage"]
            if int(itemData["itemArmor"]) > 0:
                outMsg += "\nArmor: " + itemData["itemArmor"]
            if int(itemData["itemStam"]) > 0:
                outMsg += "\nStamina: " + itemData["itemStam"]
            if int(itemData["itemStr"]) > 0:
                outMsg += "\nStrength: " + itemData["itemStr"]
            if int(itemData["itemInt"]) > 0:
                outMsg += "\nIntellect: " + itemData["itemInt"]
            if int(itemData["itemAgi"]) > 0:
                outMsg += "\nAgility: " + itemData["itemAgi"]
            if int(itemData["itemCrit"]) > 0:
                outMsg += "\nCritical Hit Chance: " + itemData["itemCrit"]
            outMsg += "\n\n"
            itemData.clear()
        outMsg += "```"
        return outMsg
    def inspectEquipment(userID):
        findUserData(userID)
        parseItems = [userData["heroHelmet"],userData["heroShoulder"],userData["heroChest"],userData["heroGloves"],userData["heroBelt"],userData["heroLegs"],userData["heroFeet"],userData["heroMH"],userData["heroOH"]]
        outMsg = userID + "'s equipment:```"
        x = 0
        for i in parseItems:
            if i != "0":
                findItemData(i)
                if len(itemData["itemName"]) > 0:
                    outMsg += "\n" + itemData["itemName"]
                if int(itemData["itemDamage"]) > 0:
                    outMsg += "\nDamage: " + itemData["itemDamage"]
                if int(itemData["itemArmor"]) > 0:
                    outMsg += "\nArmor: " + itemData["itemArmor"]
                if int(itemData["itemStam"]) > 0:
                    outMsg += "\nStamina: " + itemData["itemStam"]
                if int(itemData["itemStr"]) > 0:
                    outMsg += "\nStrength: " + itemData["itemStr"]
                if int(itemData["itemInt"]) > 0:
                    outMsg += "\nIntellect: " + itemData["itemInt"]
                if int(itemData["itemAgi"]) > 0:
                    outMsg += "\nAgility: " + itemData["itemAgi"]
                if int(itemData["itemCrit"]) > 0:
                    outMsg += "\nCritical Hit Chance: " + itemData["itemCrit"]
            else:
                if x == 0:
                    outMsg += "\nNo helmet equipped."
                elif x == 1:
                    outMsg += "\nNo shoulders equipped."
                elif x == 2:
                    outMsg += "\nNo chest equipped."
                elif x == 3:
                    outMsg += "\nNo gloves equipped."
                elif x == 4:
                    outMsg += "\nNo belt equipped."
                elif x == 5:
                    outMsg += "\nNo legs equipped."
                elif x == 6:
                    outMsg += "\nNo feet equipped."
                elif x == 7:
                    outMsg += "\nNo main hand equipped."
                elif x == 8:
                    outMsg += "\nNo offhand equipped."
            outMsg += "\n"
            itemData.clear()
            x += 1
        outMsg += "```"
        return outMsg
    def findDuelData(userID, whom):
        try:
            cursor.execute("SELECT * FROM AzerothHeroesDuels WHERE " + whom + " = '" + userID + "';")
            conn.commit()
            query = cursor.fetchall()
            tempdata = []
            for row in query:
                for col in row:
                    tempdata.append("%s" % col)
            duelData["duelInit"] = tempdata[0]
            duelData["duelRecip"] = tempdata[1]
            return True
        except Exception as e:
            print(e)
            print("Couldn't find person")
            return None

    #Functions for string manipulation
    def subStringAfter(keyword):
        regexp = re.compile(keyword + " (.*)$")
        name = regexp.search(message.content).group(1)
        name = " ".join(name.split()).title()
        return name
    def filterSpecialChars(string):
        for k in string.split("\n"):
            string = re.sub(r"[^a-zA-Z0-9]+", '', k)
        return string
    
    #Functions to update user data
    def updateCharacter(where, value, userID):
        cursor.execute("UPDATE AzerothHeroes SET " + where + " = '" + value + "' WHERE userID = '" + userID + "';")
        conn.commit()
    def updateHealth(userID):
        findUserData(userID)
        timeNow = calendar.timegm(time.gmtime())
        heroCurrentHealth = userData["heroCurrentHealth"]
        heroMaximumHealth = userData["heroMaximumHealth"]
        carryOverTime = userData["carryOverTime"]
        heroUpdateTimer = userData["heroUpdateTimer"]
        if int(heroCurrentHealth) < int(heroMaximumHealth):
            timerUsed = 3600 / (int(heroMaximumHealth) * .20)
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
        updateCharacter("heroCurrentHealth",str(heroCurrentHealth),userID)
        updateCharacter("timeUpdated",str(timeNow),userID)
        updateCharacter("carryOverSeconds", str(carryOverTime), userID)
    def unequipGear(userID, itemID):
        findItemData(itemID)
        updateCharacter(itemData["itemSlot"], str(0), userID)
        updateCharacter("heroDamage", str(int(userData["heroDamage"]) - int(itemData["itemDamage"])), userID)
        updateCharacter("heroStamina", str(int(userData["heroStam"]) - int(itemData["itemStam"])), userID)
        updateCharacter("heroStr", str(int(userData["heroStr"]) - int(itemData["itemStr"])), userID)
        updateCharacter("heroAgi", str(int(userData["heroAgi"]) - int(itemData["itemAgi"])), userID)
        updateCharacter("heroInt", str(int(userData["heroInt"]) - int(itemData["itemInt"])), userID)
        updateCharacter("heroCrit", str(int(userData["heroCrit"]) - int(itemData["itemCrit"])), userID)
        updateCharacter("heroArmor", str(int(userData["heroArmor"]) - int(itemData["itemArmor"])), userID)
        updateCharacter("heroMaximumHealth", str(int(userData["heroMaximumHealth"]) - (int(itemData["itemStam"]) * 10)), userID)
        updateCharacter("heroCurrentHealth", str(int(userData["heroCurrentHealth"]) - (int(itemData["itemStam"]) * 10)), userID)
    def equipGear(userID, itemID, **kwargs):
        unequip = kwargs.get('unequip', None)
        damageChange, armorChange, stamChange, strChange, intChange, agiChange, critChange, heroMHChange, heroCHChange = 0,0,0,0,0,0,0,0,0
        if unequip != None:
            findItemData(unequip)
            damageChange -= int(itemData["itemDamage"])
            stamChange -= int(itemData["itemStam"])
            strChange -= int(itemData["itemStr"])
            intChange -= int(itemData["itemInt"])
            agiChange -= int(itemData["itemAgi"])
            critChange -= int(itemData["itemCrit"])
            armorChange -= int(itemData["itemArmor"])
            heroMHChange -= (int(itemData["itemStam"]) * 10)
            heroCHChange -= (int(itemData["itemStam"]) * 10)
        findItemData(itemID)
        damageChange += int(itemData["itemDamage"])
        stamChange += int(itemData["itemStam"])
        strChange += int(itemData["itemStr"])
        intChange += int(itemData["itemInt"])
        agiChange += int(itemData["itemAgi"])
        critChange += int(itemData["itemCrit"])
        armorChange += int(itemData["itemArmor"])
        heroMHChange += (int(itemData["itemStam"]) * 10)
        heroCHChange += (int(itemData["itemStam"]) * 10)
        updateCharacter(itemData["itemSlot"], str(itemData["itemID"]), userID)
        updateCharacter("heroDamage", str(int(userData["heroDamage"]) + damageChange), userID)
        updateCharacter("heroStamina", str(int(userData["heroStam"]) + stamChange), userID)
        updateCharacter("heroStr", str(int(userData["heroStr"]) + strChange), userID)
        updateCharacter("heroAgi", str(int(userData["heroAgi"]) + agiChange), userID)
        updateCharacter("heroInt", str(int(userData["heroInt"]) + intChange), userID)
        updateCharacter("heroCrit", str(int(userData["heroCrit"]) + critChange), userID)
        updateCharacter("heroArmor", str(int(userData["heroArmor"]) + armorChange), userID)
        updateCharacter("heroMaximumHealth", str(int(userData["heroMaximumHealth"]) + heroMHChange), userID)
        updateCharacter("heroCurrentHealth", str(int(userData["heroCurrentHealth"]) + heroCHChange), userID)
    def goldGained(min, max, userID):
        findUserData(userID)
        goldGained = round(random.uniform(min, max) * (((.15 * int(userData["heroDamage"])) + (.1 * int(userData["heroStr"])) + (.15 * int(userData["heroInt"])) + (.1 * int(userData["heroAgi"])))))
        newGold = goldGained + int(userData['heroGold'])
        updateCharacter("heroGold", str(newGold), userID)
        return goldGained
    def failedAttempt(userID):
        updateCharacter("timeUpdated", str(calendar.timegm(time.gmtime())), userID)
        updateCharacter("heroCurrentHealth", str(1), userID)
    def levelUp(userID):
        findUserData(userID)
        expNeeded = math.floor((round((0.04*(int(userData["heroLevel"])**3))+(0.8*(int(userData["heroLevel"])**2))+(2*int(userData["heroLevel"])))))
        if int(userData["heroEXP"])>=int(expNeeded):
            try:
                outMsg = "Ding! You've leveled up! You gained 2 Stamina, 1 Critical Strike Chance and 1 "
                newLevel= int(userData["heroLevel"]) + 1
                newMH = int(userData["heroMaximumHealth"]) + 20
                newCR = int(userData["heroCurrentHealth"]) + 20
                newStam = int(userData["heroStam"]) + 2
                newCrit = int(userData["heroCrit"]) + 1
            except Exception as e:
                print(e)
                print("Bug between here!")
            if userData["heroClass"] == "warrior":
                newStr = int(userData["heroStr"]) + 1
                outMsg += "Strength!```"
                updateCharacter("heroStr", str(newStr), userID)
            elif userData["heroClass"] == "mage":
                newInt = int(userData["heroInt"]) + 1
                outMsg += "Intellect!```"
                updateCharacter("heroInt", str(newInt), userID)
            elif userData["heroClass"] == "rogue":
                newAgi = int(userData["heroAgi"]) + 1
                outMsg += "Agility!```"
                updateCharacter("heroAgi", str(newAgi), userID)
            updateCharacter("level", str(newLevel), userID)
            updateCharacter("heroMaximumHealth", str(newMH), userID)
            updateCharacter("heroCurrentHealth", str(newCR), userID)
            updateCharacter("heroStamina", str(newStam), userID)
            updateCharacter("heroCrit", str(newCrit), userID)
            return outMsg
        else:
            return None

    #Functions to update duel data
    def updateDuelData(where, value, userID):
        cursor.execute("UPDATE AzerothHeroesDuels SET " + where + " = " + value + " WHERE userID = '" + userID + "';")
        conn.commit()
    def insertIntoDuelData(duelInit, duelRecip):
        cursor.execute("INSERT INTO AzerothHeroesDuels (duelInit, duelRecip) VALUES ('" + duelInit + "','" + duelRecip + "');")
        conn.commit()
    def deleteFromDuelData(where):
        cursor.execute("DELETE FROM AzerothHeroesDuels WHERE duelInit = '" + where + "';")
        conn.commit()

    usermessage = message.content.upper() 
    if message.author == client.user:
        return
    if usermessage.startswith('MEGA HELP'):
        await client.send_message(message.author, 'Hello, {0.author.mention}, I\'m a Machine Engineered to Guide Anyone, or M.E.G.A! Type "Mega Create Hero" to get started, or "Mega Delete" to delete your hero.'.format(message))
    if usermessage.startswith('MEGA INTRODUCE YOURSELF'):
        await client.send_message(message.channel, 'Hello, {0.author.mention}, I\'m a Machine Engineered to Guide Anyone, or M.E.G.A! Type "Mega Create Hero" to get started, or "Mega Delete" to delete your hero.'.format(message))
    if usermessage.startswith('MEGA CREATE HERO'):
        try:
            findUserData(usertoken)
            await client.send_message(message.channel, "You already have a character! Type in, 'Mega Hero' to view them!")
        except Exception as e:
            print(e)
            await client.send_message(message.channel, "You can create a character!\nSimply respond with (Mega create my orc/human warrior/mage/rogue named XXX).")
    if usermessage.startswith('MEGA CREATE MY'):
        try:
            findUserData(usertoken)
            await client.send_message(message.channel, "You already have a character! Say, 'Mega Hero' to view them!")
        except Exception as e: 
            print(e)
            if 'NAMED' in usermessage and ('warrior' in message.content or 'mage' in message.content or 'rogue' in message.content) and ('orc' in message.content or 'human' in message.content) and len(message.content.split()) >= 7:
                name = filterSpecialChars(subStringAfter("named"))
                if len(name) < 12:
                    userID, heroName, heroRace, heroClass, heroHelm, heroShoulders, heroChest, heroGloves, heroBelt, heroLegs, heroFeet, heroMH, heroOH, heroInventory, heroCurrentHealth, heroMaximumHealth, heroStam, heroArmor, heroInt, heroStr, heroAgi, heroCrit, EXP, level, heroGold, timeUpdated, carryOverSeconds, heroDamage, DMLockout, heroRunning = usertoken, name, "race", "class", "1", "2", "3", "4", "5", "6", "7", "8", "OH", "In", "heroC", "heroM", "stam", "armor", "int", "str", "agi", "crit", "0", "1", "0", calendar.timegm(time.gmtime()), "0", "dmg", "AAAAAAA", "no"
                    if 'warrior' in message.content and len(message.content.split()) >= 7:
                        heroClass = "warrior"
                        heroChest = "31"
                        heroGloves = "41"
                        heroBelt = "51"
                        heroLegs = "61"
                        heroFeet = "71"
                        heroMH = "81"
                        heroOH = "0"
                        heroMaximumHealth, heroCurrentHealth = "150", "150"
                        heroStam = "10"
                        heroArmor = "15"
                        heroInt = "0"
                        heroStr = "10"
                        heroAgi = "0"
                        heroCrit = "5"
                        heroDamage = "5"
                        heroInventory = heroChest + " " + heroGloves + " " + heroBelt + " " + heroLegs + " " + heroFeet + " " + heroMH
                    elif 'mage' in message.content and len(message.content.split()) >= 7:
                        heroClass = "mage"
                        heroChest = "32"
                        heroGloves = "42"
                        heroBelt = "52"
                        heroLegs = "62"
                        heroFeet = "72"
                        heroMH = "82"
                        heroOH = "0"
                        heroMaximumHealth, heroCurrentHealth = "100", "100"
                        heroStam = "5"
                        heroArmor = "5"
                        heroInt = "15"
                        heroStr = "0"
                        heroAgi = "0"
                        heroCrit = "10"
                        heroDamage = "1"
                        heroInventory = heroChest + " " + heroGloves + " " + heroBelt + " " + heroLegs + " " + heroFeet + " " + heroMH
                    elif 'rogue' in message.content and len(message.content.split()) >= 7:
                        heroClass = "rogue"
                        heroChest = "33"
                        heroGloves = "43"
                        heroBelt = "53"
                        heroLegs = "63"
                        heroFeet = "73"
                        heroMH = "83"
                        heroOH = "91"
                        heroMaximumHealth, heroCurrentHealth = "120", "120"
                        heroStam = "7"
                        heroArmor = "10"
                        heroInt = "0"
                        heroStr = "0"
                        heroAgi = "14"
                        heroCrit = "20"
                        heroDamage = "4"
                        heroInventory = heroChest + " " + heroGloves + " " + heroBelt + " " + heroLegs + " " + heroFeet + " " + heroMH + " " + heroOH
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
                        heroCurrentHealth, heroMaximumHealth = str(int(heroMaximumHealth) + 10), str(int(heroMaximumHealth) + 10)
                        heroStam = str(int(heroStam) + 1)
                    heroHelm = "0"
                    heroShoulders = "0"
                    cursor.execute("INSERT INTO AzerothHeroes (userID, heroName, heroRace, heroClass, heroHelm, heroShoulders, heroChest, heroGloves, heroBelt, heroLegs, heroFeet, heroMH, heroOH, heroInventory, heroCurrentHealth, heroMaximumHealth, heroStamina, heroArmor, heroInt, heroStr, heroAgi, heroCrit, EXP, level, heroGold, timeUpdated, carryOverSeconds, heroDamage, DMLockout, heroRunning) VALUES ('" + userID + "','" + heroName +"','" + heroRace + "','" + heroClass + "','" + heroHelm + "','" + heroShoulders + "','" + heroChest + "','" + heroGloves +"','" + heroBelt + "','" + heroLegs + "','" + heroFeet + "','" + heroMH + "','" + heroOH + "','" + heroInventory + "','" + heroCurrentHealth + "','" + heroMaximumHealth + "','" + heroStam + "','" + heroArmor + "','" + heroInt + "','" + heroStr + "','" + heroAgi + "','" + heroCrit + "','" + EXP + "','" + level + "','" + heroGold + "','" + str(timeUpdated) + "','" + carryOverSeconds + "', '" + heroDamage + "', '" + DMLockout + "', '" + heroRunning + "');")
                    conn.commit()
                    await client.send_message(message.channel, "You chose a " + heroRace + " " + heroClass + " named " + name + "! To view your character type in, 'Mega Hero'.")
                else:
                    await client.send_message(message.channel, "Your name was too long! A name cannot be longer than 12 characters.")
            else:
                await client.send_message(message.channel, "Your response was formatted incorrectly. Make sure to include your race, class and name! An example:\nMega create my orc warrior named zugzug.")
    if usermessage.startswith('MEGA HERO'):
        if len(usermessage.split()) >= 3:
            userTag = subStringAfter("hero")
        else:
            userTag = usertoken
        try:
            updateHealth(userTag)
            findUserData(userTag)
            dispHelm = userData['heroRace'] + userData['heroHelmet']
            dispShoulder = userData['heroRace'] + userData['heroShoulder']
            dispChest = userData['heroRace'] + userData['heroChest']
            dispGloves = userData['heroRace'] + userData['heroGloves']
            dispBelt = userData['heroRace'] + userData['heroBelt']
            dispLegs = userData['heroRace'] + userData['heroLegs']
            dispFeet = userData['heroRace'] + userData['heroFeet']
            dispOH = userData['heroRace'] + userData['heroOH']
            dispMH = userData['heroMH']
            heroOffSet = (110,180)
            background = Image.open('Items/white.jpg')
            hero = Image.open("Items/" + str(userData['heroRace']) + '.png')
            helmet = Image.open("Items/" + str(dispHelm) + '.png')
            shoulders = Image.open("Items/" + str(dispShoulder) + '.png')
            chest = Image.open("Items/" + str(dispChest) + '.png')
            gloves = Image.open("Items/" + str(dispGloves) + '.png')
            belt = Image.open("Items/" + str(dispBelt) + '.png')
            legs = Image.open("Items/" + str(dispLegs) + '.png')
            feet = Image.open("Items/" + str(dispFeet) + '.png')
            mainhand = Image.open("Items/" + str(dispMH) + '.png')
            offhand = Image.open("Items/" + str(dispOH) + '.png')
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
            d.text((10,10), "Hero: " + userData['heroName'] , fill=(0,0,0), font = font)
            d.text((10,30), "Specialization: " + userData['heroRace'] .title() + " " + userData['heroClass'].title() + ".", fill=(0,0,0), font = font)
            d.text((10,50), "Health: " + str(userData['heroCurrentHealth']) + " / " + str(userData['heroMaximumHealth']), fill=(0,0,0), font = font)
            d.text((30,100), userData['heroGold'] + " gold", fill=(0,0,0), font = font)
            remainingHealth = int((int(userData['heroCurrentHealth']) / int(userData['heroMaximumHealth'])) * 62)
            ActualHealthBar = healthbar.crop((0,0,remainingHealth,22))
            canvas.paste(ActualHealthBar, (10, 70), mask=ActualHealthBar)
            canvas.paste(healthbarFrame, (10, 70), mask=healthbarFrame)
            canvas.paste(goldCoin, (10, 100), mask=goldCoin)
            d.text((350,70), "Level: " + userData['heroLevel'], fill=(0,0,0), font = font)
            d.text((350,90), "EXP: " + userData['heroEXP'], fill=(0,0,0), font = font)
            d.text((350,50), "Armor: " + userData['heroArmor'], fill=(0,0,0), font = font)
            d.text((350,30), "Stamina: " + userData['heroStam'], fill=(0,0,0), font = font)
            if userData['heroClass'] == "warrior":
                d.text((350,10), "Strength: " + userData['heroStr'], fill=(0,0,0), font = font)
            if userData['heroClass']  == "mage":
                d.text((350,10), "Intellect: " + userData['heroInt'], fill=(0,0,0), font = font)
            if userData['heroClass']  == "rogue":
                d.text((350,10), "Agility: " + userData['heroAgi'], fill=(0,0,0), font = font)
            canvas.save('hero.png', format="png")
            await client.send_file(message.channel, 'hero.png')
            os.remove("hero.png")
        except Exception as e:
            print(e)
            if len(usermessage.split()) >= 3:
                await client.send_message(message.channel, "Could not find the hero you were trying to inspect.")
            else:
                await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")
    if usermessage.startswith('MEGA INVENTORY'):
        if len(usermessage.split()) >= 3:
            user = subStringAfter("inventory")
        else:
            user = usertoken
        try:
            msg = pullUpInventory(user)
            await client.send_message(message.channel, msg)
        except Exception as e:
            print(e)
            if len(usermessage.split()) >= 3:
                await client.send_message(message.channel, "Could not find the hero you were trying to inspect.")
            else:
                await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")
    if usermessage.startswith('MEGA EQUIP'):
        try:
            findUserData(usertoken)
            if len(usermessage.split()) >= 3:
                name = subStringAfter("equip")
                try:
                    findItemData(name)
                    if userData[itemData["itemSlot"]] != "0":
                        equipGear(usertoken, name, unequip = userData[itemData["itemSlot"]])
                        findItemData(userData[itemData["itemSlot"]])
                        await client.send_message(message.channel, usertoken + "```You succesfully replaced [" + itemData["itemName"] + "] with [" + name + "]```")
                    else:
                        equipGear(usertoken, name)
                        await client.send_message(message.channel, usertoken + "```You succesfully equipped [" + name + "]```")
                except Exception as e:
                    print(e)
                    await client.send_message(message.channel, "Couldn\'t find the item you were looking for. Type \"Mega Inventory\" to see your items.")
            else:
                await client.send_message(message.channel, "What would you like to equip? Type \"Mega Inventory\" to see your items.")
        except Exception as e:
            print (e)
            await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")
    if usermessage.startswith('MEGA UNEQUIP'):
        try:
            findUserData(usertoken)
            if len(message.content.split()) >= 3:
                try:
                    itemName = subStringAfter("unequip")
                    unequipGear(usertoken, itemName)
                    await client.send_message(message.channel, usertoken + "```You succesfully unequipped [" + itemName + "]```")
                except Exception as e:
                    print(e)
                    await client.send_message(message.channel, "Couldn\'t find the item you were looking for. Type \"Mega Inventory\" to see your items.")
            else:
                await client.send_message(message.channel, "What would you like to unequip? Type \"Mega Inventory\" to see your items.")
        except Exception as e:
            print (e)
            await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")
    if usermessage.startswith('MEGA INSPECT'):
        if len(usermessage.split()) >= 3:
            user = subStringAfter("inspect")
        else:
            user = usertoken
        try:
            msg = inspectEquipment(user)
            await client.send_message(message.channel, msg)
        except Exception as e:
            print(e)
            if len(usermessage.split()) >= 3:
                await client.send_message(message.channel, "Could not find the hero you were trying to inspect.")
            else:
                await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")
    if usermessage.startswith('MEGA TRAIN'):
        try:
            updateHealth(usertoken)
            findUserData(usertoken)
            if userData["heroRunning"] == "no":
                stillRunning = "yes"
                updateCharacter("heroRunning", "yes", usertoken)
                while stillRunning == "yes":
                    updateHealth(usertoken)
                    findUserData(usertoken)
                    healthlost = round(random.uniform(30 + (10 * int(userData["heroLevel"])), 40 + (10 * int(userData["heroLevel"]))) - (.25 * int(userData["heroArmor"])))
                    newHealth = int(userData["heroCurrentHealth"]) - int(healthlost)
                    if int(newHealth) <= int(0):
                        failedAttempt(usertoken)
                        await client.send_message(message.channel, usertoken + '```Try as you might, you were too weary and collapsed during training.\nRest up before training again!```')
                        stillRunning = "no"
                        updateCharacter("heroRunning", "no", usertoken)
                        break
                    else:
                        gold = goldGained(1,3,usertoken)
                        updateCharacter("EXP", str((int(userData["heroEXP"]) + 1)), usertoken)
                        updateCharacter("heroCurrentHealth", str(newHealth), usertoken)
                        msg = usertoken + "```You succesfully completed your training and lost " + str(healthlost) + " health.\nYou gained 1 EXP and earned " + str(gold) + " gold.\nWould you like to train or rest up?"
                        additive = levelUp(usertoken)
                        if additive != None:
                            msg = msg + "\n" + additive
                            additive = None
                        else:
                            msg += "```"
                        reloop = await client.send_message(message.channel, msg)
                        await client.add_reaction(reloop, '💤')
                        await client.add_reaction(reloop, '⚔')
                        res = await client.wait_for_reaction(['💤', '⚔'], user=message.author, message=reloop, timeout = 20)
                        try:
                            userReaction = '{0.reaction.emoji}'.format(res)
                            if userReaction == "⚔":
                                await client.delete_message(reloop)
                                stillRunning = "yes"
                                updateCharacter("heroRunning", "yes", usertoken)
                            elif userReaction == "💤":
                                stillRunning = "no"
                                updateCharacter("heroRunning", "no", usertoken)
                                await client.send_message(message.channel, "```You chose to rest up and train another day.```")
                                break
                        except Exception as e:
                            print(e)
                            stillRunning = "no"
                            updateCharacter("heroRunning", "no", usertoken)
                            await client.send_message(message.channel, "```After contemplating for awhile, you chose to rest up and train another day.```")
                            break
                        userReaction = ""
            else:
                await client.send_message(message.channel, usertoken + ", you're already training or running a dungeon!")
        except Exception as e:
            print(e)
            await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")
    if usermessage.startswith('MEGA DUEL'):
        duelInit = usertoken
        duelRecip = subStringAfter("duel")
        if duelInit == duelRecip:
            await client.send_message(message.channel, "You cannot duel yourself!")
        else:
            try:
                findUserData(duelInit)
                if int(userData["heroCurrentHealth"]) < int(int(userData["heroMaximumHealth"]) * .1):
                    await client.send_message(message.channel, duelInit + "You\'re far too weary to duel! Rest up before initiating duels.")
                else:
                    try:
                        duelBegan = False
                        findUserData(duelRecip)
                        if findDuelData(duelInit, "duelRecip") == None and findDuelData(duelInit, "duelInit") == None: #If not challenged or challenger
                            insertIntoDuelData(duelInit, duelRecip)
                        elif findDuelData(duelInit, "duelRecip") == None and findDuelData(duelInit, "duelInit") != None: #If not challenged or but challenger
                            updateDuelData("duelRecip", duelRecip, duelInit)
                        elif findDuelData(duelInit, "duelRecip") != None and findDuelData(duelInit, "duelInit") != None: #If challenged and challenger
                            duelBegan = True
                            deleteFromDuelData(duelInit)
                            deleteFromDuelData(duelRecip)
                        elif findDuelData(duelInit, "duelRecip") != None and findDuelData(duelInit, "duelInit") == None: #If challenged but not challenger
                            duelBegan = True
                            deleteFromDuelData(duelRecip)
                        if duelBegan == True: #Check if duel began
                            duelInitRoll = 0
                            duelRecipRoll = 0
                            while duelInitRoll == duelRecipRoll:
                                print()
                    except Exception as e:
                        print(e)
                        await client.send_message(message.channel, 'The user you challenged does not have a character.')
            except Exception as e:
                print(e)
                await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")

    
    if usermessage.startswith('MEGA RESET'):
        cursor.execute("update azerothheroes set heroRunning = 'no';")
        conn.commit()
    if usermessage.startswith('MEGA DELETE'):
        try:
            findUserData(usertoken)
            await client.send_message(message.channel, usertoken + ', are you sure you want to delete your hero? This cannot be undone.\nType in \"I wish to delete my hero\".')
        except Exception as e:
            print(e)
            await client.send_message(message.channel, 'You do not have a character. Type "Mega Create Hero" to start your journey.')
    if usermessage.startswith('I WISH TO DELETE MY HERO'):
        try:
            findUserData(usertoken)
            cursor.execute("DELETE FROM AzerothHeroes WHERE userID = '" + usertoken + "';")
            conn.commit()
            await client.send_message(message.channel, 'Your hero has been destroyed. Type "Mega Create Hero" to start your journey.')
        except Exception as e:
            print(e)
            await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")
    if usermessage.startswith('MEGA RESTART'):
        await client.send_message(message.channel, 'Systems integrity damaged. Shutting d-down...')
        quit()
    conn.close()
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Mega Help'))
client.run(TOKEN)