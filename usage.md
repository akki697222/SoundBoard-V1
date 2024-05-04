bot-envフォルダ内にconfig.jsonを作成し、以下のコードをコピぺしてください。
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

サウンドに関してはbot-env内にsoundsフォルダを作成し、追加したいサウンドと同時にsounds.jsonをsoundsフォルダ内に作成してください。

例として"bruh.mp3"をsoundsに追加してbotで使用する場合、sounds.jsonは以下のようになります。
```json:sounds.json
{
  "bruh": "sounds/bruh.mp3"
}
```
これらは追加するサウンドに応じて変更してください。

分かりづらかったらごめんね。
