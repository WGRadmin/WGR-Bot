import json
import disnake
from disnake.ext import commands
from disnake.utils import get

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='!', intents=intents, help_command=None)

CHANNEL_ID = 1128222993550692442


class MyHelpCommand(commands.MinimalHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            await destination.send(page)


client.help_command = MyHelpCommand()


@client.event
async def on_member_join(member):
    print(f"{member.name} has joined the server")  # デバッグ用の出力
    guild = member.guild
    text_category = get(guild.categories, name="個別テキスト")
    voice_category = get(guild.categories, name="個人vc")
    role = get(guild.roles, name="窓口")
    print(f"Role: {role}")
    overwrites = {
        guild.default_role: disnake.PermissionOverwrite(read_messages=False),
        guild.me: disnake.PermissionOverwrite(read_messages=True),
        role: disnake.PermissionOverwrite(read_messages=True)
    }
    text_channel = await guild.create_text_channel(f"📝｜{member.name}", category=text_category, overwrites=overwrites)
    voice_channel = await guild.create_voice_channel(f"🔈｜{member.name}", category=voice_category, overwrites=overwrites)

    # メンションしてメッセージを送信
    await text_channel.send(f"ようこそ、{member.mention}さん！ {role.mention}の方々もよろしくお願いします。")


# 設定ファイルからフラグを読み込む
with open('config.json', 'r') as f:
    config = json.load(f)


# log inメッセージ
@client.event
async def on_ready():
    await client.change_presence(activity=disnake.Game(name="稼働中"))
    print(f'正常に起動しました')

    # 特定のチャンネルにメッセージを送信
    if config.get('send_message_on_startup'):
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("private/WGR_Botが起動しました！")


# 起動停止メッセージ
@client.event
async def on_disconnect():
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Botが停止しました")


# 起動確認コマンド
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # hello(設定を表示します)
    if message.content == '!wgrhello':
        await message.channel.send('`Hello World!`\n\n**稼働中機能**\nロール付与機能 : 稼働中\nチャンネル生成機能 : 稼働中\n\n**現在のチャンネル生成設定**\n>>> - テキストカテゴリー_個別カテゴリー\n- ボイスカテゴリー_個人vc\n- テキストチャンネルテンプレート_📝｜UserName\n- ボイスチャンネルテンプレート_🔈｜UserName')
        
client.run("botのトークン")
