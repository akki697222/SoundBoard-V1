bot-envフォルダ内にconfig.jsonを作成し、以下のコードをコピぺしてください。
↑あらかじめ用意しておいたinit関数を実行すれば作ってくれます
```json:config.json
{
    "token":"Your token Here",
    "showtoken":"true",
    "volume":"0.5",
    "prefix":".",
    "autoconnect": true
}
```

"Your token Here"の場所にはBotのトークンを記載してください。(変更せずに実行しても動きません)

"volume"はサウンドボードを再生するときの音量です。 Discordのコマンドからも変更可能です。

"prefix"にはサウンドボードを再生するときに使うコマンドの接頭辞です。`!`などに変えても問題ないです。 

"showtoken"は起動時のログにtokenを記載するかの設定です。

"autoconnect"は何かしらサウンドを再生するとき自動でVCに参加するかの設定です。 Discordのコマンドからも変更可能です。

~~サウンドに関してはbot-env内にsoundsフォルダを作成し、追加したいサウンドと同時にsounds.jsonをsoundsフォルダ内に作成してください。~~

~~例として"bruh.mp3"をsoundsに追加してbotで使用する場合、sounds.jsonは以下のようになります。~~
```json:sounds.json
{
  "bruh": "sounds/bruh.mp3"
}
```
~~これらは追加するサウンドに応じて変更してください。~~

/addsound コマンドを実装したのでdiscordから実行すれば勝手にやってくれます。

分かりづらかったらごめんね。


BOTアカウントの作成方法などは公式の記事などを参考にしてください。ここではあくまでもこのBOTの使用方法のみ記載しておきます。
