import flet as ft
import urllib.request
import json

# তোমার পার্সোনাল চাবি
api_key = "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"

def main(page: ft.Page):
    page.title = "Super AI Agent"
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.padding = 20 # মোবাইলের স্ক্রিনের চারপাশে একটু ফাঁকা জায়গা (Safe Area)
    
    chat_history = ft.ListView(expand=True, spacing=10, auto_scroll=True)
    user_input = ft.TextField(hint_text="এখানে তোমার প্রশ্ন লেখো...", expand=True)
    
    def send_click(e):
        if not user_input.value:
            return
        user_text = user_input.value
        user_input.value = ""
        chat_history.controls.append(ft.Text(f"অংশু: {user_text}", size=16, weight=ft.FontWeight.BOLD))
        page.update()
        
        try:
            url = "https://openrouter.ai/api/v1/chat/completions"
            data = {
                "model": "meta-llama/llama-3-8b-instruct:free",
                "messages": [{"role": "user", "content": user_text}]
            }
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            req = urllib.request.Request(url, data=json.dumps(data).encode("utf-8"), headers=headers, method="POST")
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode("utf-8"))
                ai_reply = result["choices"][0]["message"]["content"]
            chat_history.controls.append(ft.Text(f"এআই: {ai_reply}", size=16, color=ft.colors.BLUE))
        except Exception as ex:
            chat_history.controls.append(ft.Text(f"Error: {ex}", color=ft.colors.RED))
        page.update()

    send_btn = ft.ElevatedButton("Send", on_click=send_click)
    
    # 🟢 এই Column-টাই হলো ম্যাজিক, যা মোবাইলে ডিজাইন গায়েব হতে দেবে না!
    main_layout = ft.Column(
        expand=True,
        controls=[
            ft.Text("Super AI Agent 🚀", size=25, weight=ft.FontWeight.BOLD),
            chat_history,
            ft.Row([user_input, send_btn])
        ]
    )
    
    page.add(main_layout)

ft.app(target=main)
        
