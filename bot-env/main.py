# modules
import discord
import json
from discord import app_commands

config = open("config.json", "r")
data = json.load(config)
volume = data["volume"]

soundboards = open("sounds/sounds.json", "r")
dataS = json.load(soundboards)

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

intents.message_content = True

print("----- CONFIG -----")
if data["showtoken"] == "true":
    print(f"Bot Token: {data["token"]}")
for key, value in data.items():
    if not key == "token":
        print(f"{key}: {value}")
print("------------------")

async def getPing():
    raw_ping = client.latency
    ping = round(raw_ping * 1000)
    return ping

@client.event
async def on_ready():
    print(f'{client.user}としてログインしました。')
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"/help | {await getPing()}ms"))
    await tree.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    guild = message.guild
    soundboard_channel = discord.utils.get(guild.channels, name='soundboard')
    if message.channel == soundboard_channel:
        print(f"名前が'soundboard'のチャンネルからメッセージを受信しました: {message.content}")
        for key, value in dataS.items():
            if message.content.startswith(f"{data['prefix']}p {key}"):
                print("soundsに含まれる特定の文字列が送信されました。")
                if message.author.voice:
                    if discord.utils.get(client.voice_clients, guild=message.guild):
                        print(f"サウンド {key} を再生します...(path: {value})")
                        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable="C:/Users/akki/ffmpeg/ffmpeg.exe", source=value), volume=float(volume))
                        message.guild.voice_client.play(source)
                    else:
                        await message.channel.send("/joinを実行し、BOTがVCに接続してから実行してください。")
                else:
                    await message.channel.send(f"{message.author.name} さん、VCに参加してから実行してください。")
            if message.content == f"{data["prefix"]}stop":
                print("再生を停止しました。")
                message.guild.voice_client.stop()
                return

# コマンドたち

@tree.command(name="join", description="VCに接続します。")
async def joinVC(interaction):
    member = await interaction.guild.fetch_member(interaction.user.id)
    if member.voice:
        if not interaction.guild.voice_client:
            await interaction.response.send_message("VCに接続しました！！", ephemeral = True)
            await member.voice.channel.connect()
        else:
            await interaction.response.send_message("すでにVCに接続しています。", ephemeral = True)
    else:
        await interaction.response.send_message("VCに接続後実行してください。", ephemeral=True)

@tree.command(name="leave", description="VCから退出します。")
async def leaveVC(interaction):
    member = await interaction.guild.fetch_member(interaction.user.id)
    await member.voice_client.disconnect()
    await interaction.response.send_message("VCから退出しました。", ephemeral = True)

# ping取得コマンド
@tree.command(name="ping", description="Ping取得")
async def ping(interaction):
    await interaction.response.send_message(f"Pong! Current ping has {await getPing()}ms.", ephemeral=True)

@tree.command(name="help", description="Helpを表示します")
async def help(interaction):
    embed = discord.Embed(title="Help", description="使用可能なコマンドの一覧です。")
    embed.add_field(name="/help", value="このコマンドです。", inline=False)
    embed.add_field(name="/sounds", value="使用可能なサウンドボードの一覧です。", inline=False)
    embed.add_field(name="/ping", value="pingを取得します。", inline=False)
    embed.add_field(name=f"{data["prefix"]}p [sound]", value="サウンドボードを流します。\n/soundsコマンドで使用可能なサウンドが確認できます。", inline=False)
    embed.add_field(name=f"{data["prefix"]}stop [sound]", value="現在流れているサウンドをすべて止めます。", inline=False)
    # embed.add_field(name="/", value="説明", inline=False) てんぷら
    await interaction.response.send_message(embed=embed)

@tree.command(name="sounds", description="使用可能なサウンドの取得")
async def sounds(interaction):
    embed = discord.Embed(title="使用可能なサウンドボード",description="現在使用できるすべてのサウンドボード")
    for key, value in dataS.items():
        embed.add_field(name=key, value=value, inline=False)
    await interaction.response.send_message(embed=embed)

client.run(data["token"])