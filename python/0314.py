import tkinter as tk
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import time

class RussianRouletteGame:
    def __init__(self, master):
        self.master = master
        master.title("러시안 룰렛 게임")

        self.label = tk.Label(master, text="러시안 룰렛 게임에 오신 것을 환영합니다!")
        self.label.pack()

        self.canvas = tk.Canvas(master, width=200, height=200)
        self.canvas.pack()

        self.start_button = tk.Button(master, text="게임 시작", command=self.start_game)
        self.start_button.pack()

        self.quit_button = tk.Button(master, text="나가기", command=master.quit)
        self.quit_button.pack()

    def start_game(self):
        self.label.config(text="게임을 시작합니다...")
        self.start_button.config(state=tk.DISABLED)
        self.quit_button.config(state=tk.DISABLED)

        self.bullet_chamber = random.randint(1, 6)
        self.chamber_position = 1

        self.play_game()

    def play_game(self):
        self.animate_gun()
        self.master.after(1000, self.check_bullet)

    def animate_gun(self, angle=0):
        gun_image = Image.open("gun.png")
        gun_image = gun_image.rotate(angle)
        self.gun_photo = ImageTk.PhotoImage(gun_image)
        self.canvas.create_image(100, 100, image=self.gun_photo)
        self.master.update()
        if angle < 360:
            self.master.after(50, self.animate_gun, angle + 10)

    def check_bullet(self):
        if self.chamber_position == self.bullet_chamber:
            self.label.config(text="쾅! 총알이 발사되었습니다! 당신은 죽었습니다!")
            messagebox.showinfo("게임 종료", "쾅! 총알이 발사되었습니다! 당신은 죽었습니다!")
            self.start_button.config(state=tk.NORMAL)
            self.quit_button.config(state=tk.NORMAL)
        else:
            self.label.config(text="휴... 총알이 발사되지 않았습니다.")
            self.label.after(1000, self.continue_game)

    def continue_game(self):
        self.chamber_position = (self.chamber_position % 6) + 1
        self.label.config(text="계속해서 방아쇠를 돌리시겠습니까?")

        self.yes_button = tk.Button(self.master, text="네", command=self.start_game)
        self.yes_button.pack()

        self.no_button = tk.Button(self.master, text="아니오", command=self.master.quit)
        self.no_button.pack()

root = tk.Tk()
game = RussianRouletteGame(root)
root.mainloop()
