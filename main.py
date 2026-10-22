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
server_scores = {}

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
        if user_id not in server_scores:
            server_scores[user_id] = 0

        servers = len(client.guilds)
        await client.change_presence(status=discord.Status.online, activity=discord.CustomActivity(name=f'導入されているサーバー数：{servers}'))
        content = unicodedata.normalize("NFKC", message.content)
        content = jaconv.kata2hira(content)
        content = content.lower()

        if '人生' in content or 'じんせい' in content or 'life' in content or 'らいふ' in content:
            await message.channel.send('人生は運ゲーだ')
            server_scores[user_id] = server_scores.get(user_id, 0) + 10

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
