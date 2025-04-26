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
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None, activity=discord.CustomActivity("!classroom [科目番号 or 科目名]"))


#################### main ####################


#初期化
#@bot.event 
#async def on_ready():
#    try:
#        classList = load_class_data() #キャッシュを取得
#        
#    except Exception as e:
#        print("CONSOLE: failed to load file")
#        print(e)

# help コマンド
@bot.command(name="help", description="コマンド一覧を表示します")
async def help(ctx, index: str = None):
    if index == None:
        await ctx.send("```\n"
        "コマンド一覧\n"
        "- classroom [科目番号]: 教室情報を検索します.\n"
        "- pikmin: pikmin 5 when?"
        "- help [コマンド]: 使い方を表示します.\n"
        "```")
    elif index == "classroom":
        await ctx.send("```\n"
        "classroom [科目番号]:\n"
        "- 引数に科目番号を取ります.\n"
        "- 教室情報を返します. 結果がない場合は, オンデマ か db上に存在しない かを返します.\n"
        "```")
    elif index == "help":
        await ctx.send("```"
        "help [コマンド]:\n"
        "- 引数なし: コマンドの一覧を表示します.\n"
        "- 引数あり: 特定のコマンドの使い方を表示します.\n"
        "```")
    elif index == "pikmin":
        await ctx.send("https://www.youtube.com/watch?v=Trw4SMpA28Q")
    else:
        await ctx.send("一致するコマンドが見つかりませんでした. コマンドの一覧を表示するには !help を使用してください.")

# classroom コマンド
@bot.command(name="classroom", description="教室情報を検索します")
async def classroom(ctx, target: str):
    with open('class.csv', mode='r', encoding='UTF-8', newline='') as csvfile:
        result = []
        classList = csv.DictReader(csvfile)
        for row in classList:
            if row['科目番号'] == target or row['科目名'] == target:
                if row['教室'] == "":
                    result.append(f"{row['科目番号']} {row['科目名']} の教室は 指定されていません. ")
                else:
                    result.append(f"{row['科目番号']} {row['科目名']} の教室は {row['教室']} です")
        if result == None:
            await ctx.send('一致するものがありませんでした')
        else: 
            message = "\n".join(result)
            await ctx.send(message)

# Bot起動
bot.run(TOKEN)

