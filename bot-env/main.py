# modules
import discord
import json
import os
import sys
from discord import app_commands

ffmpeg_path = "C:/Users/akki/ffmpeg/ffmpeg.exe"
embedColor = 0x1e90ff

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

intents.message_content = True

def loadJson(jsonpath):
    with open(jsonpath, "r") as file:
        data = json.load(file)
    return data

def showConfig():
    data = loadJson("config.json")
    print("----- CONFIG -----")
    if data["showtoken"]:
        print(f"Bot Token: {data["token"]}")
    for key, value in data.items():
        if not key == "token":
            print(f"{key}: {value}")
    print("------------------")

def runClient():
    data = loadJson("config.json")
    client.run(data["token"])

async def changeSettings(key, value):
    data = loadJson("config.json")
    data[key] = value
    with open("config.json", "w") as file:
        json.dump(data, file, indent=4)
        print(f"Key '{key}' value has successfully changed to '{value}'")

async def playSound(key, value, message, data):
    print(f"サウンド {key} を再生します...(path: {value})")
    try:
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(executable=ffmpeg_path, source=value), volume=float(data["volume"]))
        message.guild.voice_client.play(source)
    except Exception as e:
        if str(e) == "Already playing audio.":
            await message.channel.send(f"既にサウンドを再生中です。`{data["prefix"]}stop`で再生を停止、または現在再生中のサウンドが終了してから実行してください。")
        else:
            await message.channel.send(f"予期せぬエラーが発生しました。管理者に連絡してください。\nError: {e}")

async def getPing():
    raw_ping = client.latency
    ping = round(raw_ping * 1000)
    return ping

@client.event
async def on_ready():
    showConfig()
    print(f'{client.user}としてログインしました。')
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"/help | {await getPing()}ms"))
    await tree.sync()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    guild = message.guild
    dataS = loadJson("sounds/sounds.json")
    data = loadJson("config.json")
    soundboard_channel = discord.utils.get(guild.channels, name='soundboard')
    soundboard_channel_jp = discord.utils.get(guild.channels, name='サウンドボード')
    if message.channel == soundboard_channel or message.channel == soundboard_channel_jp:
        print(f"名前が'soundboard'または'サウンドボード'のチャンネルからメッセージを受信しました: {message.content}")
        if message.author.bot and data["denybot"]:
            print("送信元がbotです。処理を中断します。")
            return
        blacklist = loadJson("blacklist.json")
        for key, value in blacklist.items():
            if message.author.id == value or message.author.name == key:
                print("送信元がブラックリストに入っています。処理を中断します。")
                await message.channel.send(f"{message.author.display_name}({message.author.id})さんはブラックリストに入っているので使えません。残念でした！")
                return
        for key, value in dataS.items():
            if message.content == (f"{data['prefix']}p {key}") or message.content == (f"{data['prefix']}play {key}"):
                print("sounds.jsonに含まれる特定の文字列が送信されました。")
                if message.author.bot and data["denybot"] == False:
                    if data["autoconnect"] and not message.guild.voice_client:
                        await message.channel.send("BOTからの操作ではAutoConnect設定は使用できません。BOTがVCに参加してから使用してください。")
                        return
                    print("送信元がbotですが、denybot設定がオフなので無視します。")
                    await playSound(key, value, message, data)
                    return
                if not message.author.voice:
                    await message.channel.send(f"{message.author.display_name}({message.author.id})さん、VCに参加してから実行してください。")
                    return
                elif not message.guild.voice_client:
                    if data["autoconnect"]:
                        await message.author.voice.channel.connect()
                        await playSound(key, value, message, data)
                        return
                    else:
                        await message.channel.send("/joinを実行し、BOTがVCに接続してから実行してください。")
                        return
                elif discord.utils.get(client.voice_clients, guild=message.guild):
                    await playSound(key, value, message, data)
                else:
                    await message.channel.send("普通に使っていれば出るはずのないエラーです。おめでとう！(?)")
                    return
            elif message.content == f"{data["prefix"]}stop" and message.author.voice:
                print("再生を停止しました。")
                message.guild.voice_client.stop()
                return
            elif message.author.bot and data["denybot"] == False and message.content == f"{data["prefix"]}stop":
                print("送信元がbotですが、denybot設定がオフなので無視します。")
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
    member = interaction.user
    voice_state = member.voice
    if voice_state is not None and voice_state.channel:
        await member.guild.voice_client.disconnect()
        await interaction.response.send_message("VCから退出しました。", ephemeral=True)
    else:
        await interaction.response.send_message("VCに接続していません。", ephemeral=True)

# ping取得コマンド
@tree.command(name="ping", description="Ping取得")
async def ping(interaction):
    await interaction.response.send_message(f"Pong! Current ping has {await getPing()}ms.", ephemeral=True)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=f"/help | {await getPing()}ms"))

@tree.command(name="help", description="Helpを表示します")
async def help(interaction):
    data = loadJson("config.json")
    embed = discord.Embed(title="Help / ヘルプ", description="使用可能なコマンドの一覧です。", color=embedColor)
    embed.add_field(name="/help", value="このコマンドです。", inline=False)
    embed.add_field(name="/sounds", value="使用可能なサウンドボードの一覧です。", inline=False)
    embed.add_field(name="/ping", value="pingを取得します。", inline=False)
    embed.add_field(name="/addsound [mp3 file] [sound name]", value="サウンドを追加します。", inline=False)
    embed.add_field(name="/join", value="VCに参加します。", inline=False)
    embed.add_field(name="/leave", value="VCから退出します。", inline=False)
    embed.add_field(name="/settings", value="現在の設定を表示します。", inline=False)
    embed.add_field(name="/setvolume", value="音量を変えます。0~1までの値です。", inline=False)
    embed.add_field(name="/setdenybot", value="BOTからの操作を許可するかの設定です。", inline=False)
    embed.add_field(name="/setautoconnect", value="音声再生時に、botがVCにいなかった場合に自動で参加するかの設定です。", inline=False)
    embed.add_field(name=f"{data["prefix"]}p [sound] | {data["prefix"]}play [sound]", value="サウンドボードを流します。\n/soundsコマンドで使用可能なサウンドが確認できます。", inline=False)
    embed.add_field(name=f"{data["prefix"]}stop", value="現在流れているサウンドをすべて止めます。", inline=False)
    embed.add_field(name="", value="SoundBoard Bot V1", inline=False)
    # embed.add_field(name="/", value="説明", inline=False) てんぷら
    await interaction.response.send_message(embed=embed)

@tree.command(name="settings", description="現在の設定を取得します。")
async def settings(interaction):
    data = loadJson("config.json")
    embed = discord.Embed(title="Settings", description="現在の設定です。", color=embedColor)
    embed.add_field(name="", value=f"Volume: {data["volume"]}", inline=False)
    embed.add_field(name="", value=f"Prefix: `{data["prefix"]}`", inline=False)
    embed.add_field(name="", value=f"AutoConnect: `{data["autoconnect"]}`", inline=False)
    embed.add_field(name="", value=f"DenyBot: `{data["denybot"]}`", inline=False)
    await interaction.response.send_message(embed=embed)

@tree.command(name="sounds", description="使用可能なサウンドの取得")
async def sounds(interaction):
    embed = discord.Embed(title="使用可能なサウンドボード", description="現在使用できるすべてのサウンドボードの一覧です。", color=embedColor)
    dataS = loadJson("sounds/sounds.json")
    for key, value in dataS.items():
        embed.add_field(name=key, value=value[7:])
    await interaction.response.send_message(embed=embed)

@tree.command(name="addsound", description="サウンドを追加します。※注意 サウンド名を日本語にしないでください。")
async def addSound(interaction: discord.Interaction, file: discord.Attachment, soundname: str):
    if file.filename.lower().endswith('.mp3'):
        print(f"mp3 ファイルが送信されました。 ファイル名: {file.filename}, サウンド名: {soundname}")
        dataS = loadJson("sounds/sounds.json")
        soundsDict = dict(dataS)
        fname = file.filename
        await file.save(f"sounds/{soundname}.mp3")
        soundsDict.update({f"{soundname}": f"sounds/{soundname}.mp3"})
        with open("sounds/sounds.json", "w") as file:
            json.dump(soundsDict, file, indent=4, ensure_ascii=False)
            print(f"送信されたファイル'`{fname}`'をサウンド名'{soundname}'として追加しました。")
            await interaction.response.send_message(f"送信されたファイル'`{fname}`'をサウンド名'{soundname}'として追加しました。", ephemeral=True)
    else:
        await interaction.response.send_message("mp3形式で送信してください。", ephemeral=True)
        return

@tree.command(name="guide", description="使用時のガイドを表示します。")
async def showGuide(interaction):
    embed = discord.Embed(title="ガイド", description="botのガイドです。", color=embedColor)
    embed.add_field(name="えー ヘルプ見ろ！", value="")
    await interaction.response.send_message(embed=embed)

@tree.command(name="setvolume", description="音量を変えます。")
async def setVolume(interaction, volume: float):
    data = loadJson("config.json")
    if 0 <= volume <= 1:
        volume_ = data["volume"]
        await changeSettings("volume", volume)
        await interaction.response.send_message(f"音量を{volume}に変更しました。(元の値: {volume_})")
    else:
        await interaction.response.send_message("音量は0以上もしくは1以下に設定してください。", ephemeral=True)
        return

@tree.command(name="setautoconnect", description="サウンド再生時、VCに接続していなかった場合に自動で接続するかの設定を変更します。")
async def setAutoConnect(interaction, value: bool):
    data = loadJson("config.json")
    if isinstance(value, bool):
        setting_ = data["autoconnect"]
        await changeSettings("autoconnect", value)
        await interaction.response.send_message(f"設定を{value}に変更しました。(元の値: {setting_})")
    else:
        await interaction.response.send_message("不正な値です。||本来出ないはずですが...何かしましたか...?||", ephemeral=True)
        return

@tree.command(name="setdenybot", description="botからの操作を許可するかの設定です。")
async def setDenyBot(interaction, value: bool):
    data = loadJson("config.json")
    if isinstance(value, bool):
        setting_ = data["denybot"]
        await changeSettings("denybot", value)
        await interaction.response.send_message(f"設定を{value}に変更しました。(元の値: {setting_})")
    else:
        await interaction.response.send_message("不正な値です。||本来出ないはずですが...何かしましたか...?||", ephemeral=True)
        return

runClient()