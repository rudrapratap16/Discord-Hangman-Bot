import discord
import random
from discord.ext import commands

from hangman_drawing import *
from words import *
from api_key import TOKEN


thing = random.randrange(0,2)
thing_inside = random.randrange(0,10)

turn = 0
user_moves=[]
selected_word = ""
game_ind = 0
show_msg=""
wrong_move = -1
answer = ""

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

@bot.event
async def on_member_join(ctx):
    embed = discord.Embed(
        title="Welcome to the Server",
        description="You can access the bot by typing >help\nYou can play Hangman game by typing >game"
    )
    await ctx.send(embed=embed)

@bot.command()
async def game(ctx):
    reset()
    global selected_word, show_msg, answer, game_ind
    game_ind = 1
    key = list(words.keys())
    show_msg = ""
    selected_word = words[key[thing]][thing_inside]
    answer = selected_word[:]
    print(selected_word)
    for i in range(len(selected_word)):
        show_msg+="⬜"
    await ctx.channel.purge()
    await ctx.send("Game Started, Use > word (word) as format to give answer\nThe word is of category : " + key[thing])
    embed_msg = discord.Embed(
        title=f"{show_msg} is the Word."
    )
    await ctx.send(embed=embed_msg)

@bot.event
async def on_member_update(before, after):
    if after.status.name == 'online':
        embed = discord.Embed(
            title="Welcome Back",
            description="In order to play hangman, type >game"
        )
        await bot.get_channel('1271789727309103145').send(embed=embed)

@bot.command
async def end(ctx):
    await ctx.channel.purge()

@bot.command()
async def clear(ctx):
    await ctx.channel.purge()

@bot.command()
async def word(ctx, msg: str):
    global show_msg, turn, selected_word, game_ind, user_moves, wrong_move, answer
    msg = msg.upper()[0]
    print(msg, game_ind)
    await ctx.channel.purge(limit=3)
    
    if game_ind == 1:
        turn += 1
        if msg in selected_word:
            idx = selected_word.index(msg)
            selected_word = list(selected_word)
            selected_word[idx] = msg
            selected_word = "".join(selected_word)
            selected_word = selected_word.replace(msg, "!", 1)

            show_msg = list(show_msg)
            show_msg[idx] = msg
            show_msg = "".join(show_msg)
            user_moves.append(msg)

            if len(user_moves) == len(selected_word):
                await ctx.send(f"You Won, The word was {show_msg}.\nRestart game by Typing >game")
                reset()
                return
            else:
                if wrong_move == -1:
                    embed = discord.Embed(
                        title=HANGMANPICS[0]
                    )
                else:
                    embed = discord.Embed(
                        title=HANGMANPICS[wrong_move]
                    )
                turn-=1
                await ctx.send(f"{show_msg}, {turn} out of 8 turns done")
                await ctx.send(embed=embed)
        
        elif game_ind == 1 and turn >= 8:
            wrong_move+=1
            embed = discord.Embed(
                    title=HANGMANPICS[wrong_move]
                )
            await ctx.send(embed=embed)
            await ctx.send(f"You Lost, The Word was {answer}.\nRestart game by Typing >game")
            reset()

        else:
            wrong_move+=1
            embed = discord.Embed(
                    title=HANGMANPICS[wrong_move]
                )
            await ctx.send(embed=embed)
            await ctx.send(f"{show_msg}, Wrong word, {turn} out of 8 turns done")

def reset():
    global show_msg, turn, selected_word, game_ind, user_moves, thing, thing_inside, wrong_move, answer
    user_moves=[]
    selected_word = ""
    game_ind = 0
    show_msg = "⬜⬜⬜⬜"
    turn = 0
    wrong_move = -1
    answer = ""
    thing = random.randrange(0,2)
    thing_inside = random.randrange(0,10)
    

bot.run(TOKEN)
