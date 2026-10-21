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

        # 日付リセットチェック（もし実装済みの reset_scores_if_needed があれば呼ぶ）
        try:
            reset_scores_if_needed()
        except:
            pass

        user_id = message.author.id
        if user_id not in yaju_scores:
            yaju_scores[user_id] = 0

        servers = len(client.guilds)
        await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=f'導入されているサーバー数：{servers}'))
        content = unicodedata.normalize("NFKC", message.content)
        content = jaconv.kata2hira(content)
        content = content.lower()

        if  'ほんへ' in content or 'ぽっちゃま' in content or 'あちゃも' in content or '白いの' in content or 'しろいの' in content or '黒いの' in content or 'くろいの' in content or '多少' in content or 'たしょう' in content or (('流行' in content or 'はや' in content) and 'こら' in content) or 'あのさ' in content or ('うめ' in content and 'な' in content) or '軍畑' in content or (('丘' in content or '岡' in content or 'おか' in content) and 'の' in content and ('下' in content or 'した' in content)) or ('yaju' in content and '&' not in content) or ('王道' in content and 'そーぷ' in content and 'ゆく' not in content and 'いく' not in content and '征く' not in content and '行く' not in content) or (('いいぞ' in content or '良いぞ' in content) and 'これ' in content) or (('頭' in content or 'あたま' in content) and 'ますよ' in content) or (('いいよ' in content or '良いよ' in content) and ('こいよ' in content or '来いよ' in content)) or 'んぁ' in content or 'んあ' in content or 'いきそ' in content or ('それ' in content and ('いいよ' in content or '良いよ' in content)) or 'kmr' in content or 'mur' in content or 'tdn' in content or 'acceed' in content or 'iws' in content or 'ton' in content or 'htn' in content or 'db' in content or 'tnok' in content or 'drvs' in content or 'nsok' in content or 'kbtit' in content or 'ogmm' in content or 'mjdktni' in content or 'kyn' in content or 'nktidksg' in content or 'sbr' in content or 'nrk' in content or 'ymn' in content or 'ogrsyn' in content or 'akys' in content or 'sut' in content or 'tknuc' in content or 'sgw' in content or 'hnd' in content or 'ondisk' in content or 'trn' in content or 'okd' in content or 'aok' in content or 'mtzk' in content or 'ixabt' in content or 'ishr' in content or 'inue' in content or 'kbs' in content or 'eczn' in content or 'emt' in content or 'yksmr' in content or 'mdrkw' in content or 'gt' in content or 'らいらら' in content or 'siy' in content or 'myn' in content or 'snj' in content or 'kbysytk' in content or 'bb' in content or 'tkgw' in content or 'mnr' in content or 'popo' in content or 'ndk' in content or 'aknm' in content or 'joker' in content or 'udk' in content or 'coat' in content or 'amy' in content or 'skmt' in content or 'krbys' in content or 'skgc' in content or 'どろへどろ' in content or 'しゅばるご' in content or '下北沢' in content or 'しもきたさわ' in content or '114514' in content or 'くしろ' in content or '810' in content or '野獣' in content or 'やじゅう' in content or 'いきすぎ' in content or '田所' in content or '364' in content or 'みろよ' in content or '見ろよ' in content or '1919' in content or 'いくいく' in content or 'ますね' in content or 'いんむ' in content or 'いんみゅ' in content or '真夏' in content or 'まなつ' in content or 'おなしゃす' in content or 'せんせんしゃ' in content or '菅野美穂' in content or 'かんのみほ' in content or 'でますよ' in content or '出ますよ' in content or 'くいあらためて' in content or '悔い改めて' in content or '見とけよ' in content or 'みとけよ' in content or 'まずいですよ' in content or '小並感' in content or 'ありがとなす' in content or 'よつんゔぁい' in content or 'いましめ' in content or '戒め' in content or 'ばっとまん' in content or 'ばっどまん' in content or 'badman' in content or 'んにゃぴ' in content or 'ぶっちっぱ' in content or 'くるる' in content or 'ずるる' in content or 'ぴんきー' in content:
            await message.channel.send('（これ指摘したら淫夢厨ってバレるな…）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10
        
        if '14' in content and '3000' in content:
            await message.channel.send('うせやろ！？')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '抵抗' in content:
            await message.channel.send('そんなことしなくていいから（良心）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'なんでも' in content or '何でも' in content:
            await message.channel.send('ん？今なんでもするって言ったよね？')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if ('いいよ' in content or '良いよ' in content) and 'それ' not in content and 'こいよ' not in content and '来いよ' not in content:
            await message.channel.send('こいよ！')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '屋上' in content or 'まずうち' in content or 'てかない' in content:
            await message.channel.send('まずうちさぁ、屋上あんだけど…焼いてかない？')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '疲' in content or 'つかれ' in content or 'ちかれ' in content or 'きつ' in content:
            await message.channel.send('ﾁｶﾚﾀ…(便乗)')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '待て' in content or 'まて' in content:
            await message.channel.send('肝心な所（意味深）洗い忘れてるゾ')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '枕' in content or 'まくら' in content:
            await message.channel.send('デカすぎます！')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if ('胸' in content and '度' not in content) or 'ふぁ' in content:
            await message.channel.send('ﾌｧｯ!?(驚愕)ｳｰﾝ...(心停止)')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '度胸' in content:
            await message.channel.send('おめぇ度胸足りねぇんだから鍛え直してやるよ 脱げや！（意味不明）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'お待たせ' in content or 'おまたせ' in content or '睡眠' in content or '昏睡' in content or ('飲み' in content or 'のみ' in content) and ('物' in content or 'もの' in content):
            await message.channel.send('アイスティしかなかったんだけど、いいかな？')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '21' in content and ('拳' in content or 'こぶし' in content):
            await message.channel.send('24歳です 学生です')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'みたい' in content or '見たい' in content:
            await message.channel.send('見たけりゃ見せてやるよ！（震え声）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'あ' in content and 'はい' in content:
            await message.channel.send('お前さっき俺ら着替えてる時チラチラ見てただろ')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '警察' in content or '通報' in content:
            await message.channel.send('警察だ！（インパルス板倉）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'ほり' in content or '堀' in content or 'とおる' in content or '通る' in content:
            await message.channel.send('流行らせコラ！')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'ここあ' in content and 'らいおん' in content or 'ここ' in content and ('あらえよ' in content or '洗えよ' in content):
            await message.channel.send('あ、わかりました…')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10
        elif 'ここ' in content:
            await message.channel.send('こ↑こ↓')

        if ('みて' in content or '見て' in content) and 'ない' in content:
            await message.channel.send('嘘つけ絶対見てたゾ')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'ええな' in content or 'えぇな' in content:
            await message.channel.send('あ、いいじゃん　入れたろ♪')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'とかって' in content or ('ますか' in content and 'ますから' not in content):
            await message.channel.send('やりますねぇ！')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '痛い' in content or 'いたい' in content:
            await message.channel.send('痛いですねこれは痛い（冷静）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '王道' in content and ('ゆく' in content or '征く' in content or '行く' in content or 'いく' in content):
            if 'そーぷ' in content:
                await message.channel.send('（王者の風格）')
                yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10
            else:
                await message.channel.send('ソープ系ですか')
                yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if ('ですか' in content or '王道' in content) and 'ゆく' not in content and 'いく' not in content and '征く' not in content and '行く' not in content and 'そーぷ' not in content:
            await message.channel.send('そうですねぇ...やっぱり僕は王道を征く...ソープ系ですか（王者の風格）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'じゃけん' in content:
            await message.channel.send('おっ、そうだな（適当）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'そうだな' in content:
            await message.channel.send('あっそうだ おいKMRァ！（唐突）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'あ' in content and 'そうだ' in content:
            await message.channel.send('おいKMRァ！（唐突）')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'てるか' in content:
            await message.channel.send('バッチェ冷えてますよ')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'この' in content and ('辺' in content or 'へん' in content):
            await message.channel.send('エロい♪')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'なよ' in content:
            await message.channel.send('お前のことがッ！好きだったんだよ！！！')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '白' in content:
            await message.channel.send('はっきりわかんだね')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'はっきり' in content:
            await message.channel.send('すっげぇ白くなってる はっきりわかんだね')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'たまげ' in content or '魂消' in content:
            await message.channel.send('勝手にたまげとけ')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if ('あたり' in content or '当' in content) and ('まえ' in content or '前' in content or '然' in content):
            await message.channel.send('当たり前だよなぁ？？')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'これもう' in content:
            await message.channel.send('この辺がSexy！')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'えろい' in content:
            await message.channel.send('暴れんなよ♪')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'あいすてぃ' in content:
            await message.channel.send('これもう...わかんねぇな')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'れたろ' in content:
            await message.channel.send('すここい歌♪')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        elif 'いいじゃん' in content and 'たろ' not in content:
            await message.channel.send('入れたろ♪')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'すここい' in content:
            await message.channel.send('YAJU&U！')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'yaju' in content and '&' in content:
            await message.channel.send('野獣先輩♪')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '学生' in content or 'がくせい' in content:
            await message.channel.send('学生？あっ...（察し）ふ〜ん')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10
        elif '24' in content:
            await message.channel.send('24歳？もう働いてるの、じゃあ？')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if 'one one four five' in content and 'one four' in content:
            await message.channel.send('いいよ♪こいよ♪')
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

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
                yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10
            else:
                # Webhook使えない → 普通に便乗
                await message.channel.send("そうだよ（便乗）")
                yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

        if '必殺' in content and '発動' in content:
            yaju_icon = "https://keni-77.github.io/inmbotweb/yaju.png"

            # Webhook権限チェック
            perms = message.channel.permissions_for(message.guild.me)

            if perms.manage_webhooks:
                # Webhook使える
                webhooks = await message.channel.webhooks()
                webhook = None

                for wh in webhooks:
                    if wh.name == "yaju_webhook":
                        webhook = wh
                        break

                # なければ作る
                if webhook is None:
                    webhook = await message.channel.create_webhook(name="yaju_webhook")

                # Webhookで便乗
                await webhook.send(
                    '''必殺！野獣の咆哮！
**ヌゥン！ヘッ！ヘッ！**
**ア゛ア゛ア゛ア゛ァ゛ァ゛ァ゛ァ゛**
**ア゛↑ア゛↑ア゛↑ア゛↑ア゛ア゛ア゛ァ゛ァ゛ァ゛ァ゛！！！！**
**ウ゛ア゛ア゛ア゛ア゛ア゛ア゛ァ゛ァ゛ァ゛ァ゛ァ゛ァ゛ァ！！！！！**
**フ ウ゛ウ゛ウ゛ゥ゛ゥ゛ゥ゛ン！！！！**
**フ ウ゛ゥ゛ゥ゛ゥン！！！！(大迫真)**
***（※音量注意）***
  　　　　　　 ▃▆█▇▄▖ 
　　　　　▟◤▖　　　◥█▎ 
　　　◢◤　　▐　　　　▐▉ 
　▗◤　　　▂　▗▖　　▕█▎ 
　◤　▗▅▖◥▄　▀◣　　█▊ 
▐　▕▎◥▖◣◤　　　　◢██ 
█◣　◥▅█▀　　　　▐██◤ 
▐█▙▂　　　　　　◢██◤ 
　◥██◣　　　　◢▄◤ 
　　　▀██▅▇▀''',
                    username="野獣先輩",
                    avatar_url=yaju_icon
                )
                yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10
            else:
                # Webhook使えない
                await message.channel.send('''必殺！野獣の咆哮！
**ヌゥン！ヘッ！ヘッ！**
**ア゛ア゛ア゛ア゛ァ゛ァ゛ァ゛ァ゛**
**ア゛↑ア゛↑ア゛↑ア゛↑ア゛ア゛ア゛ァ゛ァ゛ァ゛ァ゛！！！！**
**ウ゛ア゛ア゛ア゛ア゛ア゛ア゛ァ゛ァ゛ァ゛ァ゛ァ゛ァ゛ァ！！！！！**
**フ ウ゛ウ゛ウ゛ゥ゛ゥ゛ゥ゛ン！！！！**
**フ ウ゛ゥ゛ゥ゛ゥン！！！！(大迫真)**
***（※音量注意）***''')
                yaju_scores[user_id] = yaju_scores.get(user_id, 0) + 10

    @tree.command(name="inmu_rank", description="サーバー内のスコアランキングを表示します")
    async def inmu_rank(interaction: discord.Interaction):
        await interaction.response.defer()

        guild = interaction.guild
        members = guild.members

        # 数値化関数（既存ロジックを流用）
        def encode_to_numbers(text: str) -> str:
            encoded = text.encode("utf-8")
            return "".join(str(b) for b in encoded)

        # パターン（既存）
        patterns = {
            "81": 81,
            "114": 114,
            "514": 514,
            "364": 364,
            "19": 19
        }

        results = []

        for member in members:
            # 基本スコアはグローバル yaju_scores から取得（なければ 0）
            uid = member.id
            base_score = yaju_scores.get(uid, 0)

            # 名前由来のスコア（yaju_scores に無ければ補完として加算して表示に反映）
            display = member.display_name or ""
            globalname = member.global_name or ""

            display_num = encode_to_numbers(display)
            global_num = encode_to_numbers(globalname)

            name_score = 0
            for key, value in patterns.items():
                name_score += display_num.count(key) * value
                name_score += global_num.count(key) * value

            total = base_score + name_score

            results.append((member, total))

        # スコア順に並べ替え
        results.sort(key=lambda x: x[1], reverse=True)

        # Embed 作成
        embed = discord.Embed(
            title="スコアランキング（サーバー内）",
            description="合計スコア",
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
                ranking_text += f"{medals[rank-1]} **{member.display_name}** — スコア：{score}\n"
            else:
                ranking_text += f"{rank}位：**{member.display_name}** — スコア：{score}\n"

        if not ranking_text:
            ranking_text = "該当するメンバーがいません。"

        embed.add_field(
            name="ランキング結果",
            value=ranking_text,
            inline=False
        )

        # サムネイルは1位のアイコン（存在確認）
        if results and results[0][0]:
            try:
                embed.set_thumbnail(url=results[0][0].display_avatar.url)
            except:
                pass

        await interaction.followup.send(embed=embed)


    @tree.command(name="random_number", description="1,3,4,5,6,9からランダムに6回選びます")
    async def random_number(interaction: discord.Interaction):
        # ランダムに数字を選ぶ
        numbers = [1, 3, 4, 5, 6, 9]
        result = [random.choice(numbers) for _ in range(6)]
        
        # 読み方辞書
        reading = { 1: "い", 3: "み", 4: "よ", 5: "こ", 6: "ろ", 9: "く" }
        # 読み方に変換
        reading_result = "".join(reading[n] for n in result)
        user_id = interaction.user.id

        # ヘルパー: 全要素が同じか
        def all_same(lst):
            return all(x == lst[0] for x in lst)

        # まず「完全一致（ゾロ目）」を判定して動的に点数を付与
        if all_same(result):
            d = result[0]
            # 例: d=3 -> score = 333333
            score = int(str(d) * 6)
            await interaction.response.send_message(f"@everyone \n結果: {result}\n\n🎉**ゾロ目**🎉\n獲得点: {score}点")
            yaju_scores[user_id] = yaju_scores.get(user_id, 0) + score
            return

        # それ以外は通常の読み表示（得点なし）
        await interaction.response.send_message(f"結果: {result}\n{reading_result}\n残念だったね")

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
