import os
from random import randint
from dotenv import load_dotenv
from discord import Intents, Client

load_dotenv()

token = str(os.environ["CARD_BOT_TOKEN"])
guild_id = int(os.environ["GUILD_ID"])

bot_channel_id = int(os.environ["BOT_CHANNEL_ID"])
card_2f_channel_id = int(os.environ["CARD_2F_CHANNEL_ID"])
attendance_channel_id = int(os.environ["ATTENDANCE_CHANNEL_ID"])
door_channel_id = int(os.environ["DOOR_CHANNEL_ID"])
rule_channel_id = int(os.environ["RULE_CHANNEL_ID"])
y2023_channel_id = int(os.environ["Y2023_CHANNEL_ID"])

in_role_id = int(os.environ["IN_ROLE_ID"])
card_2f_role_id = int(os.environ["CARD_2F_ROLE_ID"])
trial_joining_role_id = int(os.environ["TRIAL_JOINING_ROLE_ID"])


intents = Intents.default()
intents.members = True
intents.message_content = True
intents.presences = True

client = Client(intents=intents)

card_can_take = True

@client.event
async def on_ready():
    print(f"カードキーちゃん が起動しました")
    global card_can_take
    for guild in client.guilds:
        for role in guild.roles:
            if (role.id == card_2f_role_id) and not (role.members == []):
                card_can_take = False

@client.event
async def on_member_join(member):
    trial_joining_role = member.guild.get_role(trial_joining_role_id)
    await member.add_roles(trial_joining_role)
    lst = [f"ハーイ、<@{member.id}>！RAISON DȆTREへようこそ！\nまずは落ち着いて、**<#{y2023_channel_id}>**を確認してください……", 
           f"あなたなのね、<@{member.id}>！RAISON DȆTREへおいで……\nさっそく**<#{y2023_channel_id}>**をチェックしましょう！", 
           f"ドゥクシ！<@{member.id}>！RAISON DȆTREへようこそ！\nほら、**<#{y2023_channel_id}>**を見ようよ！", 
           f"<@{member.id}>！ここがRAISON DȆTREさ……！\n見るんだ！**<#{y2023_channel_id}>**を！さあ！", 
           f"お目にかかれて光栄です……<@{member.id}>さん。\nまずは**<#{y2023_channel_id}>**をご覧ください。", 
           f"私は汎用AIのロール……RAISON DȆTREへようこそ、<@{member.id}>さん。\n説明のために、**<#{y2023_channel_id}>**をご覧ください。",
           f"ウホッウホッ！<@{member.id}>！ウホッ！！🍌🍌\nウホホ！**<#{y2023_channel_id}>**！ウホッ！🍌", 
           ]
    for channel in client.get_all_channels():
        if channel.id == door_channel_id:
            idx = randint(-5, 99) 
            if (idx < 0):
                idx = 6
            else:
                idx %= 6
            await channel.send(lst[idx])
            break

@client.event
async def on_message(message):
    global card_can_take

    is_bot_channel = (message.channel.id == bot_channel_id)
    is_attendance_channel = (message.channel.id == attendance_channel_id)
    is_2f_cardkey_channel = (message.channel.id == card_2f_channel_id)

    in_role = message.guild.get_role(in_role_id)
    card_2f_role = message.guild.get_role(card_2f_role_id)

    inlike_words = {"in", "いn", "un", "on", "im", "inn",
                    "いｎ", "ｉｎ", "いん", "イン", "ｲﾝ", "ｉｎｎ"}
    outlike_words = {"out", "put", "iut", "おうt", "auto", "ａｕｔｏ",
                     "おうｔ", "our", "ｏｕｔ", "あうと", "アウト", "ｱｳﾄ"}
    takelike_words = {"take", "ｔａｋｅ", "たけ", "タケ", "ﾀｹ", "rake", "竹", "ねいく", 
                        "ていく", "テイク", "ﾃｲｸ", "teiku", "ｔｅｉｋｕ", "て行く", "てうく"}
    returnlike_words = {"return", "ｒｅｔｕｒｎ", "れつrn", "れつｒｎ", "teturn", "retune",
                        "returm", "リターン", "りたーん", "ﾘﾀｰﾝ", "列rn", "retrun", "retrn"}
    
    # if (is_attendance_channel):
    if (is_bot_channel):
        if (message.author.bot):
            return

        user_said = message.content.lower()

        if (user_said in inlike_words) or (user_said[:-1] in inlike_words):
            print(f"{message.author} is in")
            await message.author.add_roles(in_role)

        if (user_said in outlike_words) or (user_said[:-1] in outlike_words):
            print(f"{message.author} is out")
            await message.author.remove_roles(in_role)
        return

    # if (is_2f_cardkey_channel):
    if (is_bot_channel):
        if (message.author.bot):
            return

        user_said = message.content.lower()

        if (user_said in takelike_words) or (user_said[:-1] in takelike_words):
            if (card_can_take == True):
                print(f"{message.author} took")
                card_can_take = False
                await message.channel.send(f"**<@{message.author.id}> がカードキーを装備!**")
                await message.author.add_roles(card_2f_role)
            elif (card_can_take == False):
                role_member = card_2f_role.members[0].id
                await message.channel.send(f"**カードは現在 <@{role_member}> が装備中!**")

        if (user_said in returnlike_words) or (user_said[:-1] in returnlike_words):
            if (card_can_take == True):
                await message.channel.send(f"**カードはまだ 2F にあります!**")
            elif (card_can_take == False):
                card_can_take = True
                print(f"{message.author} returned")
                await message.channel.send(f"**<@{message.author.id}> がカードキーを返却!**")
                await message.author.remove_roles(card_2f_role)
        return
    return

client.run(token)
