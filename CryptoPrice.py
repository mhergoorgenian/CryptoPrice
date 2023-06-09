import requests
import time
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.clock import Clock

class BitcoinPriceApp(App):
    def build(self):
        self.coins = [
            {"id": "bitcoin", "name": "Bitcoin"},
            {"id": "ethereum", "name": "Ethereum"},
            {"id": "litecoin", "name": "Litecoin"}
        ]  # Add more coins if needed

        self.price_label = Label(text="Fetching Bitcoin price...")
        self.current_coin_id = self.coins[0]["id"]  # Initialize current coin ID

        button_layout = BoxLayout(orientation="horizontal")
        for coin in self.coins:
            button = Button(text=coin["name"], on_release=self.on_button_press)
            button.coin_id = coin["id"]  # Store the coin ID as a custom property
            button_layout.add_widget(button)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.price_label)
        layout.add_widget(button_layout)

        # Schedule the update_price method to run every 5 seconds
        Clock.schedule_interval(self.update_price, 10)

        return layout

    def update_price(self, *args):
        try:
            selected_coin = next(coin for coin in self.coins if coin["id"] == self.current_coin_id)
            price = self.get_coin_price(selected_coin["id"])
            self.price_label.text = f"Current {selected_coin['name']} Price: $" + str(price)
        except requests.exceptions.RequestException as e:
            self.price_label.text = "Error fetching coin price: " + str(e)

    def get_coin_price(self, coin_id):
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()
        coin_price = data[coin_id]["usd"]
        return coin_price

    def on_button_press(self, button):
        self.current_coin_id = button.coin_id
        self.update_price()

if __name__ == "__main__":
    BitcoinPriceApp().run()
