# SoundBoard-V1
## DiscordのBotです。

Discordでサウンドボードのような機能が使えるbotです。

誰かさん「いや標準でサウンドボードあるやんｗｗｗ」

という人もいると思いますが、~~Discordのクソ仕様のせいで~~Nitroがないと他のサーバーのサウンドは使えません。

なので、何個でも追加して再生できるようにしたいということで作りました。

(あとPythonの勉強もかねて)

Discord.py V2( https://github.com/Rapptz/discord.py )を使用しています。
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

"volume"はサウンドボードを再生するときの音量です。"prefix"にはサウンドボードを再生するときに使うコマンドの接頭辞です。!などに変えても問題ないです。
