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
    shopData = {}
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
        userData["heroHelm"] = tempdata[4]
        userData["heroShoulders"] = tempdata[5]
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
        userData["DMLockout"] = tempdata[28]
        userData["heroRunning"] = tempdata[29]
    def findItemData(itemID):
        if itemID[0].isdigit() or itemID[:3] == "o->":
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
        itemData["sellValue"] = tempdata[10]
    def pullUpInventory(userID):
        findUserData(userID)
        parseItems = userData["heroInventory"].split()
        outMsg = userID + "'s items:```ini\n"
        for i in parseItems:
            findItemData(i)
            if len(itemData["itemName"]) > 0:
                outMsg += "[" + itemData["itemName"] + "]"
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
            if int(itemData["sellValue"]) > 0:
                outMsg += "\nSell value: " + itemData["sellValue"]
            outMsg += "\n\n"
            itemData.clear()
        outMsg += "```"
        return outMsg
    def inspectEquipment(userID):
        findUserData(userID)
        parseItems = [userData["heroHelm"],userData["heroShoulders"],userData["heroChest"],userData["heroGloves"],userData["heroBelt"],userData["heroLegs"],userData["heroFeet"],userData["heroMH"],userData["heroOH"]]
        outMsg = userID + "'s equipment:```ini\n"
        x = 0
        for i in parseItems:
            if i != "0":
                findItemData(i)
                if len(itemData["itemName"]) > 0:
                    outMsg += "\n[" + itemData["itemName"] + "]"
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
            execution = "SELECT * FROM AzerothHeroesDuels WHERE " + whom + " = '" + userID + "';"
            print (execution)
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
    def findShopData(itemID, shop):
        if itemID[0].isdigit() or itemID[:3] == "o->":
            cursor.execute("SELECT * FROM " + shop + " WHERE itemID = '" + itemID + "';")
        else:
            cursor.execute("SELECT * FROM " + shop + " WHERE itemName = '" + itemID + "';")
        conn.commit()
        tempdata = []
        query = cursor.fetchall()
        for row in query:
            for col in row:
                tempdata.append("%s" % col)
        shopData["itemName"] = tempdata[0]
        shopData["itemCost"] = tempdata[1]
        shopData["itemID"] = tempdata[2]
        shopData["itemClass"] = tempdata[3]
    def displayShopData(shop, userID):
        findUserData(userID)
        cursor.execute("SELECT itemID FROM " + shop + " WHERE itemClass = '" + userData["heroClass"] + "' OR itemClass = 'all';")
        conn.commit()
        query = cursor.fetchall()
        tempdata = []
        for row in query:
            for col in row:
                tempdata.append("%s" % col)
        parseItems = tempdata
        outMsg = ""
        for i in parseItems:
            try:
                findItemData(i)
                findShopData(i, shop)
            except:
                print("error here")
            if len(itemData["itemName"]) > 0:
                outMsg += "[" + itemData["itemName"] + "]"
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
            outMsg += "\nCost: " + shopData["itemCost"]
            outMsg += "\n\n"
            itemData.clear()
        return outMsg

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
                outMsg += "Strength!"
                updateCharacter("heroStr", str(newStr), userID)
            elif userData["heroClass"] == "mage":
                newInt = int(userData["heroInt"]) + 1
                outMsg += "Intellect!"
                updateCharacter("heroInt", str(newInt), userID)
            elif userData["heroClass"] == "rogue":
                newAgi = int(userData["heroAgi"]) + 1
                outMsg += "Agility!"
                updateCharacter("heroAgi", str(newAgi), userID)
            updateCharacter("level", str(newLevel), userID)
            updateCharacter("heroMaximumHealth", str(newMH), userID)
            updateCharacter("heroCurrentHealth", str(newCR), userID)
            updateCharacter("heroStamina", str(newStam), userID)
            updateCharacter("heroCrit", str(newCrit), userID)
            return outMsg
        else:
            return None
    def getUniqueItems(iterable):
        seen = set()
        result = []
        for item in iterable:
            if item not in seen:
                seen.add(item)
                result.append(item)
        return result
    def addItemToInventory(userID, itemID):
        findItemData(itemID)
        findUserData(userID)
        tempinventory = userData["heroInventory"]
        tempinventory += " " + itemData["itemID"]
        templist = []
        for i in tempinventory.split():
            templist.append(i)
        final = ' '.join(str(e) for e in getUniqueItems(templist))
        print (final)
        updateCharacter("heroInventory", final, userID)
    def buyItem(userID, shop, itemID):
        findUserData(userID)
        findShopData(itemID, shop)
        if shopData["itemClass"] != userData["heroClass"] and shopData["itemClass"] != "all":
            return "not for class"
        else:
            if int(shopData["itemCost"]) > int(userData["heroGold"]):
                return "can\'t afford"
            else:
                newInventory = userData["heroInventory"] + " " + shopData["itemID"]
                newGold = int(userData["heroGold"]) - int(shopData["itemCost"])
                updateCharacter("heroGold", str(newGold), userID)
                updateCharacter("heroInventory", str(newInventory), userID)
                return "bought"

    #Functions to update duel data
    def updateDuelData(where, value, userID):
        cursor.execute("UPDATE AzerothHeroesDuels SET " + where + " = '" + value + "' WHERE duelInit = '" + userID + "';")
        conn.commit()
    def insertIntoDuelData(duelInit, duelRecip):
        cursor.execute("INSERT INTO AzerothHeroesDuels (duelInit, duelRecip) VALUES ('" + duelInit + "','" + duelRecip + "');")
        conn.commit()
    def deleteFromDuelData(where):
        cursor.execute("DELETE FROM AzerothHeroesDuels WHERE duelInit = '" + where + "';")
        conn.commit()

    #Functions to facilitate duel math
    def ifCrit(userID):
        findUserData(userID)
        x = randint(1,100)
        if x < int(userData["heroCrit"]):
            return True
        else:
            return False
    def duelRolls(userID):
        updateHealth(userID)
        findUserData(userID)
        if ifCrit(userID) == True:
            duelRoll = 1.2 * (.75 * int(userData["heroLevel"])) * ((1.6 * int(userData["heroCurrentHealth"])) + (.2 * int(userData["heroStr"])) + (.2 * int(userData["heroInt"])) + (.2 * int(userData["heroAgi"])) + (.1 * int(userData["heroArmor"])) + (.3 * (int(userData["heroDamage"])))) * random.uniform(1, 5)
        else:
            duelRoll = (.75 * int(userData["heroLevel"])) * ((1.6 * int(userData["heroCurrentHealth"])) + (.2 * int(userData["heroStr"])) + (.2 * int(userData["heroInt"])) + (.2 * int(userData["heroAgi"])) + (.1 * int(userData["heroArmor"])) + (.3 * (int(userData["heroDamage"])))) * random.uniform(1, 5)
        return duelRoll
    def damageInDuel(damageDealer, damageRecip, crit):
        findUserData(damageDealer)
        damageDone = 0
        if crit == True:
            damageDone = round((1.5 * (1.0 * int(userData["heroLevel"])) * ((.4 * int(userData["heroStr"])) + (.4 * int(userData["heroInt"])) + (.4 * int(userData["heroAgi"])) + (.5 * (int(userData["heroDamage"])))) * random.uniform(2, 6)))
        else:
            damageDone = round(((1.0 * int(userData["heroLevel"])) * ((.4 * int(userData["heroStr"])) + (.4 * int(userData["heroInt"])) + (.4 * int(userData["heroAgi"])) + (.5 * (int(userData["heroDamage"])))) * random.uniform(2, 6)))
        findUserData(damageRecip)
        newHealth = int(userData["heroCurrentHealth"]) - int(damageDone)
        if int(newHealth) < 2:
            newHealth = "2"
        updateCharacter("heroCurrentHealth", str(newHealth), damageRecip)
        return damageDone
    def duelGoldTransfer(goldLoser, goldWinner):
        findUserData(goldLoser)
        goldTransfered = int(math.ceil(int(userData["heroGold"]) / 2))
        updateCharacter("heroGold", str(int(userData["heroGold"]) - goldTransfered), goldLoser)
        findUserData(goldWinner)
        updateCharacter("heroGold", str(int(userData["heroGold"]) + goldTransfered), goldWinner)
        return goldTransfered
    def duelDecider(winner, loser):
        damageDone = ""
        if ifCrit(loser) == True:
            damageDone = damageInDuel(loser, winner, True)
        else:
            damageDone = damageInDuel(loser, winner, False)
        goldTransfered = duelGoldTransfer(loser, winner)
        failedAttempt(loser)
        findUserData(winner)
        initName = userData["heroName"]
        initClass = userData["heroClass"]
        findUserData(loser)
        recipName = userData["heroName"]
        msg = ""
        if initClass == "warrior":
            msg = "```" + initName + " slashes through " + recipName + "'s armor and cuts them to pieces, winning the duel!"
        elif initClass == "mage":
            msg = "```" + initName + " burns " + recipName + " to a crisp until there's nothing but ashes, winning the duel!"
        elif initClass == "rogue":
            msg = "```" + initName + " gouges past " + recipName + "'s armor until they to death and winning the duel!"
        msg +="\n\n" + recipName + " hands over " + str(goldTransfered) + " gold to " + initName + ".\n\n" + initName + " lost " + str(damageDone) + " health.```"
        return msg
    
    #Functions to facilitate dungeon math
    def bossDamage(min, max, userID):
        findUserData(userID)
        heroRoll = round(random.uniform(min,max) - ((1 * int(userData["heroLevel"])) * ((.4 * int(userData["heroStr"])) + (.8 * int(userData["heroInt"])) + (.5 * int(userData["heroAgi"])) + (.35 * int(userData["heroArmor"])) + (.6 * (int(userData["heroDamage"]))))))
        return heroRoll
    def didSucceded(min, max, userID):
        damageTaken = bossDamage(min, max, usertoken)
        currentHealth = int(userData["heroCurrentHealth"]) - damageTaken
        if currentHealth <= 0:
            failedAttempt(userID)
            return False
        else:
            updateCharacter("heroCurrentHealth", str(currentHealth), userID)
            return True
    def rollrewards(userID, goldMin, goldMax, EXP, lootChance, **kwargs):
        findUserData(userID)
        goldEarned = goldGained(goldMin, goldMax, userID)
        newEXP = int(userData["heroEXP"]) + EXP
        updateCharacter("EXP", str(newEXP), userID)
        levelUp(userID)
        x = randint(1,100)
        output = "You've received " + str(EXP) + " EXP and looted " + str(goldEarned) + " gold."
        loot = ""
        if x <= lootChance:
            if userData["heroClass"] == "warrior":
                loot = kwargs.get('warriorloot')
            if userData["heroClass"] == "mage":
                loot = kwargs.get('mageloot')
            if userData["heroClass"] == "rogue":
                try:
                    loot = kwargs.get('rogueOH')
                    MHorOH = randint(1,2)
                    if MHorOH == 1:
                        loot = kwargs.get('rogueloot')
                    else:
                        loot = kwargs.get('rogueOH')
                except Exception as e:
                    print(e)
                    loot = kwargs.get('rogueloot')
            findItemData(loot)
            addItemToInventory(userID, loot)
            output += "\nYou received loot: [" + itemData["itemName"] + "]."
        return output
    def updateDMLockout(userID, lockout, index):
        findUserData(userID)
        splitLockout = list(userData["DMLockout"])
        if userData["heroMH"] == "0" and userData["heroOH"] == "0":
            splitLockout[index] = "H"
        else:
            splitLockout[index] = "X"
        newLockout = "".join(splitLockout)
        updateCharacter("DMLockout", newLockout, userID)
        return newLockout
    def worldFirst(userID):
        cursor.execute("SELECT * FROM worldFirstVC;")
        conn.commit()
        query = cursor.fetchall()
        tempdata = []
        for row in query:
            for col in row:
                tempdata.append("%s" % col)
        ifKilled = tempdata[0]
        print(ifKilled)
        if ifKilled == "no":
            findUserData(userID)
            cursor.execute("UPDATE worldFirstVC SET killed = 'yes';")
            conn.commit()
            outMsg = userID + "```ini\nCongratulations, you\'re the first to kill Hardmode Edwin VanCleef!\n\nYou were rewarded: ["
            loot = ""
            loot2 = ""
            if userData["heroClass"] == "warrior":
                loot = "87"
            if userData["heroClass"] == "mage":
                loot = "88"
            if userData["heroClass"] == "rogue":
                loot = "89"
                loot2 = "93"
            addItemToInventory(userID, loot)
            findItemData(loot)
            outMsg += itemData["itemName"] + "]"
            if loot2 != "":
                addItemToInventory(userID, loot2)
                findItemData(loot2)
                outMsg += " and [" + itemData["itemName"] + "]"
            outMsg += "\n\nAll will fear the name " + userData["heroName"] + ".```"
            return outMsg    
        else:
            print()
    
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
            dispHelm = userData['heroRace'] + userData['heroHelm']
            dispShoulder = userData['heroRace'] + userData['heroShoulders']
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
            canvas.paste(chest, heroOffSet, mask=chest)
            canvas.paste(helmet, heroOffSet, mask=helmet)
            canvas.paste(shoulders, heroOffSet, mask=shoulders)
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
                    print (userData[itemData["itemSlot"]])
                    if str(userData[itemData["itemSlot"]]) == "0":
                        equipGear(usertoken, name)
                        await client.send_message(message.channel, usertoken + "```ini\nYou succesfully equipped [" + name + "]```")
                    else:
                        equipGear(usertoken, name, unequip = userData[itemData["itemSlot"]])
                        findItemData(userData[itemData["itemSlot"]])
                        await client.send_message(message.channel, usertoken + "```ini\nYou succesfully replaced [" + itemData["itemName"] + "] with [" + name + "]```")
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
                    await client.send_message(message.channel, usertoken + "```ini\nYou succesfully unequipped [" + itemName + "]```")
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
                        await client.send_message(message.channel, usertoken + usertoken + '```Try as you might, you were too weary and collapsed during training.\nRest up before training again!```')
                        stillRunning = "no"
                        updateCharacter("heroRunning", "no", usertoken)
                        break
                    else:
                        gold = goldGained(1,3,usertoken)
                        updateCharacter("EXP", str((int(userData["heroEXP"]) + 1)), usertoken)
                        updateCharacter("heroCurrentHealth", str(newHealth), usertoken)
                        additive = levelUp(usertoken)
                        if additive != None:
                            msg = usertoken + "```You succesfully completed your training and lost " + str(healthlost) + " health.\n\nYou gained 1 EXP and earned " + str(gold) + " gold.\n\n" + additive + "\n\nNow standing at " + str(newHealth) + " health remaining, would you like to train or rest up?```"
                            additive = None
                        else:
                            msg = usertoken + "```You succesfully completed your training and lost " + str(healthlost) + " health.\n\nYou gained 1 EXP and earned " + str(gold) + " gold.\n\nNow standing at " + str(newHealth) + " health remaining, would you like to train or rest up?```"
                        reloop = await client.send_message(message.channel, msg)
                        await client.add_reaction(reloop, '💤')
                        await client.add_reaction(reloop, '⚔')
                        res = await client.wait_for_reaction(['💤', '⚔'], user=message.author, message=reloop, timeout = 40)
                        try:
                            userReaction = '{0.reaction.emoji}'.format(res)
                            if userReaction == "⚔":
                                await client.delete_message(reloop)
                                stillRunning = "yes"
                                updateCharacter("heroRunning", "yes", usertoken)
                            elif userReaction == "💤":
                                stillRunning = "no"
                                updateCharacter("heroRunning", "no", usertoken)
                                await client.send_message(message.channel, usertoken + "```You choose to rest up and train another day.```")
                                break
                        except Exception as e:
                            print(e)
                            stillRunning = "no"
                            updateCharacter("heroRunning", "no", usertoken)
                            await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to rest up and train another day.```")
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
                            await client.send_message(message.channel, duelInit + ' has challenged ' + duelRecip + " to a duel.")
                        elif findDuelData(duelInit, "duelRecip") == None and findDuelData(duelInit, "duelInit") != None: #If not challenged or but challenger
                            updateDuelData("duelRecip", duelRecip, duelInit)
                            await client.send_message(message.channel, duelInit + ' has challenged ' + duelRecip + " to a duel.")
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
                                duelInitRoll = duelRolls(duelInit)
                                duelRecipRoll = duelRolls(duelRecip)
                            outMsg = ""
                            if duelInitRoll > duelRecipRoll:
                                outMsg = duelDecider(duelInit, duelRecip)
                            else:
                                outMsg = duelDecider(duelRecip, duelInit)
                            await client.send_message(message.channel, outMsg)
                    except Exception as e:
                        print(e)
                        await client.send_message(message.channel, 'The user you challenged does not have a character.')
            except Exception as e:
                print(e)
                await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")
    if usermessage.startswith('MEGA DEADMINES'):
        try:
            updateHealth(usertoken)
            findUserData(usertoken)
            if userData["heroRunning"] == "yes":
                msg = await client.send_message(message.channel, usertoken + ', you\'re already running a dungeon!')
            else:
                updateCharacter("heroRunning", "yes", usertoken)
                currentlyRunning = "yes"
                currentLockout = userData["DMLockout"]
                initmsg = await client.send_message(message.channel, usertoken + '```You\'ve reached the entrance to The Deadmines, do you wish to enter or flee?```')
                await client.add_reaction(initmsg, '🏃')
                await client.add_reaction(initmsg, '⚔')
                initres = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=initmsg, timeout = 60)
                try:
                    initReaction = '{0.reaction.emoji}'.format(initres)
                    if initReaction == "⚔":
                        if "o->DM" not in userData["heroInventory"]:
                            await client.send_message(message.channel, usertoken + '```You try to open the door, but no matter how hard you try, the door will not budge. It\'s locked, and the key is nowhere in sight.\nOut of the corner of your eye, you catch a glimpse of a merchant, skulking around.\nIn a gruff voice, he barks, ‘Trying to get in there, are we? Not without this here key. You want it? Pay up.’\nYou can view what the merchant sells by typing \'Mega Shop Deadmines\'.```')
                            currentlyRunning = "no"
                            updateCharacter("heroRunning", "no", usertoken)
                        else:
                            userReaction = "⚔"
                            loopmsg = ""
                            returnMsg = ""
                            prevReturn = ""
                            while currentlyRunning == "yes":
                                try:
                                    await client.delete_message(loopmsg)
                                    await client.delete_message(prevReturn)
                                    prevReturn = returnMsg
                                except Exception as e:
                                    prevReturn = returnMsg
                                    print(e)
                                if currentLockout.count("A") == 7: #Rhahk'Zor
                                    loopmsg = await client.send_message(message.channel, usertoken + '```The air here is musty, but you proceed into the damp, dark tunnel.\n\nThe clanging of mining picks starts to get louder and louder. An ogre can be heard mercilessly beating squealing Kobolds.\n\nYou finally reach a room with a giant steel door, and the ogre thug guards it.\n\nYou\'re now face-to-face with Rhahk\'Zor, the mining supervisor. Will you engage him? Or will you flee and live another day?```')
                                    await client.add_reaction(loopmsg, '🏃')
                                    await client.add_reaction(loopmsg, '⚔')
                                    loopres = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=loopmsg, timeout = 60)
                                    try:
                                        userReaction = '{0.reaction.emoji}'.format(loopres)
                                        if userReaction == "⚔":
                                            if didSucceded(300, 330, usertoken) == False:
                                                returnMsg = await client.send_message(message.channel, usertoken + "```Rhahk\'Zor strikes you down with his hammer, cackling as he scoffs, \"Is this best heroes can do? Hah!\"\n\nWith that, your run ends. Rest up before trying again!```")
                                                currentlyRunning = "no"
                                                updateCharacter("heroRunning", "no", usertoken)
                                                break
                                            else:
                                                currentLockout = updateDMLockout(usertoken, userData["DMLockout"], 0)
                                                rewards = rollrewards(usertoken, 6, 10, 2, 15, warriorloot="74",mageloot="75",rogueloot="76")
                                                msg = usertoken + "```ini\nAfter an intense fight, Rhahk'zor goes down! He mutters, \"VanCleef not gonna be happy when he find out!\" with his dying breath.\n\n" + str(rewards) + " Valiant effort, Hero!```"
                                                returnMsg = await client.send_message(message.channel, msg)
                                        else:
                                            currentlyRunning = "no"
                                            updateCharacter("heroRunning", "no", usertoken)
                                            returnMsg = await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                                            break
                                    except Exception as e:
                                        print(e)
                                        currentlyRunning = "no"
                                        updateCharacter("heroRunning", "no", usertoken)
                                        await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to flee and live another day.```")
                                        break
                                elif currentLockout.count("A") == 6: #Sneed
                                    loopmsg = await client.send_message(message.channel, usertoken + '```After dealing with a some inane lackeys, you look up to a giant mechanical shredder.\n\n\"Keep it quick, kid, I ain\'t got all day! Hey, you don\'t look familiar! Doesn\'t matter, get to chopping wood!\"\n\nYou now face Sneed, the lumber supervisor. Will you engage him? Or flee and live another day?```')
                                    await client.add_reaction(loopmsg, '🏃')
                                    await client.add_reaction(loopmsg, '⚔')
                                    loopres = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=loopmsg, timeout = 60)
                                    try:
                                        userReaction = '{0.reaction.emoji}'.format(loopres)
                                        if userReaction == "⚔":
                                            if didSucceded(330, 360, usertoken) == False:
                                                returnMsg = await client.send_message(message.channel, usertoken + "```As Sneed cuts you down, you hear him guffaw, \"Who said you couldn't mix business with pleasure? Now get out of my sight, you buffooning oaf!\"\n\nWith that, your run ends. Rest up before trying again!```")
                                                currentlyRunning = "no"
                                                updateCharacter("heroRunning", "no", usertoken)
                                                break
                                            else:
                                                currentLockout = updateDMLockout(usertoken, userData["DMLockout"], 1)
                                                rewards = rollrewards(usertoken, 8, 12, 2, 15, warriorloot="64",mageloot="65",rogueloot="66")
                                                msg = usertoken + "```ini\nWith all the might you can muster, you rip the Shredder to shreds. Sneed squirms as he says, \"VanCleef can't replace me! I'm Sneed! The... \" and with those words, he breathes his last.\n\n" + str(rewards) + " Well done, Hero, but what formidable foe lies ahead?```"
                                                returnMsg = await client.send_message(message.channel, msg)
                                        else:
                                            currentlyRunning = "no"
                                            updateCharacter("heroRunning", "no", usertoken)
                                            await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                                            break
                                    except Exception as e:
                                        print(e)
                                        currentlyRunning = "no"
                                        updateCharacter("heroRunning", "no", usertoken)
                                        await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to flee and live another day.```")
                                        break
                                elif currentLockout.count("A") == 5: #Gilnid
                                    loopmsg = await client.send_message(message.channel, usertoken + '```As you exit the lumberyard, you walk into a massive room with lava pouring from the ceiling.\n\nYou can hear a goblin yelling, \"What am I paying you for! Oh, wait, I\'m not paying you. HAHAHAHA! Get back to making VanCleef\'s weapons, you halfwit, or you\'re going to regret it!\"\n\nAs you walk down the spiraling ramp, you happen upon the blacksmith supervisor, Gilnid. Will you engage him? Or flee and live another day?```')
                                    await client.add_reaction(loopmsg, '🏃')
                                    await client.add_reaction(loopmsg, '⚔')
                                    await client.add_reaction(loopmsg, '🔴')
                                    loopres = await client.wait_for_reaction(['🏃', '⚔', '🔴'], user=message.author, message=loopmsg, timeout = 60)
                                    try:
                                        userReaction = '{0.reaction.emoji}'.format(loopres)
                                        if userReaction == "⚔":
                                            if didSucceded(360, 390, usertoken) == False:
                                                returnMsg = await client.send_message(message.channel, usertoken + "```Overwhelmed by harvest golems, you\'re shot down by Gilnid as he sneers, \"You're no threat to the Brotherhood! Now leave before you're our next weapon rack!\"\n\nWith that, your run ends. Rest up before trying again!```")
                                                currentlyRunning = "no"
                                                updateCharacter("heroRunning", "no", usertoken)
                                                break
                                            else:
                                                currentLockout = updateDMLockout(usertoken, userData["DMLockout"], 2)
                                                rewards = rollrewards(usertoken, 10, 14, 2, 15, warriorloot="44",mageloot="45",rogueloot="46")
                                                msg = usertoken + "```ini\nPutting up the best fight he can, Gilnid finally falls as he squawks, \"You\'ll never get to VanCleef! Never! Hahaha...\" and dies.\n\n" + str(rewards) + " Save your strength, Hero, for the WORST is yet to come!```"
                                                returnMsg = await client.send_message(message.channel, msg)
                                        elif userReaction == "🔴":
                                            if didSucceded(550, 580, usertoken) == False:
                                                returnMsg = await client.send_message(message.channel, usertoken + "```\"You fiend! You've got no right pushing the self-destruct button!\" an irate voice howls in the distance.\n\nAs the ceiling begins to crumble around you, the air is getting heavier and heavier.\n\nGilnid, furious, gouges you until you can no longer stand.\n\n\"YOU\'VE. GOT. NO. RIGHT. PUSHING. THAT... BUTTON! NEVER COME BACK!\"\n\nWith that, your run ends. Rest up before trying again!```")
                                                currentlyRunning = "no"
                                                updateCharacter("heroRunning", "no", usertoken)
                                                break
                                            else:
                                                currentLockout = updateDMLockout(usertoken, userData["DMLockout"], 2)
                                                rewards = rollrewards(usertoken, 18, 22, 2, 35, warriorloot="14",mageloot="15",rogueloot="16")
                                                msg = usertoken + "```ini\n\"You fiend! You've got no right pushing the self-destruct button!\" an irate voice howls in the distance.\n\nAs the ceiling begins to crumble around you, Gilnid begins to cough as he falls to the ground, unable to breathe.\n\n\"You've... destroyed this place... ruined us all! You\'ll... you'll pay for this! The brotherhood, will... prevail\" he yells before he collapses, lifeless and cold.\n\n" + str(rewards) + " Save your strength, Hero, for the WORST is yet to come!```"
                                                returnMsg = await client.send_message(message.channel, msg)
                                        else:
                                            currentlyRunning = "no"
                                            updateCharacter("heroRunning", "no", usertoken)
                                            await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                                            break
                                    except Exception as e:
                                        print(e)
                                        currentlyRunning = "no"
                                        updateCharacter("heroRunning", "no", usertoken)
                                        await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to flee and live another day.```")
                                        break
                                elif currentLockout.count("A") == 4: #Smite
                                    loopmsg = await client.send_message(message.channel, usertoken + '```Exiting the forge, you walk onto a dock. In the distance, you see a ship.\n\nA deep, commanding voice roars, \"We\'re under attack! A vast, ye swabs! Repel the invaders!\"\n\nStanding at the ramp to the boat, you’re greeted by a massive Tauren.\n\nYou\'re now facing Mr.Smite, VanCleef\'s deckhand. Will you engage him? Or flee and live another day?```')
                                    await client.add_reaction(loopmsg, '🏃')
                                    await client.add_reaction(loopmsg, '⚔')
                                    loopres = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=loopmsg, timeout = 60)
                                    try:
                                        userReaction = '{0.reaction.emoji}'.format(loopres)
                                        if userReaction == "⚔":
                                            if didSucceded(390, 420, usertoken) == False:
                                                returnMsg = await client.send_message(message.channel, usertoken + "```After beating you with his incredible arsenal, Smite simply looks back and spits on you as he walks back on board.\n\nWith that, your run ends. Rest up before trying again!```")
                                                currentlyRunning = "no"
                                                updateCharacter("heroRunning", "no", usertoken)
                                                break
                                            else:
                                                currentLockout = updateDMLockout(usertoken, userData["DMLockout"], 3)
                                                rewards = rollrewards(usertoken, 8, 12, 2, 15, warriorloot="34",mageloot="35",rogueloot="36")
                                                msg = usertoken + "```ini\nAs Mr.Smite duels you to his final breath, he mutters, \"You landlubbers are tougher than I thought. I should have improvised.\"\n\nHe collapses to the floor, and the way to the dock is cleared.\n\n" + str(rewards) + " You think that fight was difficult? Just you wait...```"
                                                returnMsg = await client.send_message(message.channel, msg)
                                        else:
                                            currentlyRunning = "no"
                                            updateCharacter("heroRunning", "no", usertoken)
                                            await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                                            break
                                    except Exception as e:
                                        print(e)
                                        currentlyRunning = "no"
                                        updateCharacter("heroRunning", "no", usertoken)
                                        await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to flee and live another day.```")
                                        break
                                elif currentLockout.count("A") == 3: #Cookie
                                    loopmsg = await client.send_message(message.channel, usertoken + '```Walking on board, you\'re quickly greeted with the sound of rushing footsteps and chaotic shouting.\n\nYou hear a murloc gurgling in the distance. Could it be? Cookie and his gang have caught up to you!\n\n\"Mrglgrglglrlgl!\" he says, with a rolling pin in hand.\n\nYou now face Cookie, the chef of the Brotherhood. Will you engage him? Or flee and live another day?```')
                                    await client.add_reaction(loopmsg, '🏃')
                                    await client.add_reaction(loopmsg, '⚔')
                                    loopres = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=loopmsg, timeout = 60)
                                    try:
                                        userReaction = '{0.reaction.emoji}'.format(loopres)
                                        if userReaction == "⚔":
                                            if didSucceded(420, 450, usertoken) == False:
                                                returnMsg = await client.send_message(message.channel, usertoken + "```As Cookie finishes beating you with his rolling pin, he leaves as a gang of bandits come and finish you off.\n\n\"We\'ll use you as an example to the others.\" one says, as he stabs your throat.\n\nWith that, your run ends. Rest up before trying again!```")
                                                currentlyRunning = "no"
                                                updateCharacter("heroRunning", "no", usertoken)
                                                break
                                            else:
                                                currentLockout = updateDMLockout(usertoken, userData["DMLockout"], 4)
                                                rewards = rollrewards(usertoken, 10, 14, 2, 15, warriorloot="44",mageloot="45",rogueloot="46")
                                                msg = usertoken + "```ini\nAs you quickly defeat Cookie, you see a band of thugs run towards you. You hide and avoid them, waiting for the area to clear up.\n\nAfter they\'ve left, you begin making your way up the ship.\n\n" + str(rewards) + " But what other adversaries patrol these mines?```"
                                                returnMsg = await client.send_message(message.channel, msg)
                                        else:
                                            currentlyRunning = "no"
                                            updateCharacter("heroRunning", "no", usertoken)
                                            await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                                            break
                                    except Exception as e:
                                        print(e)
                                        currentlyRunning = "no"
                                        updateCharacter("heroRunning", "no", usertoken)
                                        await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to flee and live another day.```")
                                        break
                                elif currentLockout.count("A") == 2: #Greenskin
                                    loopmsg = await client.send_message(message.channel, usertoken + '```As you clear the path to the top of the ship, you hear a parrot squawk, \"Intruders! Intruders! RAAWK!\"\n\nA goblin mutters as he walks over to you with his crew, now at the top of the ship.\n\n\"You dare step foot on my ship? I\'ll have you skinned!\"\n\nThe goblin pulls out his spear and charges.\n\nYou now face Greenskin, captain of the Deadmines. Will you engage him? Or flee and live another day?```')
                                    await client.add_reaction(loopmsg, '🏃')
                                    await client.add_reaction(loopmsg, '⚔')
                                    loopres = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=loopmsg, timeout = 60)
                                    try:
                                        userReaction = '{0.reaction.emoji}'.format(loopres)
                                        if userReaction == "⚔":
                                            if didSucceded(450, 480, usertoken) == False:
                                                returnMsg = await client.send_message(message.channel, usertoken + "```Greenskin skewers you with his spear, snickering to himself.\n\n\"What did ye hope to accomplish against the cap'n? Win? Pathetic! To Davy Jones's locker with you, imbecile!\"\n\nWith that, your run ends. Rest up before trying again!```")
                                                currentlyRunning = "no"
                                                updateCharacter("heroRunning", "no", usertoken)
                                                break
                                            else:
                                                currentLockout = updateDMLockout(usertoken, userData["DMLockout"], 5)
                                                rewards = rollrewards(usertoken, 12, 16, 3, 15, warriorloot="24",mageloot="25",rogueloot="26")
                                                msg = usertoken + "```ini\nAs you strike down Captain Greenskin, he yells \"VanCleef! They, they have... arrived. The cap'n... didn't make it!\"\n\n" + str(rewards) + " Only one remains; do you dare face the final boss, Hero?```"
                                                returnMsg = await client.send_message(message.channel, msg)
                                        else:
                                            currentlyRunning = "no"
                                            updateCharacter("heroRunning", "no", usertoken)
                                            await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                                            break
                                    except Exception as e:
                                        print(e)
                                        currentlyRunning = "no"
                                        updateCharacter("heroRunning", "no", usertoken)
                                        await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to flee and live another day.```")
                                        break
                                elif currentLockout.count("A") == 1 and currentLockout != "HHHHHHA": #VanCleef
                                    loopmsg = await client.send_message(message.channel, usertoken + '```You\'re finally at the very top of the ship, you see a shadowy figure step out of the captain\'s quarters.\n\n\"None may challenge the Brotherhood, least of all you. You won\'t stop this operation or the Brotherhood. None shall defeat the Brotherhood!\" he sneers.\n\n\"You\'ve slaughtered my entire crew with that weapon, it\'s time I stake it through your heart!\"\n\nYou now stand face-to-face with Edwin VanCleef, leader of the Defias Brotherhood. Will you engage him? Or flee and live another day?```')
                                    await client.add_reaction(loopmsg, '🏃')
                                    await client.add_reaction(loopmsg, '⚔')
                                    loopres = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=loopmsg, timeout = 60)
                                    try:
                                        userReaction = '{0.reaction.emoji}'.format(loopres)
                                        if userReaction == "⚔":
                                            if didSucceded(520, 550, usertoken) == False:
                                                await client.send_message(message.channel, usertoken + "```VanCleef mercilessly cuts you down with his sabers.\n\nHe turns around and smirks as he says, \"You wield such a weapon and still manage to lose? Feeble wretch!\"\n\nWith that, your run ends. How pathetic. Rest up before trying again!```")
                                                currentlyRunning = "no"
                                                updateCharacter("heroRunning", "no", usertoken)
                                                break
                                            else:
                                                currentLockout = updateDMLockout(usertoken, userData["DMLockout"], 6)
                                                rewards = rollrewards(usertoken, 12, 16, 3, 15, warriorloot="84",mageloot="85",rogueloot="86", rogueOH = "92")
                                                VCmsg = await client.send_message(message.channel,usertoken + "```ini\nAfter an intense duel, VanCleef kneels down, dropping to the floor.\n\n\"My death means nothing. This Brotherhood runs deeper than you think. Strike me down, if you will, but know that your actions change nothing!\"\n\n" + str(rewards) + "\n\nVanCleef now lays in front of you, bloodied and bruised. He's too tired to fight and has given up.\n\nThe choice is yours to make.\nDo you kill VanCleef or spare him?```")
                                                await client.add_reaction(VCmsg, '🤝')
                                                await client.add_reaction(VCmsg, '⚔')
                                                VCres = await client.wait_for_reaction(['🤝', '⚔'], user=message.author, message=VCmsg, timeout = 60)
                                                try: 
                                                    VCReaction = '{0.reaction.emoji}'.format(VCres)
                                                    if VCReaction == "⚔":
                                                        await client.send_message(message.channel,usertoken + "```You strike VanCleef down with all your might. The head of Edwin VanCleef rolls around on the floor and off the boat.\n\nThe leader of the Brotherhood is no more.\n\nWith that, your adventure comes to an end. The Deadmines have been rid of all evil, Hero, thanks to your stoic bravery.```")
                                                        currentlyRunning = "no"
                                                        updateCharacter("heroRunning", "no", usertoken)
                                                        break
                                                    else:
                                                        await client.send_message(message.channel,usertoken + "```You reach your hand out to help VanCleef stand up. He glances at you with confusion and distrust in his eyes but hangs his head dejectedly as he accepts your offering.\n\n\"It is not your place to decide whether I live or die. I will return, my forces stronger than ever!\"\n\nVanCleef jumps off the top of the boat, disappearing down below.\n\nWith that, your adventure comes to an end. The Deadmines have been rid of all evil, Hero, thanks to your stoic bravery.```")
                                                        currentlyRunning = "no"
                                                        updateCharacter("heroRunning", "no", usertoken)
                                                        break
                                                except Exception as e:
                                                    await client.send_message(message.channel,usertoken + "```As you stand there contemplating your decision, VanCleef slowly rises. He gazes at you with disdain and cackles.\n\n\"It is not your place to decide whether I live or die. I will return, my forces stronger than ever!\"\n\nVanCleef jumps off the top of the boat, disappearing down below.\n\nWith that, your adventure comes to an end. The Deadmines have been rid of all evil, Hero, thanks to your stoic bravery.```")
                                                    currentlyRunning = "no"
                                                    updateCharacter("heroRunning", "no", usertoken)
                                                    break
                                        else:
                                            currentlyRunning = "no"
                                            updateCharacter("heroRunning", "no", usertoken)
                                            await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                                            break
                                    except Exception as e:
                                        print(e)
                                        currentlyRunning = "no"
                                        updateCharacter("heroRunning", "no", usertoken)
                                        await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to flee and live another day.```")
                                        break
                                elif currentLockout == "HHHHHHA": #VanCleef HM
                                    loopmsg = await client.send_message(message.channel, usertoken + '```You\'re finally at the very top of the ship, you see a shadowy figure step out of the captain\'s quarters.\n\n\"None may challenge the Brotherhood, least of all you. You won\'t stop this operation or the Brotherhood. None shall defeat the Brotherhood!\" he sneers.\n\n\"You\'ve defeated my crew without a weapon? It\'s high time I face a worthy opponent.\"\n\nYou now stand face-to-face with Edwin VanCleef, leader of the Defias Brotherhood. Will you engage him? Or flee and live another day?```')
                                    await client.add_reaction(loopmsg, '🏃')
                                    await client.add_reaction(loopmsg, '⚔')
                                    loopres = await client.wait_for_reaction(['🏃', '⚔'], user=message.author, message=loopmsg, timeout = 60)
                                    try:
                                        userReaction = '{0.reaction.emoji}'.format(loopres)
                                        if userReaction == "⚔":
                                            if didSucceded(520, 550, usertoken) == False:
                                                await client.send_message(message.channel, usertoken + "```VanCleef mercilessly cuts you down with his sabers.\n\nHe turns around and smirks as he says, \"A clean fight, but you're still no match for the Brotherhood!\"\n\nWith that, your run ends. How pathetic. Rest up before trying again!```")
                                                currentlyRunning = "no"
                                                updateCharacter("heroRunning", "no", usertoken)
                                                break
                                            else:
                                                currentLockout = updateDMLockout(usertoken, userData["DMLockout"], 6)
                                                rewards = rollrewards(usertoken, 12, 16, 3, 15, warriorloot="84",mageloot="85",rogueloot="86", rogueOH = "92")
                                                VCmsg = await client.send_message(message.channel,usertoken + "```ini\nAfter an intense duel, VanCleef kneels down, dropping to the floor.\n\n\"A worthy battle. Strike me down, if you will, but know that your actions change nothing!\"\n\n" + str(rewards) + "\n\nVanCleef now lays in front of you, bloodied and bruised. He's too tired to fight and has given up.\n\nThe choice is yours to make.\nDo you kill VanCleef or spare him?```")
                                                await client.add_reaction(VCmsg, '🤝')
                                                await client.add_reaction(VCmsg, '⚔')
                                                VCres = await client.wait_for_reaction(['🤝', '⚔'], user=message.author, message=VCmsg, timeout = 10)
                                                try: 
                                                    VCReaction = '{0.reaction.emoji}'.format(VCres)
                                                    if VCReaction == "⚔":
                                                        await client.send_message(message.channel,usertoken + "```You strike VanCleef down with all your might. The head of Edwin VanCleef rolls around on the floor and off the boat. \n\nThe leader of the Brotherhood is no more.\n\nAfter looking around, you find a key. Inscribed upon it are the words \"The Key to Karazhan.\"\n\nWith that, your adventure comes to an end. The Deadmines have been rid of all evil, Hero, thanks to your stoic bravery.```")
                                                        addItemToInventory(usertoken, "o->KARA")
                                                        currentlyRunning = "no"
                                                        updateCharacter("heroRunning", "no", usertoken)
                                                        await client.send_message(message.channel, worldFirst(usertoken))
                                                        break
                                                    else:
                                                        await client.send_message(message.channel,usertoken + "```You reach your hand out to help VanCleef stand up. He glances at you with confusion and distrust in his eyes, but hangs his head dejectedly as he accepts your offering.\n\n\"It is not your place to decide whether I live or die. I will return, my forces stronger than ever!\"\n\nVanCleef runs off and jumps off the top of the boat, disappearing down below.\n\nWhat's this? It seems he dropped a key as he left. Inscribed upon it are the words \"The Key to Karazhan.\"\n\nWith that, your adventure comes to an end. The Deadmines have been rid of all evil, Hero, thanks to your stoic bravery.```")
                                                        addItemToInventory(usertoken, "o->KARA")
                                                        currentlyRunning = "no"
                                                        updateCharacter("heroRunning", "no", usertoken)
                                                        await client.send_message(message.channel, worldFirst(usertoken))
                                                        break
                                                except Exception as e:
                                                    await client.send_message(message.channel,usertoken + "```As you stand there contemplating your decision, VanCleef slowly rises. He gazes at you with disdain and cackles.\n\n\"It is not your place to decide whether I live or die. I will return, my forces stronger than ever!\"\n\nVanCleef jumps off the top of the boat, disappearing down below.\n\nWhat\'s this? It seems he dropped a key as he left. Inscribed upon it are the words \"The Key to Karazhan.\"\n\nWith that, your adventure comes to an end. The Deadmines have been rid of all evil, Hero, thanks to your stoic bravery.```")
                                                    addItemToInventory(usertoken, "o->KARA")
                                                    currentlyRunning = "no"
                                                    updateCharacter("heroRunning", "no", usertoken)
                                                    await client.send_message(message.channel, worldFirst(usertoken))
                                                    break
                                        else:
                                            currentlyRunning = "no"
                                            updateCharacter("heroRunning", "no", usertoken)
                                            await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                                            break
                                    except Exception as e:
                                        print(e)
                                        currentlyRunning = "no"
                                        updateCharacter("heroRunning", "no", usertoken)
                                        await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to flee and live another day.```")
                                        break
                                elif userReaction == "🏃":
                                    await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                                    currentlyRunning = "no"
                                    updateCharacter("heroRunning", "no", usertoken)
                                    break
                                else: #Dungeon Cleared
                                    await client.send_message(message.channel,usertoken + "```You stroll through the Deadmines, the corpses littering the floor. The Deadmines have been rid of all evil, Hero, thanks to your stoic bravery.```")
                                    currentlyRunning = "no"
                                    updateCharacter("heroRunning", "no", usertoken)
                                    break
                    else:
                        await client.send_message(message.channel, usertoken + '```You flee to live another day.```')
                        currentlyRunning = "no"
                        updateCharacter("heroRunning", "no", usertoken)
                except Exception as e:
                    print(e)
                    currentlyRunning = "no"
                    updateCharacter("heroRunning", "no", usertoken)
                    await client.send_message(message.channel, usertoken + "```After contemplating for awhile, you choose to flee and live another day.```")
        except Exception as e:
            print(e)
            await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")
    if usermessage.startswith('MEGA SHOP DEADMINES'):
        try:
            findUserData(usertoken)
            msg = usertoken + "```ini\nThe shifty-eyed merchant whispers in your direction, looking all around to make sure you're alone.\n\n\"Pssst, you! Commere! I'm not supposed ta be tellin\' ya this, but this mornin\' down at the docks, I overheard that dirty scoundrel VanCleef sayin\' that he dared anyone to enter his mines without a weapon.\n\n\'Nobody in these parts is strong enough to defeat me with his own bare hands,\' he says.\n\nSo whaddya say, pal? Think ya can prove him wrong?\n\nRegardless, have a look at my wares and good luck, Hero. Or should I say... good riddance?\" the merchant taunts, laughing manically with betrayal in his eyes."
            items = displayShopData("AzerothHeroesDMShop", usertoken)
            msg += "\n\n" + items + "To buy an item simply type \"Mega Buy\"```"
            await client.send_message(message.channel, msg)
        except Exception as e:
            print(e)
            await client.send_message(message.channel, 'You do not have a character. Type "Mega Create Hero" to start your journey.')
    if usermessage.startswith('MEGA BUY'):
        try:
            findUserData(usertoken)
            if len(usermessage.split()) >= 3:
                name = subStringAfter("buy")
                try:
                    findItemData(name)
                    try:
                        findShopData(name, "AzerothHeroesDMShop")
                        whatHappened = buyItem(usertoken, "AzerothHeroesDMShop", name)
                        if whatHappened == "bought":
                            await client.send_message(message.channel, "```ini\n\"A pleasure doin\' business with ye!\"\nYou bought item: [" + name + "]```")
                        elif whatHappened == "can\'t afford":
                            await client.send_message(message.channel, "```ini\nThe merchant looks at you and cackles\n\"Yer not buying that with a coin purse that light!\"\nYou couldn\'t afford [" + name + "]```")
                        else:
                            await client.send_message(message.channel, "That item is not for your class.")
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
                    await client.send_message(message.channel, "Couldn\'t find the item you were looking for.")
            else:
                await client.send_message(message.channel, "Type in the name for the item you would like to buy. Example:\nMega Buy Thief Helmet")
        except Exception as e:
            print (e)
            await client.send_message(message.channel, "You do not have a character! Type \"Mega Create Hero\" to start!")

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
    conn.close()
@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name='Mega Help'))
client.run(TOKEN)