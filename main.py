import flet as ft
import random
import time
import smtplib


def main(page: ft.Page):
    page.title = "Match it! - Picture Matching Memory Game"
    page.theme_mode = ft.ThemeMode.DARK
    page.window_width = 1000
    page.window_height = 800
    page.window_resizable = False
    page.window_maximizable = False
    page.window_top = 0
    page.window_left = -7
    page.padding = 25
    page.vertical_alignment = ft.MainAxisAlignment.SPACE_AROUND

    password = "PASS"
    hints = ("Reveal one correct pair", "Reveal first 3 pics", "Add more time and moves")
    themes = ("cats", "dogs", "flowers")
    no_of_pics = (6, 12, 16, 20)
    x_dimentions = (3, 4, 4, 5)
    y_dimentions = (2, 3, 4, 4)
    time_limits = (30, 60, 80, 100)
    moves_limits = (5, 10, 12, 15)
    answer_pairs = list()
    selected = []

    def rate_game(self):
        global time_taken, lvl, player_name
        self.control.disabled = True
        rating_slider.current.disabled = True
        page.update()
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'mosaabgka@gmail.com'
        smtp_password = 'kjayrwlmylamlubg'
        from_email = 'mosaabgka@gmail.com'
        to_email = 'matchit@mosaab.is-a.dev'
        subject = 'New Rating for Matchit!'
        body = f'Hello, Developer of Matchit!\nA player called {player_name} has sent you this rating for Matchit Game\nRating: {int(rating_slider.current.value)}/10\nComments: "{self.control.value}"\nBR,\nMatchit Game Software.'
        message = f'Subject: {subject}\n\n{body}'
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(from_email, to_email, message)
            smtp.close()
        self.control.value = f"Rating and comments were successfully sent to the developers of Matchit."
        page.update()

    def send_score(self):
        global time_taken, answered, lvl, player_name
        self.control.disabled = True
        page.update()
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'mosaabgka@gmail.com'
        smtp_password = 'kjayrwlmylamlubg'
        from_email = 'mosaabgka@gmail.com'
        to_email = f'{self.control.value}'
        subject = 'Your Result from Match It Game!'
        body = f'Hello, {player_name}!\nYou have matched {answered} correct pairs of pictures in {round(time_taken, 1)} seconds in Level {lvl+1} in Match It Game!\nBR,\nMatch It Developers Team.'
        message = f'Subject: {subject}\n\n{body}'
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(from_email, to_email, message)
            smtp.close()
        self.control.value = f"Email was successfully sent to {self.control.value}."
        page.update()

    def lose_game():
        global player_name, lvl, moves_done, time_taken, rating_slider
        rating_slider = ft.Ref[ft.Slider]()
        time_taken = time.time() - start_time
        page.controls.clear()
        page.add(
            ft.Text(f"You Lost...", size=36, weight=ft.FontWeight.W_800),
            ft.Row([
                ft.Column([
                    ft.Text("Send your result to your email inbox", size=24),
                    ft.TextField(label="Email", hint_text="Enter your email then press ENTER", on_submit=send_score),
                ], width=450, alignment=ft.MainAxisAlignment.START),
                ft.Column([
                    ft.Text("Rate our game", size=24),
                    ft.Slider(min=0, max=10, value=5, label="{value}", divisions=10, ref=rating_slider),
                    ft.TextField(label="Comments", hint_text="Type whatever you want...", on_submit=rate_game)
                ], width=450, alignment=ft.MainAxisAlignment.START),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.FilledButton("Play Again", on_click=open_game_options)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def win_game():
        global player_name, lvl, moves_done, time_taken, rating_slider
        rating_slider = ft.Ref[ft.Slider]()
        time_taken = time.time() - start_time
        page.controls.clear()
        page.add(
            ft.Text(f"🎉 Congrats, {player_name}!", size=36, weight=ft.FontWeight.W_800),
            ft.Text(f"You matched all the pictures of Level {lvl+1} within the time and moves limits set to that level.\nYou finished with {round(time_limits[lvl]-time_taken, 1)} seconds left and {int(moves_limits[lvl]-moves_done)} moves left.",
                    size=24, weight=ft.FontWeight.W_600),
            ft.Row([
                ft.Column([
                    ft.Text("Send your result to your email inbox", size=24),
                    ft.TextField(label="Email", hint_text="Enter your email then press ENTER", on_submit=send_score),
                ], width=450, alignment=ft.MainAxisAlignment.START),
                ft.Column([
                    ft.Text("Rate our game", size=24),
                    ft.Slider(min=0, max=10, value=5, label="{value}", divisions=10, ref=rating_slider),
                    ft.TextField(label="Comments", hint_text="Type whatever you want...", on_submit=rate_game)
                ], width=450, alignment=ft.MainAxisAlignment.START),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                ft.FilledButton("Play Again", on_click=open_game_options)
            ], alignment=ft.MainAxisAlignment.CENTER)
        )

    def check_timer():
        if time.time()-start_time <= time_limits[lvl] and moves_limits[lvl]-moves_done > 0:
            timer.current.value = f"{time_limits[lvl]-(time.time()-start_time):.1f}secs"
            page.update()
            return True
        else:
            lose_game()
            return False

    def picture_selected(e):
        global answer_pairs, answered, moves_done, theme
        if not check_timer(): return None
        if len(selected) == 0:
            selected.append(e.control.data[0])
            e.control.style.side = ft.BorderSide(2, ft.colors.WHITE)
            e.control.content.content.src = f"/images/{themes[theme]}/{e.control.data[1]}.jpg"
            page.update()
        else:
            if e.control.data[0] in selected:
                e.control.style.side = ft.BorderSide(0, ft.colors.WHITE)
                e.control.content.content.src = f"/images/q.jpg"
                page.update()
                selected.remove(e.control.data[0])
            else:
                selected.append(e.control.data[0])
                e.control.style.side = ft.BorderSide(2, ft.colors.WHITE)
                e.control.content.content.src = f"/images/{themes[theme]}/{e.control.data[1]}.jpg"
                moves_done += 1
                moves.current.value = f"{moves_limits[lvl]-moves_done}moves"
                page.update()
                selected_mirror = selected[-1:-3:-1]
                time.sleep(0.3)
                check_timer()
                if selected in answer_pairs:
                    answer_pairs.remove(selected)
                    for i in selected:
                        pics_grid.current.controls[i].style.side = ft.BorderSide(0, ft.colors.GREEN)
                        pics_grid.current.controls[i].disabled = True
                    answered += 1
                    corrects.current.value = f"{answered}/{no_of_pics[lvl]//2}"
                    page.update()
                    selected.clear()
                    selected_mirror.clear()
                    if answered == no_of_pics[lvl]//2:
                        time.sleep(1)
                        win_game()
                elif selected_mirror in answer_pairs:
                    answer_pairs.remove(selected_mirror)
                    for i in selected_mirror:
                        pics_grid.current.controls[i].style.side = ft.BorderSide(0, ft.colors.GREEN)
                        pics_grid.current.controls[i].disabled = True
                    answered += 1
                    corrects.current.value = f"{answered}/{no_of_pics[lvl]//2}"
                    page.update()
                    selected.clear()
                    selected_mirror.clear()
                    if answered == no_of_pics[lvl]//2:
                        time.sleep(1)
                        win_game()
                else:
                    for i in selected:
                        pics_grid.current.controls[i].style.side = ft.BorderSide(0, ft.colors.WHITE)
                        pics_grid.current.controls[i].content.content.src = f"/images/q.jpg"
                    page.update()
                    selected.clear()
                    selected_mirror.clear()

    def add_time_moves():
        global moves_done, start_time
        moves_done -= 3
        start_time += 30
        moves.current.value = f"{moves_limits[lvl] - moves_done}moves"
        hint_button.current.disabled = True
        check_timer()

    def reveal_3_pics():
        n = 3
        x = 0
        reveals = []
        while n > 0 and x < no_of_pics[lvl]:
            e = pics_grid.current.controls[x]
            x += 1
            if not e.disabled:
                e.content.content.src = f"/images/{themes[theme]}/{e.data[1]}.jpg"
                reveals.append(x - 1)
                n -= 1
        hint_button.current.disabled = True
        check_timer()
        page.update()
        time.sleep(1.5)
        for i in reveals:
            e = pics_grid.current.controls[i]
            e.content.content.src = f"/images/q.jpg"
        check_timer()
        page.update()

    def reveal_correct_pair():
        global answered, answer_pairs
        selected = answer_pairs[0]
        answer_pairs.remove(selected)
        for i in selected:
            e = pics_grid.current.controls[i]
            e.content.content.src = f"/images/{themes[theme]}/{e.data[1]}.jpg"
            e.style.side = ft.BorderSide(0, ft.colors.GREEN)
            e.disabled = True
        hint_button.current.disabled = True
        answered += 1
        corrects.current.value = f"{answered}/{no_of_pics[lvl] // 2}"
        check_timer()
        page.update()
        selected.clear()
        if answered == no_of_pics[lvl] // 2:
            time.sleep(1)
            win_game()

    def use_hint(self):
        if self.control.data == 0: reveal_correct_pair()
        elif self.control.data == 1: reveal_3_pics()
        else: add_time_moves()

    def generate_answers(number_of_pics):
        pics = [i for i in range(number_of_pics // 2)] * 2
        random.shuffle(pics)
        random.shuffle(pics)
        random.shuffle(pics)
        ans = [[] for i in range(number_of_pics // 2)]
        for i in range(number_of_pics):
            ans[pics[i]].append(i)
        return ans

    pics_grid = ft.Ref[ft.GridView]()
    timer = ft.Ref[ft.Text]()
    moves = ft.Ref[ft.Text]()
    corrects = ft.Ref[ft.Text]()
    hint_button = ft.Ref[ft.OutlinedButton]()

    def start_game(self):
        global player_name, answered, answer_pairs, lvl, moves_done, theme, hint
        answer_pairs = generate_answers(no_of_pics[lvl])
        page.controls.clear()
        answered, moves_done = 0, 0
        time_left = x_dimentions[lvl]
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.add(
            ft.Row([
                ft.Container(content=ft.Row([
                    ft.Icon(name=ft.icons.PERSON),
                    ft.Text(f"{player_name}", size=24, weight=ft.FontWeight.W_600),
                ])),
                ft.Text(f"{time_left}secs", size=24, ref=timer),
                ft.Text(f"{moves_limits[lvl]-moves_done}moves", size=24, ref=moves),
                ft.Text(f"{answered}/{no_of_pics[lvl]//2}", size=24, ref=corrects),
                ft.OutlinedButton(f"{hints[hint]}",
                                  icon=ft.icons.LIGHTBULB_OUTLINED,
                                  data=hint,
                                  on_click=use_hint, disabled=True, ref=hint_button),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Divider(),
            ft.GridView(
                ref=pics_grid,
                expand=1,
                runs_count=x_dimentions[lvl],
                child_aspect_ratio=1.5,
                width=900
            )
        )
        pics_grid.current.controls = [None for i in range(no_of_pics[lvl])]
        for i in range(len(answer_pairs)):
            for j in range(2):
                indx = answer_pairs[i][j]
                pics_grid.current.controls[indx] = ft.OutlinedButton(
                    content=ft.Container(
                        content=ft.Image(
                            src=f"/images/{themes[theme]}/{i}.jpg",
                            fit=ft.ImageFit.COVER,
                            border_radius=ft.border_radius.all(7),
                        )
                    ),
                    style=ft.ButtonStyle(
                        shape=ft.ContinuousRectangleBorder(radius=20),
                    ),
                    disabled=True, data=(indx, i), on_click=picture_selected,
                )
        page.update()
        for i in range(x_dimentions[lvl]):
            time.sleep(1)
            time_left -= 1
            timer.current.value = f"{time_left}secs"
            page.update()
        for control in pics_grid.current.controls:
            control.content.content.src = f"/images/q.jpg"
            control.disabled = False
        hint_button.current.disabled = False
        timer.current.value = f"{time_limits[lvl]}secs"
        global start_time
        start_time = time.time()
        page.update()

    game_levels = ft.Ref[ft.Row]()
    game_themes = ft.Ref[ft.Row]()
    game_hints = ft.Ref[ft.Row]()

    def hint_selected(self):
        global hint
        game_hints.current.controls[hint].style.side = ft.BorderSide(0, ft.colors.WHITE70)
        hint = self.control.data
        self.control.style.side = ft.BorderSide(2, ft.colors.WHITE)
        page.update()

    def theme_selected(self):
        global theme
        game_themes.current.controls[theme].style.side = ft.BorderSide(0, ft.colors.WHITE70)
        theme = self.control.data
        self.control.style.side = ft.BorderSide(2, ft.colors.WHITE)
        page.update()

    def level_selected(self):
        global lvl
        game_levels.current.controls[lvl].style.side = ft.BorderSide(0, ft.colors.WHITE70)
        lvl = self.control.data
        self.control.style.side = ft.BorderSide(2, ft.colors.WHITE)
        page.update()

    def open_game_options(e):
        global player_name, lvl, theme, hint
        lvl, theme, hint = 0, 0, 0
        page.controls.clear()
        page.add(
            ft.Row([
                ft.Icon(name=ft.icons.PERSON),
                ft.Text(f"{player_name}", size=24, weight=ft.FontWeight.W_600)
            ]),
            ft.Column([
                ft.Text("Choose game level", size=24, weight=ft.FontWeight.W_800),
                ft.Row([
                    ft.OutlinedButton(
                        content=ft.Text("Level 1\n3×2 Grid of Pics. 30 Secs. 5 Moves.", text_align=ft.TextAlign.CENTER),
                        data=0, on_click=level_selected, height=150,
                        style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True
                    ),
                    ft.OutlinedButton(
                        content=ft.Text("Level 2\n4×3 Grid of Pics. 60 Secs. 10 Moves.",
                                        text_align=ft.TextAlign.CENTER),
                        data=1, on_click=level_selected, height=150,
                        style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True
                    ),
                    ft.OutlinedButton(
                        content=ft.Text("Level 3\n4×4 Grid of Pics. 80 Secs. 12 Moves.",
                                        text_align=ft.TextAlign.CENTER),
                        data=2, on_click=level_selected, height=150,
                        style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True
                    ),
                    ft.OutlinedButton(
                        content=ft.Text("Level 4\n5×4 Grid of Pics. 100 Secs. 15 Moves.",
                                        text_align=ft.TextAlign.CENTER),
                        data=3, on_click=level_selected, height=150,
                        style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True
                    ),
                ], height=150, ref=game_levels),
                ft.Text("Choose game theme", size=24, weight=ft.FontWeight.W_800),
                ft.Row([
                    ft.OutlinedButton("Cats", data=0, on_click=theme_selected, height=150,
                                      style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True),
                    ft.OutlinedButton("Dogs", data=1, on_click=theme_selected, height=150,
                                      style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True),
                    ft.OutlinedButton("Flowers", data=2, on_click=theme_selected, height=150,
                                      style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True),
                ], height=150, ref=game_themes),
                ft.Text("Choose hint to use during game", size=24, weight=ft.FontWeight.W_800),
                ft.Row([
                    ft.OutlinedButton("Revealing Correct Pair", data=0, on_click=hint_selected, height=150,
                                      style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True),
                    ft.OutlinedButton("Showing First 3 Pictures", data=1, on_click=hint_selected, height=150,
                                      style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True),
                    ft.OutlinedButton("Add 30 Seconds & 3 more moves", data=2, on_click=hint_selected, height=150,
                                      style=ft.ButtonStyle(shape=ft.ContinuousRectangleBorder(radius=30)), expand=True),
                ], height=150, ref=game_hints),
                ft.Divider(),
                ft.Row([ft.FilledButton("START GAME", on_click=start_game, expand=True, height=40, autofocus=True)], height=50),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        )
        game_levels.current.controls[0].style.side = ft.BorderSide(2, ft.colors.WHITE)
        game_themes.current.controls[0].style.side = ft.BorderSide(2, ft.colors.WHITE)
        game_hints.current.controls[0].style.side = ft.BorderSide(2, ft.colors.WHITE)
        page.update()

    def check_login_credentials(self):
        if not player_name_field.current.value:
            name_alert.current.opacity = 1
            page.update()
            time.sleep(2)
            name_alert.current.opacity = 0
            page.update()
        elif password_field.current.value != password:
            password_alert.current.opacity = 1
            page.update()
            time.sleep(2)
            password_alert.current.opacity = 0
            page.update()
        else:
            global player_name
            player_name = player_name_field.current.value
            correct_password_alert.current.opacity = 1
            player_name_field.current.disabled = True
            password_field.current.disabled = True
            page.update()
            for i in range(2, -1, -1):
                correct_password_alert.current.value = f"Correct password! Login in {i} seconds."
                page.update()
                time.sleep(1)
            open_game_options(self)

    player_name_field = ft.Ref[ft.TextField]()
    password_field = ft.Ref[ft.TextField]()
    name_alert = ft.Ref[ft.Text]()
    password_alert = ft.Ref[ft.Text]()
    correct_password_alert = ft.Ref[ft.Text]()

    page.add(
        ft.Column([
            ft.Row([
                ft.Text(
                    "Match it!",
                    size=60,
                    weight=ft.FontWeight.W_800,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Text(
                    "Login",
                    size=45,
                    weight=ft.FontWeight.W_600,
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ]),
        ft.Column([
            ft.Row([
                ft.TextField(ref=player_name_field, label="Player Name", on_submit=check_login_credentials,
                             autofocus=True, hint_text="Enter your name"),
                ft.TextField(ref=password_field, label="Password", password=True, can_reveal_password=True,
                             on_submit=check_login_credentials, hint_text="Try to PASS"),
                ft.FilledButton(text="Login", icon=ft.icons.LOGIN, height=50, on_click=check_login_credentials),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Text("Please provide a player name.", ref=name_alert, color=ft.colors.ORANGE, opacity=0,
                    animate_opacity=300),
            ft.Text("Please provide correct password.", ref=password_alert, color=ft.colors.RED, opacity=0,
                    animate_opacity=300),
            ft.Text("", ref=correct_password_alert, color=ft.colors.GREEN, opacity=0, animate_opacity=300),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        ft.Row([
            ft.Text("Made with ❤ by Mosaab, Ohoud, Zeinab, and Logain.")
        ], alignment=ft.MainAxisAlignment.CENTER)
    )


ft.app(target=main, assets_dir="assets")
