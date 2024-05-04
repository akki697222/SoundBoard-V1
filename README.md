# SoundBoard-V1
## DiscordのBotです。

Discordのサーバー上でサウンドボードのような機能が使えるbotです。

例えば「いや標準でサウンドボードあるやんｗｗｗ」

という人もいると思いますが、~~Discordのクソ仕様のせいで~~Nitroがないと他のサーバーのサウンドは使えません。

なので、何個でも追加して再生できるようにしたいということで作りました。

(あとPythonの勉強もかねて)

Discord.py( https://github.com/Rapptz/discord.py )を使用して作成しました。
このbotを使いたい方はbot-envフォルダ内にconfig.jsonを作成し、以下のコードをコピぺしてください。
```json:config.json
{
    "token":"Your token Here",
    "showtoken":"true",
    "volume":"0.5",
    "prefix":"."
}
```

"Your token Here"の場所にはBotのトークンを記載してください。

"volume"はサウンドボードを再生するときの音量です。"prefix"にはサウンドボードを再生するときに使うコマンドの接頭辞です。`!`などに変えても問題ないです。

"showtoken"は起動時のログにtokenを記載するかの設定です。

サウンドの追加方法を書いてたけどめんどくさいのでsounds.jsonとかを見て自分でやってください(投げやり

あ、あとffmpegの実行ファイルをbot-envに入れておいてね。それとDiscord.pyは[voice]付きでインストールしないと動かないので注意

サウンドを再生する場合は`soundboard`という名前のチャンネルを作ってそこで`.p [sound]` のように実行してください。

説明が分かりづらかったらすまない。
