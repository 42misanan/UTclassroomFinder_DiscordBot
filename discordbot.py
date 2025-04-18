import discord
from discord.ext import commands
import csv

TOKEN = 'MTM2MjMxNzU1NzE5MjcyNDU2MA.GGr3Tw.iu_idP-zzgsBNK5bqlO8W-h-lrebXyqnVPF0hE'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents, activity=discord.CustomActivity("!classroom [科目番号] で検索"))

# Bot起動時の通知
@bot.event
async def on_ready():
    print(f"ready")

# classroom コマンド
@bot.command(name="classroom", description="教室情報を検索します")
async def classroom(ctx, target: str):
    is_found = False
    with open('kdb_2025-ja_fix.csv', mode='r', encoding='UTF-8') as csvfile:
        classList = csv.DictReader(csvfile)
        for row in classList: #リストを検索
            if row['科目番号'] == target: #一致時処理
                if row['教室'] == "": #教室なしの分岐
                    await ctx.send(f'{target} {row['科目名']} の教室は 指定されていません. もしかして: オンデマ')
                    is_found = True
                    break
                else: #教室ありの分岐
                    await ctx.send(f'{target} {row['科目名']} の教室は {row['教室']} です')
                    is_found = True
                    break
        if is_found == False: #検索後の不一致時処理
            await ctx.send('一致するものがありませんでした')

# Bot起動
bot.run(TOKEN)