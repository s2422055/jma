import requests
import flet as ft

def get_weather_forecast(region_code):
    url = f"https://www.jma.go.jp/bosai/forecast/data/forecast/{region_code}.json"
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
    def search_weather(e):
        area_code = area_code_input.value
        forecast = get_weather_forecast(area_code)
        if forecast:
            result.value = forecast
        else:
            result.value = "天気予報を取得できませんでした。"
        page.update()

    area_code_input = ft.TextField(label="地域コードを入力")
    search_button = ft.ElevatedButton(text="検索", on_click=search_weather)
    result = ft.Text()

    page.add(area_code_input, search_button, result)

# アプリを起動
ft.app(target=main)