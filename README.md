# Presenter Table Generator

Portal に WIP/TERM の発表ページを作る時に楽するためのスクリプト。

具体的には、発表者一覧のテーブルを作成する。

## 使い方

### 必要なもの

- Nix
  - Nix Flakes を有効化する
- または Python
  - pyyaml をインストールする

### 実行方法

#### 1. 発表者データを含む YAML ファイルを用意する

presenters.sample.yaml をみてよしなにかく。

```presenters.yaml
wip:
  one:
    - kino-ma
    - mirai: "ほげほげ研究"
  d-hacks:
    - tsukky

term:
  sensys:
    - dang0
```

基本は *発表種別 > KG > ログイン名のリスト*。
ログイン名の部分を `ログイン名: 発表タイトル` に変えるとタイトル付きで生成できる。

#### 2. 実行する

```
python3 ./generator/main.py <入力ファイル名>
```

実行例:

```
$ nix develop
$ python3 ./generator/main.py ./presenters.sample.yaml
| 種別 | ログイン名 | KG | 発表ページ |
| wip | kino-ma | one | 自分の研究タイトル |
| wip | mirai | one | ほげほげ研究 |
| wip | tsukky | d-hacks | 自分の研究タイトル |
| term | dang0 | sensys | 自分の研究タイトル |
```