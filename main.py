import requests
import flet as ft

# 地域ごとのコードを設定
REGIONS = {
    "北海道地方": "010100",
    "東北地方": "010200",
    "関東甲信地方": "010300",
    "東海地方": "010400",
    "北陸地方": "010500",
    "近畿地方": "010600",
    "中国地方 (山口県を除く)": "010700",
    "四国地方": "010800",
    "九州地方": "010900",
    "沖縄地方": "011000",
}

def get_weather_forecast(region_code):
    # 指定された地域の天気予報データを取得
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{region_code}.json"
    # リクエストを送信
    response = requests.get(url)
    if response.status_code == 200:
        # レスポンスデータを取得
        data = response.json()
        # 地域名と天気情報を取得
        area_name = data[0]["timeSeries"][0]["areas"][0]["area"]["name"]
        # 発表日時を取得
        report_datetime = data[0]["reportDatetime"]
        # 天気情報を取得
        weather_forecast = data[0]["timeSeries"][0]["areas"][0]["weathers"]
        # 天気情報を整形して返す
        formatted_forecast = f"発表機関: 気象庁\n発表日時: {report_datetime}\n{area_name} の天気予報:\n"
        formatted_forecast += "\n".join([f"- {weather}" for weather in weather_forecast])
        return formatted_forecast
    else:
        return None

def main(page: ft.Page):
    page.title = "天気予報検索"
    # ページの配置を設定
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START

# 選択された地域コードを保持
    selected_region_code = ft.Text(value="", visible=False)

    # 天気予報表示用テキスト
    weather_info = ft.Text(value="地域を選択してください", size=16)

    # ドロップダウンリストの作成
    dropdown = ft.Dropdown(
        hint_text="地域を選択",
        options=[
            ft.dropdown.Option(text=name, key=code) for name, code in REGIONS.items()
        ],
        on_change=lambda e: update_weather(e.control.value),
    )

    # 天気情報を更新する関数
    def update_weather(region_code):
        if region_code:
            selected_region_code.value = region_code
            weather_info.value = get_weather_forecast(region_code)
            page.update()

    # レイアウトを構築
    page.add(
        ft.Column(
            [
                ft.Text("天気予報", size=24, weight="bold"),
                dropdown,
                ft.Container(weather_info, padding=20, bgcolor=ft.colors.BLUE_50),
            ],
            spacing=20,
        )
    )


# アプリを起動
ft.app(target=main)