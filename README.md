# HEIC → JPG 変換ツール

HEIC / HEIF画像をJPGに変換する、Windows向けのシンプルなデスクトップアプリです。日本語の画面で操作できます。

## できること

- 複数画像の一括変換
- 保存先フォルダの指定
- JPG品質の調整（1〜100、標準値92）
- 同名ファイルがある場合の連番保存（上書き防止）
- 変換の進捗と、成功・失敗件数の表示

画像はPC内で処理します。画像のアップロードや外部サービスへの送信は行いません。元のHEICファイルも変更しません。

## 起動方法

このリポジトリではソースコードを公開しています。配布用EXEは含まれていません。

Windows 64bit版のPython 3.9以降と、Tcl/Tk（tkinter）が必要です。開発時の変換確認にはPython 3.9を使用しました。Pythonの公式インストーラーでは、Tcl/Tkのインストールを有効にしてください。

PowerShellで以下を実行します。

```powershell
git clone https://github.com/cac-gwd/heic-to-jpg.git
cd heic-to-jpg
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe heic_to_jpg.py
```

依存ライブラリのインストール時にはインターネット接続が必要です。変換時には不要です。

## 使い方

1. 「HEIC画像を選択（複数可）」から画像を選択します。
2. 保存先フォルダを指定します。初期値は、最初に選んだ画像と同じ場所にある `JPG` フォルダです。
3. 必要に応じてJPG品質を変更します。
4. 「JPGに変換」を押します。

例：`photo.heic` は `photo.jpg` になります。すでに同名のファイルがある場合は、`photo_1.jpg`、`photo_2.jpg` のように保存します。

## Windows用EXEの作成

公式PythonのTcl/Tkが利用できる環境で、次のコマンドを実行してください。

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-build.txt
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --onefile --windowed --name HEIC-to-JPG --collect-all pillow_heif --exclude-module numpy heic_to_jpg.py
```

`dist/HEIC-to-JPG.exe` が生成されます。作成後のEXEはPythonをインストールしていないPCでも起動できる形式です。別PCでの動作は、そのPCで確認してください。

生成したEXEには依存ライブラリも同梱されます。EXEを第三者へ再配布するときの依存関係については、[THIRD_PARTY.md](THIRD_PARTY.md) を確認してください。

## 動作上の制約

- JPGは非可逆圧縮です。品質100でも完全な可逆変換にはなりません。
- HDR画像は8bit JPGへ変換されるため、見え方が変わる場合があります。
- 透過部分は白で塗りつぶします。
- 複数画像を格納したHEIFは、開いた時点で選択されている1枚を変換します。全フレームやLive Photosの動画は出力しません。
- 位置情報などのEXIFやXMP、ICCプロファイルは引き継ぎません。向きの情報は画素へ適用して保存します。
- 壊れたファイルや対応していない圧縮方式の画像は、エラーとして表示される場合があります。
- 変換中はアプリを閉じずに完了を待ってください。

## 検証

合成した小さなHEIC画像を使った変換、重複名の保護、不正ファイルでのエラー、向き補正、透過部分とメタデータの扱いを確認できます。個人の写真はテストに含まれません。

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

## ライセンス

このリポジトリのアプリのソースコードと文書は [MIT License](LICENSE) です。Pillow、pillow-heifなどの依存ライブラリには、それぞれ別のライセンスが適用されます。詳細は [THIRD_PARTY.md](THIRD_PARTY.md) を参照してください。
