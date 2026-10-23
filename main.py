import discord
import os
import random
from flask import Flask
from threading import Thread
import time
from discord import app_commands
from datetime import timedelta
import unicodedata
import jaconv

# Flaskのアプリケーションインスタンスを作成（gunicornが実行するWebサーバー）
app = Flask(__name__) 

# グローバルフラグ：Botが起動を試みたかを示す
bot_start_attempted = False

# -----------------
# Discord Bot本体の起動関数
# -----------------
# ユーザーごとのスコアを保存
yaju_scores = {}

def run_discord_bot():
    global bot_start_attempted
    
    # 環境変数からトークンを取得
    TOKEN = os.getenv("DISCORD_TOKEN")
    
    # 元のコードで使用されていた Intents.all() を使用
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)
    intents.message_content = True  # メッセージ内容の受信を有効化
    intents.messages = True  # メッセージの受信を有効化
    tree = app_commands.CommandTree(client)
    
    @client.event
    async def on_ready():
        # ログ出力（元のコードのまま）
        print(f'We have logged in as {client.user}')
        await tree.sync()
        print("Slash commands synced.")

    @tree.context_menu(name="メッセージ消去")
    async def delete_message(interaction: discord.Interaction, message: discord.Message):

        # オーナー以外は使えない
        if interaction.user.id != 1367077549363953737:
            await interaction.response.send_message("❌ この機能は許可されていません。", ephemeral=True)
            return

        # メッセージ削除
        try:
            await message.delete()
            await interaction.response.send_message("🧹 メッセージを削除しました。", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("❌ 権限不足で削除できませんでした。", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ エラーが発生しました: {e}", ephemeral=True)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        servers = len(client.guilds)
        await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=f'導入されているサーバー数：{servers}'))
        content = unicodedata.normalize("NFKC", message.content)
        content = jaconv.kata2hira(content)
        content = content.lower()

        if (('頭' in content or 'あたま' in content) and 'ますよ' in content) or ('いいよ' in content and 'こいよ' in content) or 'んぁ' in content or 'んあ' in content or 'いきそ' in content or 'それいいよ' in content or 'kmr' in content or 'mur' in content or 'tdn' in content or 'ton' in content or 'htn' in content or 'db' in content or 'tnok' in content or 'drvs' in content or 'nsok' in content or 'kbtit' in content or 'ogmm' in content or 'kyn' in content or 'nktidksg' in content or 'akys' in content or 'tknuc' in content or 'sgw' in content or 'ondisk' in content or 'trn' in content or 'kbs' in content or 'eczn' in content or 'ru' in content or 'emt' in content or 'らいらら' in content or 'myn' in content or 'snj' in content or 'bb' in content or 'tkgw' in content or 'mnr' in content or 'popo' in content or 'ndk' in content or 'aknm' in content or 'joker' in content or 'go' in content or 'udk' in content or 'coat' in content or 'krbys' in content or 'skgt' in content or 'どろへどろ' in content or 'しゅばるご' in content or '下北沢' in content or 'しもきたさわ' in content or '114514' in content or 'くしろよ' in content or '810' in content or '野獣' in content or 'やじゅう' in content or 'いきすぎ' in content or '田所' in content or '364' in content or 'みろよ' in content or '見ろよ' in content or '1919' in content or 'いくいく' in content or 'ますね' in content or 'いんむ' in content or 'いんみゅ' in content or '真夏' in content or 'まなつ' in content or 'おなしゃす' in content or 'せんせんしゃ' in content or '菅野美穂' in content or 'かんのみほ' in content or 'でますよ' in content or '出ますよ' in content or 'くいあらためて' in content or '悔い改めて' in content or '見とけよ' in content or 'みとけよ' in content or 'まずいですよ' in content or '小並感' in content or 'ありがとなす' in content or 'よつんゔぁい' in content or 'いましめ' in content or '戒め' in content or 'ばっとまん' in content or 'ばっどまん' in content or 'badman' in content or 'んにゃぴ' in content or 'ぶっちっぱ' in content:
            await message.channel.send('（これ指摘したら淫夢厨ってバレるな...）')
        if '14' in content and '3000' in content:
            await message.channel.send('うせやろ！？')
        if 'いいよ' in content and 'それ' not in content and 'こいよ' not in content:
            await message.channel.send('こいよ！')
        if '屋上' in content or 'まずうち' in content or 'てかない' in content:
            await message.channel.send('まずうちさぁ、屋上あんだけど...焼いてかない？')
        if '胸' in content:
            await message.channel.send('ファ！？')
        if 'ふぁ' in content:
            await message.channel.send('ﾌｧｯ!?(驚愕)ｳｰﾝ...(心停止)')
        if 'お待たせ' in content or 'おまたせ' in content or '睡眠' in content or '昏睡' in content or ('飲み' in content or 'のみ' in content) and ('物' in content or 'もの' in content):
            await message.channel.send('アイスティしかなかったんだけど、いいかな？')
        if '21' in content and ('拳' in content or 'こぶし' in content):
            await message.channel.send('24歳です 学生です')
        if 'みたい' in content or '見たい' in content:
            await message.channel.send('見たけりゃ見せてやるよ！（震え声）')
        if 'あ' in content and 'はい' in content:
            await message.channel.send('お前さっき俺ら着替えてる時チラチラ見てただろ')
        if '警察' in content or '通報' in content:
            await message.channel.send('警察だ！（インパルス板倉）')
        if 'ほり' in content or '堀' in content or 'とおる' in content or '通る' in content:
            await message.channel.send('流行らせコラ！')
        if 'ここあ' in content and 'らいおん' in content or 'ここ' in content and ('あらえよ' in content or '洗えよ' in content):
            await message.channel.send('あ、わかりました...')
        if ('みて' in content or '見て' in content) and 'ない' in content:
            await message.channel.send('嘘つけ絶対見てたゾ')
        if 'ええな' in content or 'えぇな' in content:
            await message.channel.send('あ、いいじゃん　入れたろ♪')
        if 'とかって' in content or 'ますか' in content:
            await message.channel.send('やりますねぇ！')
        if '痛い' in content or 'いたい' in content:
            await message.channel.send('痛いですねこれは痛い（冷静）')
        if '王道' in content and ('ゆく' in content or '征く' in content or '行く' in content or 'いく' in content):
            if 'そーぷ' in content:
                await message.channel.send('（王者の風格）')
            else:
                await message.channel.send('ソープ系ですか')
        if 'じゃけん' in content:
            await message.channel.send('おっ、そうだな（適当）')
        if 'お' in content and 'そうだな' in content:
            await message.channel.send('あっそうだ　おいKMRァ！（唐突）')
        if 'あ' in content and 'そうだ' in content:
            await message.channel.send('おいKMRァ！（唐突）')
        if 'てるか' in content:
            await message.channel.send('バッチェ冷えてますよ')
        if 'ですか' in content:
            await message.channel.send('そうですねぇ...やっぱり僕は王道を征く...ソープ系ですか（王者の風格）')
        if ('丘' in content or '岡' in content or 'おか' in content) and 'の' in content and ('下' in content or 'した' in content):
            await message.channel.send('（これ指摘したら淫夢厨ってバレるな...）')
        if 'この' in content and ('辺' in content or 'へん' in content):
            await message.channel.send('エロい♪')
        if 'なよ' in content:
            await message.channel.send('お前のことがッ！好きだったんだよ！！！')
        if '白' in content:
            await message.channel.send('はっきりわかんだね')
        if 'はっきり' in content:
            await message.channel.send('すっげぇ白くなってる はっきりわかんだね')
        if 'たまげ' in content or '魂消' in content:
            await message.channel.send('勝手にたまげとけ')
        if ('あたり' in content or '当たり' in content) and ('まえ' in content or '前' in content) or '当然' in content:
            await message.channel.send('当たり前だよなぁ？？')
        if 'これもう' in content:
            await message.channel.send('この辺がSexy！')
        if 'えろい' in content:
            await message.channel.send('暴れんなよ♪')
        if 'あいすてぃ' in content:
            await message.channel.send('これもう...わかんねぇな')
        if '多少' in content or 'たしょう' in content:
            await message.channel.send('まあ、多少はね？')
        if 'れたろ' in content:
            await message.channel.send('すここい歌♪')
        elif 'いいじゃん' in content and 'たろ' not in content:
            await message.channel.send('入れたろ♪')
        if 'すここい' in content:
            await message.channel.send('YAJU&U！')
        if 'yaju' in content and '&' in content and 'u' in content:
            await message.channel.send('野獣先輩♪')
        if '学生' in content or 'がくせい' in content:
            await message.channel.send('学生？あっ...（察し）ふ〜ん')
        elif '24' in content:
            await message.channel.send('24歳？もう働いてるの、じゃあ？')
        if 'one one four five' in content and 'one four' in content:
            await message.channel.send('いいよ♪こいよ♪')
        if ('そうだよ' in content or 'そだよ' in content or 'そうですよ' in content) and '便乗' not in content:
            mur_icon = "https://keni-77.github.io/inmbotweb/mur.png"

            # Webhook権限チェック
            perms = message.channel.permissions_for(message.guild.me)

            if perms.manage_webhooks:
                # Webhook使える
                webhooks = await message.channel.webhooks()
                webhook = None

                for wh in webhooks:
                    if wh.name == "MUR_webhook":
                        webhook = wh
                        break

                # なければ作る
                if webhook is None:
                    webhook = await message.channel.create_webhook(name="MUR_webhook")

                # Webhookで便乗
                await webhook.send(
                    "そうだよ（便乗）",
                    username="MUR先輩",
                    avatar_url=mur_icon
                )

            else:
                # Webhook使えない → 普通に便乗
                await message.channel.send("そうだよ（便乗）")

        if '必殺' in content and '発動' in content:
            await message.channel.send('''必殺！野獣の咆哮！
**ヌゥン！ヘッ！ヘッ！**
**ア゛ア゛ア゛ア゛ァ゛ァ゛ァ゛ァ゛**
**ア゛↑ア゛↑ア゛↑ア゛↑ア゛ア゛ア゛ァ゛ァ゛ァ゛ァ゛！！！！**
**ウ゛ア゛ア゛ア゛ア゛ア゛ア゛ァ゛ァ゛ァ゛ァ゛ァ゛ァ゛ァ！！！！！**
**フ ウ゛ウ゛ウ゛ゥ゛ゥ゛ゥ゛ン！！！！**
**フ ウ゛ゥ゛ゥ゛ゥン！！！！(大迫真)**
***（※音量注意）***
https://www.youtube.com/watch?v=A3P4J7TcAk0''')

    @tree.command(name="server_list", description="Botが参加しているサーバー一覧を表示します")
    async def server_list(interaction: discord.Interaction):

        guilds = client.guilds
        text = "\n".join([f"{g.name} : {g.id}" for g in guilds])

        await interaction.response.send_message(f"**参加中のサーバー（{len(guilds)}件）**\n{text}")
    
    @tree.command(name="invite", description="Botが参加しているサーバーの招待リンクを送ります")
    async def invite(interaction: discord.Interaction, guild_id: str):

        # 数字チェック
        if not guild_id.isdigit():
            await interaction.response.send_message("サーバーIDは数字で入力してください。", ephemeral=True)
            return

        guild = interaction.client.get_guild(int(guild_id))
        if guild is None:
            await interaction.response.send_message("そのサーバーは見つかりませんでした。", ephemeral=True)
            return

        # 招待リンクを作れるチャンネルを探す
        target_channel = None
        for ch in guild.text_channels:
            perms = ch.permissions_for(guild.me)
            if perms.create_instant_invite:
                target_channel = ch
                break

        if target_channel is None:
            await interaction.response.send_message(
                "❌ Botに招待リンクを作成する権限がありません。",
                ephemeral=True
            )
            return

        # 招待リンク作成
        invite = await target_channel.create_invite(max_age=0, max_uses=0)

        await interaction.response.send_message(
            f"**{guild.name} の招待リンクはこちらです**\n{invite.url}"
        )

    @tree.command(name="leave", description="このBotを特定のサーバーから退出させます（Botオーナー専用コマンド）")
    async def leave_server(interaction: discord.Interaction, guild_id: str):

        # Bot のオーナーだけ使える
        if interaction.user.id != 1367077549363953737:
            await interaction.response.send_message("このコマンドは許可されていません。", ephemeral=True)
            return

        # まず defer でインタラクション確保
        await interaction.response.defer(ephemeral=True)

        # 数字チェック
        if not guild_id.isdigit():
            await interaction.followup.send("サーバーIDは数字で入力してください。", ephemeral=True)
            return

        # サーバーチェック
        guild = interaction.client.get_guild(int(guild_id))
        if guild is None:
            await interaction.followup.send("そのサーバーは見つかりませんでした。", ephemeral=True)
            return

        # 退出メッセージ送信（権限不足でも無視）
        try:
            # システムチャンネル or 最初に書き込めるテキストチャンネル
            send_channel = guild.system_channel or next(
                (ch for ch in guild.text_channels if ch.permissions_for(guild.me).send_messages),
                None
            )
            if send_channel:
                await send_channel.send(f"**{guild.name}** から退出します。")
        except:
            pass

        # サーバー退出
        try:
            await guild.leave()
            await interaction.followup.send(f"サーバー **{guild.name}** から退出しました。")
        except discord.Forbidden:
            await interaction.followup.send("権限不足で退出できませんでした。Bot のロールを一番上にしてください。", ephemeral=True)
        
    @tree.command(name="random_number", description="1,3,4,5,6,9からランダムに6回選びます")
    async def random_number(interaction: discord.Interaction):
        # ランダムに数字を選ぶ
        numbers = [1, 3, 4, 5, 6, 9]
        result = [random.choice(numbers) for _ in range(6)]
        
        # 読み方辞書
        reading = { 1: "い", 3: "み", 4: "よ", 5: "こ", 6: "ろ", 9: "く" }
        # 読み方に変換
        reading_result = "".join(reading[n] for n in result)

        # 特別な並び
        special = [1, 1, 4, 5, 1, 4]
        zorome1 = [1, 1, 1, 1, 1, 1]
        zorome3 = [3, 3, 3, 3, 3, 3]
        zorome4 = [4, 4, 4, 4, 4, 4]
        zorome5 = [5, 5, 5, 5, 5, 5]
        zorome6 = [6, 6, 6, 6, 6, 6]
        zorome9 = [9, 9, 9, 9, 9, 9]
        ikuikuiku = [1, 9, 1, 9, 1, 9]
        sikosikosiko = [4, 5, 4, 5, 4, 5]
        gosigosigosi = [5, 4, 5, 4, 5, 4]
        miroyomiroyo = [3, 6, 4, 3, 6, 4]
        
        user_id = interaction.user.id
        
        if result == special:
            await interaction.response.send_message(f"結果: {result}\n\n🎉**いい世、来いよ！**🎉")
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 6
        elif result == zorome1 or result == zorome3 or result == zorome4 or result == zorome5 or result == zorome6 or result ==zorome9:
            await interaction.response.send_message(f"結果: {result}\n\n🎉**ゾロ目だゾ**🎉")
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 3
        elif result == ikuikuiku:
            await interaction.response.send_message(f"結果: {result}\n\n🎉**イキスギィ！**🎉")
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 5
        elif result == sikosikosiko:
            await interaction.response.send_message(f"結果: {result}\n（し◯し◯し◯...）\n🎉**やりますねぇ！**🎉")
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 4
        elif result == gosigosigosi:
            await interaction.response.send_message(f"結果: {result}\n（ごしごしごし...）\n🎉**洗い方上手いっすね〜**🎉")
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 4
        elif result == miroyomiroyo:
            await interaction.response.send_message(f"結果: {result}\n\n🎉**見ろよみろよ！**🎉")
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 5
        else:
            await interaction.response.send_message(f"結果: {result}\n{reading_result}\n残念だったゾ")

    @tree.command(name="yaju_rank", description="野獣スコアランキングを表示します")
    async def yaju_rank(interaction: discord.Interaction):

        if not yaju_scores:
            await interaction.response.send_message("まだ誰もスコアを持っていません。", ephemeral=True)
            return

        # スコア順に並べ替え
        sorted_scores = sorted(yaju_scores.items(), key=lambda x: x[1], reverse=True)

        rank_lines = []
        for i, (user_id, score) in enumerate(sorted_scores, start=1):

            # どのサーバーにいてもユーザー情報を取得
            user = interaction.client.get_user(user_id)

            if user:
                # グローバル名 → なければ username
                name = user.global_name or user.name
            else:
                name = f"Unknown({user_id})"

            rank_lines.append(f"{i}位: **{name}** - {score}点")

        rank_text = "\n".join(rank_lines)

        await interaction.response.send_message(f"🏆**野獣スコアランキング**🏆\n　*今日の野獣王は誰！？*　\n\n{rank_text}")

    @tree.command(name="inmu_rank", description="サーバー内の淫夢度ランキングを表示します")
    async def inmu_rank(interaction: discord.Interaction):

        await interaction.response.defer()

        guild = interaction.guild
        members = guild.members

        # 数値化関数
        def encode_to_numbers(text: str) -> str:
            encoded = text.encode("utf-8")
            return "".join(str(b) for b in encoded)

        # パターン
        patterns = {
            "81": 81,
            "114": 114,
            "514": 514,
            "364": 364,
            "19": 19
        }

        results = []

        for member in members:
            display = member.display_name
            globalname = member.global_name or ""

            display_num = encode_to_numbers(display)
            global_num = encode_to_numbers(globalname)

            score_display = 0
            score_global = 0

            for key, value in patterns.items():
                score_display += display_num.count(key) * value
                score_global += global_num.count(key) * value

            total = score_display + score_global

            results.append((member, total))

        # スコア順に並べ替え
        results.sort(key=lambda x: x[1], reverse=True)

        # Embed 作成
        embed = discord.Embed(
            title="淫夢度ランキング",
            description="（サーバー内）",
            color=discord.Color.blue()
        )

        medals = ["🥇", "🥈", "🥉"]

        ranking_text = ""

        # 順位計算（同点は同順位）
        last_score = None
        last_rank = 0
        count = 0
        max_rank = 20

        for member, score in results:
            count += 1

            # 同点なら同順位
            if score == last_score:
                rank = last_rank
            else:
                rank = count
                last_rank = rank
                last_score = score

            # 20位を超えたら終了（ただし20位と同点なら表示）
            if rank > max_rank:
                break

            # メダル付与
            if rank <= 3:
                ranking_text += f"{medals[rank-1]} **{member.display_name}** — 淫夢度：{score}\n"
            else:
                ranking_text += f"{rank}位：**{member.display_name}** — 淫夢度：{score}\n"

        embed.add_field(
            name="ランキング結果",
            value=ranking_text,
            inline=False
        )

        # サムネイルは1位のアイコン
        if results:
            embed.set_thumbnail(url=results[0][0].display_avatar.url)

        await interaction.followup.send(embed=embed)

    @tree.command(name="purge_from", description="指定ユーザーの指定キーワードを含むメッセージをチャンネルから削除（管理者専用）")
    @app_commands.describe(
        user="削除対象のユーザー",
        keyword="含まれているキーワード（allで全てのメッセージを削除）"
    )
    async def purge_from(interaction: discord.Interaction, user: discord.User, keyword: str):

        # 管理者チェック
        if not interaction.user.guild_permissions.administrator and interaction.user.id != 1367077549363953737:
            await interaction.response.send_message("❌ このコマンドは管理者のみ使用できます。", ephemeral=True)
            return

        await interaction.response.send_message(
            f"🔍 {user.display_name} の「{keyword}」を含むメッセージを検索中…",
            ephemeral=True
        )

        channel = interaction.channel
        now = discord.utils.utcnow()
        limit_date = now - timedelta(days=14)

        # メッセージを全部集める
        targets = []
        async for msg in channel.history(limit=None):
            if msg.author.id == user.id and (keyword == "all" or keyword in msg.content):
                targets.append(msg)

        # 14日以内と14日以上に分ける
        recent = [m for m in targets if m.created_at > limit_date]
        old = [m for m in targets if m.created_at <= limit_date]

        # --- 100件ずつ削除（bulk delete） ---
        for i in range(0, len(recent), 100):
            batch = recent[i:i+100]
            if len(batch) > 1:
                await channel.delete_messages(batch)
            else:
                await batch[0].delete()

        # --- 古いメッセージは1件ずつ削除 ---
        for m in old:
            await m.delete()

        await interaction.followup.send(
            f"🧹 削除完了\n"
            f"・14日以内：{len(recent)}件（100件ずつ削除）\n"
            f"・14日以上：{len(old)}件（1件ずつ削除）",
            ephemeral=True
        )

    # --- Botの実行 ---
    if TOKEN:
        try:
            # 元のコードにあった client.run(TOKEN) のみを実行
            client.run(TOKEN)
        except Exception as e:
            print(f"Discord Bot 起動失敗: {e}")
    else:
        print("エラー: Botトークンが設定されていません。")

# -----------------
# Webサーバーのエンドポイント (gunicornがアクセスする場所)
# -----------------
@app.route('/', methods=['GET', 'HEAD'])
def home():
    global bot_start_attempted
    
    # Botがまだ起動を試みていない場合のみ、Botを別スレッドで起動
    if not bot_start_attempted:
        print("Webアクセスを検知。Discord Botの起動を試みます...")
        bot_start_attempted = True
        
        # Botを別スレッドで起動
        Thread(target=run_discord_bot).start()
        
        return "Discord Bot is initializing..."
    
    # Bot起動試行済みの場合は、Renderのヘルスチェックに応答
    return "Bot is alive!"
