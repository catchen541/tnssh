import datetime
import discord
from discord.ext import commands
from discord import app_commands
import os

QUOTES_IMG_FOLDER = "./quotes_img"

class QuoteSlashCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="安迪語錄", description="顯示圖片語錄")
    @app_commands.describe(quote_name="輸入語錄名稱")
    async def quote_image(self, interaction: discord.Interaction, quote_name: str):
        for ext in [".png", ".jpg", ".jpeg"]:
            filepath = os.path.join(QUOTES_IMG_FOLDER, f"{quote_name}{ext}")
            if os.path.isfile(filepath):
                # 直接建立一個檔案物件
                file = discord.File(filepath, filename=os.path.basename(filepath))
                
                # ✨ 關鍵在這！直接發送檔案，不用嵌入框 ✨
                await interaction.response.send_message(file=file)
                return

        # 如果找不到圖片，還是會送出錯誤訊息喔！
        await interaction.response.send_message(f"❌ 找不到圖片語錄「{quote_name}」", ephemeral=True)

    # 自動補全語錄名稱
    @quote_image.autocomplete("quote_name")
    async def quote_autocomplete(self, interaction: discord.Interaction, current: str):
        options = []
        for fname in os.listdir(QUOTES_IMG_FOLDER):
            name, ext = os.path.splitext(fname)
            if ext.lower() in [".png", ".jpg", ".jpeg"] and current in name:
                options.append(app_commands.Choice(name=name, value=name))
        return options[:20] # 最多只顯示20個選項喔！

async def setup(bot):
    await bot.add_cog(QuoteSlashCog(bot))
    print("✅ QuoteSlashCog has been loaded successfully!")