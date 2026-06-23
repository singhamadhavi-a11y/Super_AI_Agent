import flet as ft
from openai import OpenAI
import os

# GitHub Secrets থেকে তোমার সুরক্ষিত API Key নেবে
api_key = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

def main(page: ft.Page):
    # অ্যাপের ডিজাইন এবং থিম
    page.title = "Super AI Agent"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 400
    page.window_height = 800

    chat_history = ft.ListView(expand=True, spacing=10)
    user_input = ft.TextField(hint_text="তোমার প্রশ্ন বা নির্দেশ লেখো...", expand=True)

    def send_click(e):
        if not user_input.value:
            return

        # তোমার দেওয়া মেসেজ স্ক্রিনে দেখানো
        user_text = user_input.value
        chat_history.controls.append(ft.Text(f"অংশু: {user_text}", color=ft.colors.BLUE_200))
        user_input.value = ""
        page.update()

        # এআই-এর ম্যাজিক উত্তর আনা
        try:
            response = client.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct:free",
                messages=[{"role": "user", "content": user_text}]
            )
            ai_reply = response.choices[0].message.content
            chat_history.controls.append(ft.Text(f"এআই: {ai_reply}", color=ft.colors.GREEN_200))
        except Exception as ex:
            chat_history.controls.append(ft.Text(f"Error: {ex}", color=ft.colors.RED_400))
        
        page.update()

    send_btn = ft.IconButton(icon=ft.icons.SEND, on_click=send_click)
    
    # স্ক্রিনের সব কিছু সাজানো
    page.add(
        ft.Text("Super AI Agent V1.0", size=24, weight=ft.FontWeight.BOLD),
        chat_history,
        ft.Row([user_input, send_btn])
    )

ft.app(target=main)
  
