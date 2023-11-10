import random
import interactions
from interactions import ActionRow, Button

bot = interactions.Client(token="MTE1Mjc4NTUyOTAzNzkzNDY2Mg.GK5yJS.pgXdZ9l0jSBCgwMoI4gxX-Aq_CavRe2wD67jsM")

rockpaperscissors = ["rock","newspaper","scissors"]

rockButton = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Rock",
    custom_id="rock",
    )

paperButton = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Paper",
    custom_id="newspaper",
)
scissorsButton = interactions.Button(
    style=interactions.ButtonStyle.PRIMARY,
    label="Scissors",
    custom_id="scissors"
)


row = interactions.ActionRow(
    components=[rockButton,paperButton,scissorsButton]
)

@bot.command(
    name="rockpaperscissors",
    description="Play a Rock newspaper Scissors game!",
    scope=1152789940040642560,
)
async def RockPaperScissors(ctx: interactions.CommandContext):
    
    await ctx.send("Hi there!", components=row)

async def Win(ctx, human_sign, bot_sign):
    print("lmaooooo /n crazy")
    await ctx.send("Player: :" + human_sign + ":\n" + "Bot: :" + bot_sign + ":\n" + "Hahah! I win!")
async def Lose(ctx, human_sign, bot_sign):
    await ctx.send("Player: :" + human_sign + ":\n" + "Bot: :" + bot_sign + ":\n" + "Awh.. I lost! \n :pensive:")

async def match_up(ctx, human_sign, bot_sign):
    if human_sign == bot_sign:
        await ctx.send("Tied! Choose again!", components=row)
    if human_sign == "rock" and bot_sign == "newspaper":
        await Win(ctx, human_sign, bot_sign)
    if human_sign == "rock" and bot_sign == "scissors":
        await Lose(ctx, human_sign, bot_sign)
    if human_sign == "newspaper" and bot_sign == "rock":
        await Lose(ctx, human_sign, bot_sign)
    if human_sign == "newspaper" and bot_sign == "scissors":
        await Win(ctx, human_sign, bot_sign)
    if human_sign == "scissors" and bot_sign == "rock":
        await Win(ctx, human_sign, bot_sign)
    if human_sign == "scissors" and bot_sign == "newspaper":
        await Lose(ctx, human_sign, bot_sign)

async def choose_player(ctx, human_sign):
    player = random.choice(rockpaperscissors)
    await match_up(ctx, human_sign, player)
    

@bot.component("scissors")
async def scissors_component(ctx: interactions.ComponentContext):
    await ctx.send("Scissors!")
    await choose_player(ctx,rockpaperscissors[2])
    await ctx.send("Scissors passed!")
@bot.component("rock")
async def rock_component(ctx: interactions.ComponentContext):
    await choose_player(ctx, rockpaperscissors[0])
@bot.component("newspaper")
async def paper_component(ctx: interactions.ComponentContext):
    await choose_player(ctx,rockpaperscissors[1])

    


bot.start()