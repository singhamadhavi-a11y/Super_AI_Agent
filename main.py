import flet as ft
import urllib.request
import json

# তোমার পার্সোনাল চাবি
api_key = "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"

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = ft.colors.WHITE
    
    # 🟢 ওপরের হেডলাইন
    top_bar = ft.Container(
        content=ft.Row([
            ft.IconButton(ft.icons.MENU, icon_color=ft.colors.BLACK87),
            ft.Text("Gemini AI", size=22, weight=ft.FontWeight.W_500, color=ft.colors.BLACK87),
            ft.CircleAvatar(content=ft.Icon(ft.icons.PERSON, color=ft.colors.WHITE), bgcolor=ft.colors.PURPLE)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.only(top=15, left=10, right=15, bottom=5)
    )
    
    chat_history = ft.ListView(expand=True, spacing=20, auto_scroll=True, padding=20)
    
    greeting_text = ft.Text("", size=32, weight=ft.FontWeight.W_400, color=ft.colors.BLUE_GREY_700)
    
    welcome_box = ft.Column([
        greeting_text,
        ft.Text("How can I help you today?", size=28, weight=ft.FontWeight.BOLD, color=ft.colors.BLACK87)
    ])
    chat_history.controls.append(welcome_box)
    
    user_input = ft.TextField(
        hint_text="Ask Gemini...", 
        border_radius=30,
        filled=True,
        bgcolor=ft.colors.GREY_100,
        border_color=ft.colors.TRANSPARENT,
        content_padding=15,
        expand=True
    )
    
    loading_ring = ft.ProgressRing(width=20, height=20, visible=False)

    def send_click(e):
        if not user_input.value:
            return
        
        user_text = user_input.value
        user_input.value = ""
        
        if welcome_box in chat_history.controls:
            chat_history.controls.remove(welcome_box)
        
        chat_history.controls.append(
            ft.Row(
                [
                    ft.Container(
                        content=ft.Text(user_text, size=16, color=ft.colors.BLACK87),
                        bgcolor=ft.colors.GREY_200,
                        border_radius=ft.border_radius.all(20),
                        padding=15,
                    )
                ],
                alignment=ft.MainAxisAlignment.END
            )
        )
        
        loading_ring.visible = True
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
            
            chat_history.controls.append(
                ft.Row(
                    [
                        ft.Icon(ft.icons.AUTO_AWESOME, color=ft.colors.BLUE_400),
                        ft.Container(
                            content=ft.Text(ai_reply, size=16, color=ft.colors.BLACK87),
                            expand=True,
                            padding=ft.padding.only(left=10)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.START
                )
            )
        except Exception as ex:
            chat_history.controls.append(ft.Text(f"Error: {ex}", color=ft.colors.RED))
            
        loading_ring.visible = False
        page.update()

    send_btn = ft.IconButton(
        icon=ft.icons.SEND_ROUNDED, 
        icon_color=ft.colors.BLACK87, 
        on_click=send_click
    )
    
    input_area = ft.Container(
        content=ft.Row([
            ft.IconButton(ft.icons.ADD_CIRCLE_OUTLINE, icon_color=ft.colors.BLACK87),
            user_input,
            loading_ring,
            send_btn
        ]),
        padding=ft.padding.only(left=5, right=5, bottom=10, top=5),
        bgcolor=ft.colors.WHITE
    )

    chat_layout = ft.Column(
        expand=True,
        visible=False,
        controls=[top_bar, chat_history, input_area]
    )

    # 🟢 ফিক্সড ওয়েলকাম লগইন স্ক্রিন (এটার জন্যই ফোন হ্যাং করবে না)
    name_field = ft.TextField(hint_text="Enter your name...", width=250, border_radius=20, text_align=ft.TextAlign.CENTER)
    
    def start_app_click(e):
        if name_field.value:
            user_name = name_field.value
            welcome_layout.visible = False
            chat_layout.visible = True
            
            greeting_text.value = f"Hi {user_name}"
            page.update()

    start_button = ft.ElevatedButton("Start Chat", on_click=start_app_click, bgcolor=ft.colors.BLUE_600, color=ft.colors.WHITE)

    welcome_layout = ft.Column(
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        controls=[
            ft.Icon(ft.icons.AUTO_AWESOME, size=80, color=ft.colors.BLUE_400),
            ft.Text("Welcome to Super AI", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            name_field,
            start_button
        ]
    )

    page.add(welcome_layout, chat_layout)

# 🟢 পিওর মোবাইল অ্যাপের কমান্ড
ft.app(target=main)
    
