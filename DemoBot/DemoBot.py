import asyncio
import discord
from discord.ext import commands
from discord.ext.commands import Bot
import random

# Authroizes bot account with the API.
TOKEN = open("token.txt").read()

# Sets prefix for bot commands in Discord.
bot = commands.Bot(command_prefix='!')

# Hangman global variables.
hangmanActive = False
hangmanDMActive = False
hangmanUserId = 0
hangmanWord = ""
boardFinal = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", "|", "\n"],
               [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", "O", "\n"],
               [" ", " ", " ", " ", " ", "|", " ", " ", " ", "-", "|", "-", "\n"],
               [" ", " ", " ", " ", " ", "|", " ", " ", " ", "/", " ", "\\", "\n"],
               ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]

boardStart = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", " ", "\n"],
               [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", "\n"],
               [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
               [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
               ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]
boardString = "```"
hangmanAttempts = 7
hNewRow = []
hGameWon = False
guessList = []
guesses = ""

# Run the bot.
# @pre TOKEN (token.txt) must have a value.
def run():
    bot.run(TOKEN)
    
# Sets the bot's activity status in Discord.
async def status_task():
    status = "you!"
    await bot.wait_until_ready()
    while not bot.is_closed():
        activity = discord.Activity(name=status, type=discord.ActivityType.listening)
        await bot.change_presence(activity=activity)

# Helper function for an on_message check. Reads from a file and selects a 
# random Youtube link if certain keywords are present in a message.
# @param message A Discord message object.
# @return msg The message to send in the channel the keywords were posted in.
def sleepHelp(message):
    keywords = ["HELP", "ME", "SLEEP"]
    check = True
    msg = ""
    for word in keywords:
        if word not in message.content.upper():
            check = False
    if check:
        bob = random.choice(open("bobross.txt").readlines())
        msg = "Here you go, {0.author.mention}!\n".format(message) + f"Sleep well. :zzz:\n{bob}"  
    return msg           
  
# Decorator assigns this event.        
@bot.event   
# Generic on_message function. Catches any messages in any channel that 
# the bot has access to.
# @param message A Discord message object.
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == bot.user:
        return
    
    if message.content.upper().startswith('WHERE ARE YOU'):
        msg = "I'm right here, {0.author.mention}.".format(message)
        await message.channel.send(msg)
        
    if message.author.bot == False and "HELLO" in message.content.upper() and "DEMO" in message.content.upper():
            msg = ':wave:  Hello, {0.author.mention}!'.format(message) + "  :wave:"
            await message.channel.send(msg)         
            
    if message.author.bot == False and "THANKS" in message.content.upper() and "DEMO" in message.content.upper():
        msg = "No problem, {0.author.mention}.".format(message)
        await message.channel.send(msg)      
        
    if message.author.bot == False and "DEMO" in message.content.upper():
        msg = sleepHelp(message)
        if msg != "":
            await message.channel.send(msg)
            
    if message.author.bot == False and "DEAD" in message.content.upper():
        await message.add_reaction("\U0001F480")
        
    if message.author.bot == False and ("GOODNIGHT" in message.content.upper() or "SLEEP" in message.content.upper()):
        await message.add_reaction("\U0001F4A4")
    
    # This block checks to see if a user is referencing the bot. If they are,
    # This block will take their message and direct it back at the user.
    if message.author.bot == False and "DEMO IS" in message.content.upper():
        #declare our variables & initialize them
        indexDemo = 0 
        indexIs = 0
        i = 0
        newWordList = []
        finalWord = ""
        originalM = message.content.split(" ")
        # Check to see if message is more than just "Demo is"
        if len(originalM) > 2:
            for word in originalM:
                if word.upper() == "DEMO":
                    indexDemo = i
                if word.upper() == "IS":
                    indexIs = i
                i = i + 1
            # reset i
            i = 0
            for word in originalM:
                if i is indexDemo:           
                    while i >= 0:
                        originalM.pop(i)
                        i = i - 1
                    # set i equal to our index for 'Demo'
                    i = 0
                    # add words after 'Demo' to newWordList
                    while i < len(originalM):
                        newWordList.append(originalM[i])
                        i = i + 1
                i = i + 1
            # reset i again           
            i = 0       
            for word in newWordList:
                if word.upper() == "IS":
                    word = "are"
                finalWord = f"{finalWord}{word} " 
            msg = "{0.author.mention} ".format(message) + f"No you {finalWord}"
            await message.channel.send(msg)    
    await bot.process_commands(message)
            
# Decorator assigns this event.   
@bot.event
# Generic on_ready function. Prints status and runs a loop when bot is active.
async def on_ready():
    print('Logged in as: ')
    print("Demobot")
    print(bot.user.id)
    print('---Status---')
    print("Ready!")
    bot.loop.create_task(status_task())

# Creates objects that are capable of rolling either a die with
# user-defined sides or between 1 and some other user-defined number.
class Roll(commands.Cog):
    
    # Decorator assigns this command.  
    @commands.command(name="roll", help="roll a die or a number.")
    async def roll(self, ctx, state : str, limit : int):
        if limit <= 1000000:
            if state == "die" and limit % 2 == 0:
                emojis = {
                          "die"    : ":game_die:",
                          "number" : ":small_blue_diamond:"
                         }
                number = random.randint(1, limit)  
                await ctx.send(f"`Rolling {state.capitalize()}...`")
                await asyncio.sleep(1.2)
                msg = f'{emojis[state]}  You rolled a {str(number)},' + '{0.author.mention}!  '.format(ctx) + f'{emojis[state]}'
                await ctx.send(msg)      
            else:
                await ctx.send("A die has an even number of sides, {0.author.mention}.".format(ctx))
            
bot.add_cog(Roll(bot))

class Math(commands.Cog):
    @commands.Cog.listener()
    async def on_message(message):
        await bot.process_commands(message)
    
    @commands.command(name='factor', help='List all factors of a number up to 6 figures.')
    async def factor(self, ctx):
        num = ctx.message.content.split(" ")
        factors=[]
        i = 1
        k=num[1]
        if len(num[1]) > 6:
            msg = '{0.author.mention}, that number is too large. Python is a interpreted language. It takes time to calculate large numbers because of this. Please choose a smaller number. Consult ~help for the size limit.'.format(ctx)
            await ctx.send(msg)
        while i <= int(k):
            f = int(k) % i
            if f == 0:
                factors.append(i)
            i=i+1
            mes = "`Finding All Factors...`"
        msg = "The factors of " + str(k) + " are: " + str(factors) + ', {0.author.mention}.'.format(ctx)
        await ctx.send(mes)
        await asyncio.sleep(1.2)    
        await ctx.send(msg)
        factors=[]
        
    @commands.command(name='average', help='Finds the average of up to 10 numbers.')
    async def average(self, ctx):
        vals = ctx.message.content.split(" ")
        num=[]
        i = 0
        if len(vals[1]) > 10:
            msg = '{0.author.mention}, that number is too large. Python is \
            a interpreted language. It takes time to calculate large numbers \
            because of this. Please choose a smaller number. Consult ~help \
            for the size limit.'.format(ctx)
            await ctx.send(msg)    
        while i < len(vals)-1:
            num.append(vals[i+1])
            i=i+1
        i = 0
        total = 0
        while i < len(num):
            total = total + int(num[i])
            i=i+1
        total = total / int(len(num))
        mes = "`Calculating Average...`"
        msg = 'The average of those number is ' + str(total) +  ', {0.author.mention}.'.format(ctx)
        await ctx.send(mes)
        await asyncio.sleep(1.2)    
        await ctx.send(msg)
        
    @commands.command(name='percent', help='Finds how much one number is of another number (for grades).')
    async def percentage(self, ctx):
        vals = ctx.message.content.split(" ")
        NumberX = float(vals[1])
        NumberY = float(vals[2])
        
        total = NumberX / NumberY
        per = total * 100
        mes = "`Calculating Percentage...`"
        msg = "The percentage of those two numbers is " + str(per) + '%' + ', {0.author.mention}.'.format(ctx)
        await ctx.send(mes)
        await asyncio.sleep(1.2)    
        await ctx.send(msg)
    
    @commands.command(name='sqrt', help='Find the square root of a number.')
    async def squareRoot(self, ctx):
        vals = ctx.message.content.split(" ")
        NumberX = float(vals[1])
        num = NumberX ** 0.5
        mes = "`Calculating Square Root...`"
        msg = "The square root of " + str(NumberX) + " is " + str(num) + ", {0.author.mention}.".format(ctx)
        await ctx.send(mes)
        await asyncio.sleep(1.2)
        await ctx.send(msg)
    
    @commands.group(name='prime', help='Find prime numbers.')
    async def prime(self, ctx):
        if ctx.invoked_subcommand is None:
                await ctx.send('`Invalid command passed...`')
                
    @prime.command(name='100', help='Find all prime numbers up to one hundred.')
    async def primeOneHundred(self, ctx):
        m = ""
        prime = []
        j = 2
        for i in range(2,100):
            if (j % i) == 0:
                continue
            else:
                prime.append(j)
            j = j + 1
        for num in prime:
            m = m + str(num) + " "
        msg = m
        mes = "`Finding All Prime Numbers...`"
        await ctx.send(mes)
        await asyncio.sleep(1.2)
        await ctx.send("`Prime Numbers from 1-100: `" + msg)
    
    @prime.command(name='200', help='Find all prime numbers up to two hundred.')
    async def primeTwoHundred(self, ctx):
        m = ""
        prime = []
        j = 2
        for i in range(2,200):
            if (j % i) == 0:
                continue
            else:
                prime.append(j)
            j = j + 1
        for num in prime:
            m = m + str(num) + " "
        msg = m
        mes = "`Finding All Prime Numbers...`"
        await ctx.send(mes)
        await asyncio.sleep(1.2)
        await ctx.send("`Prime Numbers from 1-200: `" + msg)
        
    @prime.command(name='isit', help='Check if a number is a prime number.')
    async def primeIsIt(self, ctx, num: int):
        m = ""
        prime = []
        j = 2
        if num <= 10000:
            if num > 1:
                if num == 2:
                    mes = "`Calculating...`"
                    await ctx.send(mes)
                    await asyncio.sleep(.9)
                    await ctx.send("`...`")
                    await asyncio.sleep(1)
                    await ctx.send(":abacus:  Prime!  :abacus:")
                
                for i in range(2, num):
                    if (num % i) == 0:
                        mes = "`Calculating...`"
                        await ctx.send(mes)
                        await asyncio.sleep(.9)
                        await ctx.send("`...`")
                        await asyncio.sleep(1)
                        await ctx.send(":x:  Not Prime!  :x:")
                        break
                    else:
                        mes = "`Calculating...`"
                        await ctx.send(mes)
                        await asyncio.sleep(.9)
                        await ctx.send("`...`")
                        await asyncio.sleep(1)
                        await ctx.send(":abacus:  Prime!  :abacus:")
                        break
    
            else:
                msg = "{0.author.mention}, 1 cannot be a prime number. Please choose a larger number."
                await ctx.send(msg)
            
            
        else:
            msg = '{0.author.mention}, that number is too large. Consult !help for the size limit.'.format(ctx)
            await ctx.send(msg)        
            
    @commands.command(name='midpnt', help='calculate the midpoint of two points.')
    async def midpoint(self, ctx, x1 : int, y1: int, x2: int, y2: int):
        def midpointHelper(num1, num2, num3, num4):
            coordin1Total = (num3 + num1) / 2
            coordin2Total = (num4 + num2) / 2
            if coordin1Total.is_integer():
                coordin1Total = int(coordin1Total)
            if coordin2Total.is_integer():
                coordin2Total = int(coordin2Total)        
            midpoint = '(' + str(coordin1Total) + ', ' + str(coordin2Total) + ')'
            return midpoint
        await ctx.send("`Calculating...`")
        await asyncio.sleep(1)
        await ctx.send(midpointHelper(x1,y1,x2,y2))
        
    @commands.command(name='distance', help="Calculate the distance between two points.")
    async def distance(self, ctx, x1 : int, y1: int, x2: int, y2: int):
        def distanceHelper(num1, num2, num3, num4):
            coordin1Total = (num3 - num1) ** 2
            coordin2Total = (num4 - num2) ** 2
            subTotal = coordin1Total + coordin2Total
            total = math.sqrt(subTotal)
            distance = str(total)
            return distance
        await ctx.send("`Calculating...`")
        await asyncio.sleep(1)
        await ctx.send(distanceHelper(x1,y1,x2,y2)) 
        
    @commands.group(name='area', help='Calculate the area of a 2d shape.')
    async def area(self, ctx):
        if ctx.invoked_subcommand is None:
                await ctx.send('`Invalid command passed...`')
                
    @area.command(name='tri', help='Calculate the area of a triangle.')
    async def areaTriangle(self, ctx, base: float, height: float):
        if base > 10000 or height > 10000:
            await ctx.send("Number is too large.")
        else:
            calculate = (base * height) / 2
            await ctx.send(calculate)
            
    @area.command(name='rec', help='Calculate the area of a rectangle.')
    async def areaRectangle(self, ctx, width: float, height: float):
        if width > 10000 or height > 10000:
            await ctx.send("Number is too large.")
        else:
            calculate = (width * height)
            await ctx.send(calculate)
            
    @area.command(name='squ', help='Calculate the area of a square.')
    async def areaSquare(self, ctx, side: float):
        if side > 10000:
            await ctx.send("Number is too large.")
        else:
            calculate = side ** 2
            await ctx.send(calculate)
            
    @area.command(name='trap', help='Calculate the area of a trapezoid.')
    async def areaTrap(self, ctx, side1: float, side2: float, height: float):
        if side1 > 10000 or side2 > 10000 or height > 10000:
            await ctx.send("Number is too large.")
        else:
            calculate = ((side1 + side2) * height) / 2
            await ctx.send(calculate)
            
    @area.command(name='semi', help='Calculate the area of a semi-circle.')
    async def areaSemiCircle(self, ctx, radius: float):
        if radius > 10000:
            await ctx.send("Number is too large.")
        else:
            calculate = (math.pi * (radius ** 2)) / 2
            await ctx.send(calculate) 
            
    @commands.command(name='quad', help="Find a quadratic equation's X values.")
    async def quad(self, ctx, a : float, b : float, c : float):
        xValues = []
        multiply = (b**2) - 4 * (a * c)
        print(multiply)
        squaring = math.sqrt(multiply)
        if squaring < 0:
            await ctx.send("Factor is an imaginary number.")
        dividing = squaring / (2*a)
        b = b / (2*a)
        add = -1 * b + dividing
        add = round(add, 2)
        xValues.append(add)
        subtract = -1 * b - dividing
        subtract = round(subtract, 2)
        xValues.append(subtract)
        await ctx.send("X values: " + str(xValues))
bot.add_cog(Math(bot))  

'''

Commands can also be implemented without class structure.

'''
    
async def hangmanDMHelper(player : discord.User):
    global hangmanActive
    global hangmanWord
    global hangmanUserId
    global hangmanDMActive
    person = bot.get_user(hangmanUserId)
    
    def check(m):
        global hangmanUserId
        return m.author.id == hangmanUserId
    #no need for timeout argument as wait_for in hangman() handles it
    msg = await bot.wait_for('message', check=check)
    if len(msg.content) > 25:
        await person.send("The word must be under 25 characters.")
    else:
        await person.send("Okay, got it {0.author.mention}.".format(msg))
    hangmanWord = msg.content
    hangmanDMActive = False    

@bot.command(name='hngmn', help='Play a game of Hangman.')
async def hangman(ctx):
    global hangmanActive
    global hangmanUserId
    global hangmanDMActive
    global hangmanWord
    global boardStart
    global boardString
    global hangmanAttempts
    global hNewRow
    await ctx.message.add_reaction("\U0001F579")
    if hangmanActive == True:
        await ctx.send("A game is already active {0.author.mention}.".format(ctx) + " Please finish that game before starting another one.")
        await ctx.send("Attempts left: " + str(hangmanAttempts))
        await ctx.send(boardString)

    if hangmanActive == False:
        hangmanActive = True
        if hangmanDMActive != True:
            hangmanDMActive = True        
        await ctx.send("It's time for some Hangman {0.author.mention}".format(ctx) +  "! Message me the word you would like to use. You have one minute to choose your word. Choose wisely. Call '!guess 'your guess here'' to guess a letter. You can guess spaces by typing 'space' instead of a letter. No hyphens. Good luck!")
        hangmanUserId = ctx.author.id
        user = bot.get_user(hangmanUserId)
        try:
            await asyncio.wait_for(hangmanDMHelper(user), timeout=66.0)
            if len(hangmanWord) > 25:
                return
        except asyncio.TimeoutError:
            await ctx.send("You never sent anything {0.author.mention}!".format(ctx) + " I am going to end the game.")
            print("COMMAND TIMED OUT")
            hangmanActive = False
            hangmanWord = ""
            return
        
        rowToAdd = len(hangmanWord)
        listOfChars = ["_", " ", "\n"]
        
        i = 0
        while i != rowToAdd:
            hNewRow.append(listOfChars[0])
            if i != rowToAdd - 1:
                hNewRow.append(listOfChars[1])
            i = i + 1
        hNewRow.append(listOfChars[2])
        boardStart.append(hNewRow)
        
        for i in range(len(boardStart)):
            for j in range(len(boardStart[i])):
                boardString = boardString + boardStart[i][j]
        boardString = boardString + "```"
        await ctx.send("Attempts left: " + str(hangmanAttempts))
        await ctx.send(boardString)       
        
@bot.command(name='guess', help='Guess a letter in Hangman.')
async def guess(ctx, guess : str):
    global hangmanActive
    global hangmanWord
    global hangmanUserId
    global hangmanDmActive
    global boardStart
    global boardFinal
    global boardString
    global hangmanAttempts
    global hNewRow
    global hGameWon
    global guessList
    global guesses
    place = 0
    checker = False
    letter = ""
    finished = 0
    if hangmanActive == True:
        if len(guess) == 1 or guess == "space":
            guessList.append(guess)
        elif len(guess) > 1:
            guessList.append(guess)
        loop = 0
        if len(guess) == 1 or guess == "space":
            
            while loop < len(hangmanWord):
                if guess == "space":
                    if hangmanWord[loop] == " ":
                        place = loop
                        hNewRow[place + place] = "-"
                        checker = True
                        loop = loop + 1
                        checkUnderscore = True
                        for l in hNewRow:
                            if l == "_":
                                checkUnderscore = False
                                finished = finished + 1
                        #reset finished if there are no underscores left (words to guess)
                        if checkUnderscore == True:
                            finished = 0                
                #if the user guesses a letter
                if guess.lower() == hangmanWord[loop].lower():
                    place = loop
                    checker = True
                    loop = loop + 1
                    if place == 0:
                        #append first letter
                        hNewRow[place] = hangmanWord[place].lower()
                        #check if the word is guessed
                        for l in hNewRow:
                            if l == "_":
                                finished = finished + 1
                            #end if
                        #end for
                    #end if
                    else:

                        #any other letter must account for spaces in hNewRow
                        hNewRow[place+(place)] = hangmanWord[place].lower()
                        #check if the word is guessed
                        checkUnderscore = True
                        for l in hNewRow:
                            if l == "_":
                                checkUnderscore = False
                                finished = finished + 1
                        #reset finished if there are no underscores left (words to guess)
                        if checkUnderscore == True:
                            finished = 0
                    #end else
                else:
                    loop = loop + 1
            #end while
            if checker == True:
                boardStart.pop()
                #rebuild board with new row
                boardStart.append(hNewRow)
                boardString = "```"
                for i in range(len(boardStart)):
                    for j in range(len(boardStart[i])):
                        boardString = boardString + boardStart[i][j]
                boardString = boardString + "```"
                await ctx.send("Attempts left: " + str(hangmanAttempts))
                await ctx.send(boardString)
                await ctx.send("Letters already guessed: " + str(guessList))
                #if word is guessed end the game
                if finished == 0:
                    await ctx.send("You've guessed the word! The game has been won!")
                    hangmanActive = False
                    hangmanDMActive = False
                    hangmanUserId = 0
                    hangmanWord = ""
                    boardFinal = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", "|", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", "O", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", "-", "|", "-", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", "/", " ", "\\", "\n"],
                                   ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]
                    
                    boardStart = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", " ", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
                                   ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]
                    boardString = "```"
                    hangmanAttempts = 7
                    hNewRow = []
                    hGameWon = False
                    guessList = []
                    guesses = ""
                #end if
                                
                #if the user is out of attempts end the game
                
            #end if
            
            #if guess was incorrect
            else:     
                if hangmanAttempts == 7:
                    boardStart[0][10] = boardFinal[0][10]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"

                if hangmanAttempts == 6:
                    boardStart[1][10] = boardFinal[1][10]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"                
                
                if hangmanAttempts == 5:
                    boardStart[2][10] = boardFinal[2][10]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"

                if hangmanAttempts == 4:
                    boardStart[2][9] = boardFinal[2][9]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"
                    
                if hangmanAttempts == 3:
                    boardStart[2][11] = boardFinal[2][11]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"
                    
                if hangmanAttempts == 2:
                    boardStart[3][9] = boardFinal[3][9]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"  
                
                if hangmanAttempts == 1:
                    boardStart[3][11] = boardFinal[3][11]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"                  
                 
                
                hangmanAttempts = hangmanAttempts - 1
                await ctx.send("Attempts left: " + str(hangmanAttempts))
                await ctx.send(boardString) 
                await ctx.send("Letters already guessed: " + str(guessList))                
                    
                if hangmanAttempts == 0:
                    await ctx.send("You are out of attempts! The game is over. The word was " + hangmanWord + ".")
                    hangmanActive = False
                    hangmanDMActive = False
                    hangmanUserId = 0
                    hangmanWord = ""
                    boardFinal = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", "|", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", "O", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", "-", "|", "-", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", "/", " ", "\\", "\n"],
                                   ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]
                    
                    boardStart = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", " ", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
                                   ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]
                    boardString = "```"
                    hangmanAttempts = 7
                    hNewRow = []
                    hGameWon = False
                    guessList = []
                    guesses = ""                    
            #end else
            
        elif len(guess) > 1:
            loop = 0
            counter = 0
            guessWordBuilder = ""
            while loop < len(guess) and loop < len(hangmanWord):
                if guess[loop] == hangmanWord[loop]:
                    guessWordBuilder += hangmanWord[loop]
                    loop += 1
                else:
                    loop += 1
            if guessWordBuilder == hangmanWord:
                await ctx.send("You've guessed the word! The game has been won!")
                hangmanActive = False
                hangmanDMActive = False
                hangmanUserId = 0
                hangmanWord = ""
                boardFinal = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", "|", "\n"],
                               [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", "O", "\n"],
                               [" ", " ", " ", " ", " ", "|", " ", " ", " ", "-", "|", "-", "\n"],
                               [" ", " ", " ", " ", " ", "|", " ", " ", " ", "/", " ", "\\", "\n"],
                               ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]
                
                boardStart = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", " ", "\n"],
                               [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", "\n"],
                               [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
                               [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
                               ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]
                boardString = "```"
                hangmanAttempts = 7
                hNewRow = []
                hGameWon = False
                guessList = []
                guesses = ""
            else:
                if hangmanAttempts == 7:
                    boardStart[0][10] = boardFinal[0][10]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"

                if hangmanAttempts == 6:
                    boardStart[1][10] = boardFinal[1][10]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"                
                
                if hangmanAttempts == 5:
                    boardStart[2][10] = boardFinal[2][10]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"

                if hangmanAttempts == 4:
                    boardStart[2][9] = boardFinal[2][9]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"
                    
                if hangmanAttempts == 3:
                    boardStart[2][11] = boardFinal[2][11]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"
                    
                if hangmanAttempts == 2:
                    boardStart[3][9] = boardFinal[3][9]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"  
                
                if hangmanAttempts == 1:
                    boardStart[3][11] = boardFinal[3][11]
                    boardString = "```"
                    for i in range(len(boardStart)):
                        for j in range(len(boardStart[i])):
                            boardString = boardString + boardStart[i][j]
                    boardString = boardString + "```"                  
                 
                
                hangmanAttempts = hangmanAttempts - 1
                await ctx.send("Attempts left: " + str(hangmanAttempts))
                await ctx.send(boardString)  
                await ctx.send("Letters already guessed: " + str(guessList))                
                    
                if hangmanAttempts == 0:
                    await ctx.send("You are out of attempts! The game is over. The word was " + hangmanWord + ".")
                    hangmanActive = False
                    hangmanDMActive = False
                    hangmanUserId = 0
                    hangmanWord = ""
                    boardFinal = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", "|", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", "O", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", "-", "|", "-", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", "/", " ", "\\", "\n"],
                                   ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]
                    
                    boardStart = [ [" ", " ", " ", " ", " ", "|", "─", "─", "─", "─", " ", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
                                   [" ", " ", " ", " ", " ", "|", " ", " ", " ", " ", " ", " ", "\n"],
                                   ["_", "_", "_", "_", "_", "|", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "_", "\n"]]
                    boardString = "```"
                    hangmanAttempts = 7
                    hNewRow = []
                    hGameWon = False
                    guessList = []
                    guesses = ""     
        else:
            await ctx.send("You must enter a letter.")        
    else:
        await ctx.send("You need to start a game first with '~hngmn'!") 

def main():
    run()
main()

    
