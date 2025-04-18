import discord
from discord.ext import commands
import csv
import config

# .env -> config.py -> discordbot.py 受け渡し
# トークン 取得
TOKEN = config.DISCORD_TOKEN

# intents の設定
intents = discord.Intents.default()
intents.message_content = True

# bot オブジェクトを作成
# prefix 指定, intents 指定, 標準 help_command 無効化, activity 設定)
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None, activity=discord.CustomActivity("!classroom [科目番号] で検索"))

#csvファイルからキャッシュする関数を定義
def load_class_data():
    class_cache.clear()
    with open('kdb_2025-ja_fix.csv', mode='r', encoding='UTF-8', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            subject_code = row['科目番号']
            class_cache[subject_code] = row


#################### main ####################


#初期化
class_cache = {} 
@bot.event 
async def on_ready():
    try:
        load_class_data() #キャッシュを取得
        print(f"CONSOLE: file successfully loaded")
    except Exception as e:
        print("CONSOLE: failed to load file")
        print(e)

# help コマンド
@bot.command(name="help", description="コマンド一覧を表示します")
async def help(ctx, index: str = None):
    if index == None:
        await ctx.send("```\n"
        "コマンド一覧\n"
        "- classroom [科目番号]: 教室情報を検索します.\n"
        "- reload: 再読み込みします.\n"
        "- help [コマンド]: 使い方を表示します.\n"
        "```")
    elif index == "classroom":
        await ctx.send("```\n"
        "classroom [科目番号]:\n"
        "- 引数に科目番号を取ります.\n"
        "- 教室情報を返します. 結果がない場合は, オンデマ か db上に存在しない かを返します.\n"
        "```")
    elif index == "reload":
        await ctx.send("```\n"
        "reload:\n"
        "- 引数を取りません.\n"
        "- 動いているpc上での kdb_2025-ja_fix.csv ファイルを読み込みし直します.\n"
        "```")
    elif index == "help":
        await ctx.send("```"
        "help [コマンド]:\n"
        "- 引数なし: コマンドの一覧を表示します.\n"
        "- 引数あり: 特定のコマンドの使い方を表示します.\n"
        "```")
    else:
        await ctx.send("一致するコマンドが見つかりませんでした. コマンドの一覧を表示するには !help を使用してください.")

# classroom コマンド
@bot.command(name="classroom", description="教室情報を検索します")
async def classroom(ctx, target: str):
    row = class_cache.get(target)
    if row == None:
        await ctx.send('一致するものがありませんでした')
    elif row['教室'] == "": #教室なしの分岐
        await ctx.send(f"{target} {row['科目名']} の教室は 指定されていません. もしかしてオンデマ?")
    else: #教室ありの分岐
        await ctx.send(f"{target} {row['科目名']} の教室は {row['教室']} です")

# reload コマンド
@bot.command(name="reload", description="csvファイルを読み込み直します(管理者用)")
async def reload(ctx):
    try:
        load_class_data()
        await ctx.send("リロードしました")
    except Exception as e:
        await ctx.send("CONSOLE: failed to load file")
        print(e)

# Bot起動
bot.run(TOKEN)

