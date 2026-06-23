import flet as ft
import urllib.request
import json

# তোমার পার্সোনাল চাবি
api_key = "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"

def main(page: ft.Page):
    # প্রো-লেভেল অ্যাপ ডিজাইন
    page.title = "Super AI Agent"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = ft.colors.GREY_900
    page.window_width = 400
    page.window_height = 800

    page.appbar = ft.AppBar(
        title=ft.Text("Super AI Agent 🚀", weight=ft.FontWeight.BOLD, color=ft.colors.WHITE), 
        bgcolor=ft.colors.BLUE_GREY_900,
        center_title=True
    )

    # চ্যাট লিস্ট (অটো স্ক্রোল হবে)
    chat_history = ft.ListView(expand=True, spacing=15, auto_scroll=True)
    
    # সুন্দর ইনপুট বক্স
    user_input = ft.TextField(
        hint_text="তোমার নির্দেশ এখানে লেখো...", 
        expand=True, 
        border_radius=20,
        filled=True,
        bgcolor=ft.colors.GREY_800
    )
    
    # লোডিং আইকন (যখন এআই ভাববে)
    loading_ring = ft.ProgressRing(visible=False, width=20, height=20, color=ft.colors.CYAN_ACCENT)

    def send_click(e):
        if not user_input.value:
            return

        user_text = user_input.value
        user_input.value = ""
        
        # ইউজারের মেসেজ
        chat_history.controls.append(
            ft.Container(
                content=ft.Text(f"অংশু: {user_text}", color=ft.colors.WHITE, size=16),
                bgcolor=ft.colors.BLUE_700,
                border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_left=15),
                padding=12,
                alignment=ft.alignment.center_right
            )
        )
        
        loading_ring.visible = True
        page.update()

        # এআই-এর ম্যাজিক উত্তর আনা (পুরোপুরি পাইথনের নিজস্ব নিয়মে)
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
            
            # এআই-এর মেসেজ
            chat_history.controls.append(
                ft.Container(
                    content=ft.Text(f"এআই: {ai_reply}", color=ft.colors.BLACK, size=16),
                    bgcolor=ft.colors.GREEN_ACCENT_400,
                    border_radius=ft.border_radius.only(top_left=15, top_right=15, bottom_right=15),
                    padding=12,
                    alignment=ft.alignment.center_left
                )
            )
        except Exception as ex:
            chat_history.controls.append(
                ft.Text(f"Error: {ex}", color=ft.colors.RED_400, italic=True)
            )
        
        loading_ring.visible = False
        page.update()

    send_btn = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED, 
        icon_color=ft.colors.CYAN_ACCENT_400, 
        icon_size=30,
        on_click=send_click
    )
    
    # স্ক্রিনের সব কিছু সাজানো
    page.add(
        chat_history,
        ft.Row([loading_ring], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([user_input, send_btn], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )

ft.app(target=main)
    
