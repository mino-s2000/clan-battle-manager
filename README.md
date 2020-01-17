# Clan Battle Manager

## Overview (Japanese Only)

Cygames社からリリースされているスマホ向けRPG「プリンセスコネクト Re:Dive」のクランバトルの諸々の管理を補助する Discord Bot です。

## 実装済み

- 凸報告

## 実装予定

- ダメージ集計
  - バトルログのOCR
  - Google Spreadsheetsへの自動書き込み
  - 集計、グラフ作成、グラフ投稿
- 凸宣言のサマライズ
  - 同時凸／連携凸やダメコンの自動判別
  - ラスアタ判別
- 凸宣言<->凸報告の連携
- [PriLog](https://prilog.jp/) APIを利用したTL書き起こし

## Requirement

- Python 3.6

## How to use

1. Clone
  
    ```bash
    git clone https://github.com/mino-s2000/clan-battle-manager.git
    ```

2. Modify any parameters.
    - discordbot.py

        ```
        DISCORD_TOKEN = ''
        ```

    - config.ini
    - cogs/attacking-count.py

        ```
        SECTION = 'dev'
        #SECTION = 'prod'
        EMOJI_ONE = '\U0001F95A'
        EMOJI_TWO = '\U0001F423'
        EMOJI_THREE = '\U0001F425'
        ```

3. Install modules

    ```bash
    pip install -U -r requirements.txt
    ```

4. Run

    ```bash
    python ./discordbot.py
    ```

## LICENSE

MIT License

## Author

mino-s2000
