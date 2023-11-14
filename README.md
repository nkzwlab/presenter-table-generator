# Presenter Table Generator

Portal に WIP/TERM の発表ページを作る時に楽するためのスクリプト。

具体的には、発表者一覧のテーブルを作成する。

## 使い方

### 必要なもの

- Nix
  - Nix Flakes を有効化する
- または Python がある環境
  - pyyaml をインストールする

### 実行方法

#### 1. 発表者データを含む YAML ファイルを用意する

presenters.sample.yaml をみてよしなにかく。


```sh
cp presenters.sample.yaml presenters.yaml
```

`presenters.yaml` を編集

```yaml:presenters.yaml
config:
  # テーブル内に埋め込むリンクをどこに作るかのオプション
  # たとえば ./term_mid なら ./term_mid/kino-ma でリンクが作られる
  presentation_page_root: "./term_mid"
  start_time: "11:10"
  presentation_time:
    wip: 10
    term: 15
  breaks:
    # after で指定すると、その時間以降の一番早いタイミングで休憩が入る
    - after: "12:20"
      length: 40
      title: お昼休憩
    # before で指定すると、その時間以前の一番遅いタイミングで休憩が入る
    # 休憩の終了時刻ではなく開始時刻が指定時間になることに注意
    - before: "14:30"
      length: 15
    - before: "16:15"
      length: 15

presenters:
  # wip または term に対応。小文字オンリー
  wip:
    # テーブルでの表記がこの KG 名そのままになるので、大文字・小文字が正しくなるよう注意する
    ONE:
      - kino-ma
      # 既知のタイトルがあれば指定可能
      - mirai: "ほげほげ研究"
    D-Hacks:
      - tsukky
    WellComp:
      - kino-ma
    SenSys:
      - kino-ma

  term:
    SenSys:
      - dang0
    ONE:
      - kino-ma
      - kino-ma
      - kino-ma
      - kino-ma
      - kino-ma
      - kino-ma
      - kino-ma
      - kino-ma
      - kino-ma
      - kino-ma
      - kino-ma
```

#### 2. 実行する

```
nix develop
python3 ./generator/main.py presenters.yaml
```

実行結果はこんな感じ

```md
| 種別 / Kind | 発表時間 / Presentation time | ログイン名 / Login name | KG | 発表タイトル |
| --- | --- | --- | --- | --- |
| WIP | 11:10 - 11:20 | kino-ma | WellComp | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 11:20 - 11:35 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 11:35 - 11:50 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 11:50 - 12:05 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 12:05 - 12:20 | dang0 | SenSys | [自分の研究タイトル](./term_mid/dang0) |
| 休憩 / Break | 12:20 - 13:00 |  |  | お昼休憩 |
| WIP | 13:00 - 13:10 | kino-ma | SenSys | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 13:10 - 13:25 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 13:25 - 13:40 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| WIP | 13:40 - 13:50 | tsukky | D-Hacks | [自分の研究タイトル](./term_mid/tsukky) |
| TERM | 13:50 - 14:05 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 14:05 - 14:20 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| 休憩 / Break | 14:20 - 14:35 |  |  |  |
| TERM | 14:35 - 14:50 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 14:50 - 15:05 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 15:05 - 15:20 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| WIP | 15:20 - 15:30 | mirai | ONE | [ほげほげ研究](./term_mid/mirai) |
| TERM | 15:30 - 15:45 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| WIP | 15:45 - 15:55 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
```

<details>
<summary>表示はこんな感じ</summary>

| 種別 / Kind | 発表時間 / Presentation time | ログイン名 / Login name | KG | 発表タイトル |
| --- | --- | --- | --- | --- |
| WIP | 11:10 - 11:20 | kino-ma | WellComp | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 11:20 - 11:35 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 11:35 - 11:50 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 11:50 - 12:05 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 12:05 - 12:20 | dang0 | SenSys | [自分の研究タイトル](./term_mid/dang0) |
| 休憩 / Break | 12:20 - 13:00 |  |  | お昼休憩 |
| WIP | 13:00 - 13:10 | kino-ma | SenSys | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 13:10 - 13:25 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 13:25 - 13:40 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| WIP | 13:40 - 13:50 | tsukky | D-Hacks | [自分の研究タイトル](./term_mid/tsukky) |
| TERM | 13:50 - 14:05 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 14:05 - 14:20 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| 休憩 / Break | 14:20 - 14:35 |  |  |  |
| TERM | 14:35 - 14:50 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 14:50 - 15:05 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| TERM | 15:05 - 15:20 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| WIP | 15:20 - 15:30 | mirai | ONE | [ほげほげ研究](./term_mid/mirai) |
| TERM | 15:30 - 15:45 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
| WIP | 15:45 - 15:55 | kino-ma | ONE | [自分の研究タイトル](./term_mid/kino-ma) |
</details>

#### 3. Portal にはりつける

Meeting ページを作って、発表者一覧に貼り付ける。

## Contacts

何かあれば kino-ma にきいてください。