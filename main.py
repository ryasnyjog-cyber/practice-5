import tkinter as tk
from tkinter import ttk, messagebox
import random


# =========================
# НАЛАШТУВАННЯ ГРИ
# =========================

DETAILS_DAMAGE_PRICE = {
    "Energy Gun": 100,
    "Minigun": 70,
    "Thor Hammer": 50,
    "Laser Gun": 80,
    "Rail Gun": 90,
    "Sniper Rifle": 150
}

DETAILS_SURVIVE_PRICE = {
    "Shield": 50,
    "Energy Shield": 80,
    "Resist": 30,
    "Evasion": 100,
    "Armor": 140
}

# Скільки атаки дає кожна зброя
DAMAGE_VALUE = {
    "Energy Gun": 25,
    "Minigun": 18,
    "Thor Hammer": 15,
    "Laser Gun": 22,
    "Rail Gun": 30,
    "Sniper Rifle": 40
}

# Скільки захисту дає кожна деталь
DEFENSE_VALUE = {
    "Shield": 20,
    "Energy Shield": 30,
    "Resist": 12,
    "Evasion": 25,
    "Armor": 40
}

MIN_START_SUM = min(DETAILS_DAMAGE_PRICE.values())

MAX_START_SUM = (
    sum(DETAILS_DAMAGE_PRICE.values())
    + sum(DETAILS_SURVIVE_PRICE.values())
)


# =========================
# ГОЛОВНИЙ КЛАС
# =========================

class RobotArena:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Robot Arena")
        self.root.geometry("1050x700")
        self.root.resizable(False, False)

        self.players = []
        self.current_player_index = 0

        self.create_styles()
        self.create_interface()

    # =========================
    # СТИЛІ
    # =========================

    def create_styles(self):
        style = ttk.Style()

        try:
            style.theme_use("clam")
        except:
            pass

        style.configure(
            "Title.TLabel",
            font=("Arial", 24, "bold")
        )

        style.configure(
            "Subtitle.TLabel",
            font=("Arial", 12)
        )

        style.configure(
            "Game.TButton",
            font=("Arial", 11, "bold"),
            padding=8
        )

        style.configure(
            "Shop.TButton",
            font=("Arial", 10, "bold"),
            padding=6
        )

    # =========================
    # ІНТЕРФЕЙС
    # =========================

    def create_interface(self):
        header = ttk.Frame(self.root)
        header.pack(fill="x", padx=20, pady=15)

        ttk.Label(
            header,
            text="🤖 ROBOT ARENA",
            style="Title.TLabel"
        ).pack()

        ttk.Label(
            header,
            text="Створи свого бойового робота та відправ його на арену!",
            style="Subtitle.TLabel"
        ).pack(pady=5)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=10)

        self.create_setup_tab()
        self.create_shop_tab()
        self.create_battle_tab()

    # =========================
    # ВКЛАДКА СТВОРЕННЯ
    # =========================

    def create_setup_tab(self):
        self.setup_frame = ttk.Frame(self.notebook)
        self.notebook.add(
            self.setup_frame,
            text="👥 Гравці"
        )

        # Ліва частина
        left_frame = ttk.LabelFrame(
            self.setup_frame,
            text="Створення гравця",
            padding=20
        )
        left_frame.place(
            x=20,
            y=20,
            width=450,
            height=260
        )

        ttk.Label(
            left_frame,
            text="Ім'я гравця:"
        ).pack(anchor="w")

        self.player_name_entry = ttk.Entry(
            left_frame,
            font=("Arial", 12)
        )
        self.player_name_entry.pack(
            fill="x",
            pady=8
        )

        ttk.Label(
            left_frame,
            text="Стартовий капітал:"
        ).pack(anchor="w")

        self.start_money_entry = ttk.Entry(
            left_frame,
            font=("Arial", 12)
        )
        self.start_money_entry.insert(
            0,
            "300"
        )
        self.start_money_entry.pack(
            fill="x",
            pady=8
        )

        ttk.Label(
            left_frame,
            text=f"Допустимо: {MIN_START_SUM} – {MAX_START_SUM} монет"
        ).pack(
            anchor="w",
            pady=5
        )

        ttk.Button(
            left_frame,
            text="➕ Додати гравця",
            style="Game.TButton",
            command=self.add_player
        ).pack(
            fill="x",
            pady=15
        )

        # Права частина
        right_frame = ttk.LabelFrame(
            self.setup_frame,
            text="Список гравців",
            padding=15
        )
        right_frame.place(
            x=500,
            y=20,
            width=500,
            height=430
        )

        self.players_listbox = tk.Listbox(
            right_frame,
            font=("Arial", 12),
            height=15
        )
        self.players_listbox.pack(
            fill="both",
            expand=True
        )

        ttk.Button(
            self.setup_frame,
            text="🗑 Видалити вибраного",
            command=self.remove_player
        ).place(
            x=500,
            y=470,
            width=240
        )

        ttk.Button(
            self.setup_frame,
            text="➡ Перейти до магазину",
            style="Game.TButton",
            command=self.open_shop
        ).place(
            x=760,
            y=470,
            width=240
        )

        self.setup_status = ttk.Label(
            self.setup_frame,
            text="Створіть мінімум 2 гравців.",
            font=("Arial", 11)
        )
        self.setup_status.place(
            x=20,
            y=470
        )

    # =========================
    # ВКЛАДКА МАГАЗИНУ
    # =========================

    def create_shop_tab(self):
        self.shop_frame = ttk.Frame(self.notebook)
        self.notebook.add(
            self.shop_frame,
            text="🛒 Магазин"
        )

        # Заголовок
        self.shop_player_label = ttk.Label(
            self.shop_frame,
            text="Гравець не вибраний",
            font=("Arial", 18, "bold")
        )
        self.shop_player_label.pack(pady=10)

        self.money_label = ttk.Label(
            self.shop_frame,
            text="💰 0 монет",
            font=("Arial", 14)
        )
        self.money_label.pack()

        self.stats_label = ttk.Label(
            self.shop_frame,
            text="⚔ Атака: 0 | 🛡 Захист: 0",
            font=("Arial", 12)
        )
        self.stats_label.pack(pady=5)

        # Кнопка наступного гравця
        ttk.Button(
            self.shop_frame,
            text="➡ Наступний гравець",
            command=self.next_player
        ).pack(pady=10)

        # Основна область
        shop_container = ttk.Frame(self.shop_frame)
        shop_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        damage_frame = ttk.LabelFrame(
            shop_container,
            text="⚔ ЗБРОЯ",
            padding=10
        )
        damage_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        survive_frame = ttk.LabelFrame(
            shop_container,
            text="🛡 ЗАХИСТ",
            padding=10
        )
        survive_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        self.damage_buttons = {}
        self.survive_buttons = {}

        for name, price in DETAILS_DAMAGE_PRICE.items():
            button = ttk.Button(
                damage_frame,
                text=f"{name}\n💰 {price}",
                style="Shop.TButton",
                command=lambda n=name: self.buy_detail(n)
            )
            button.pack(
                fill="x",
                pady=4
            )
            self.damage_buttons[name] = button

        for name, price in DETAILS_SURVIVE_PRICE.items():
            button = ttk.Button(
                survive_frame,
                text=f"{name}\n💰 {price}",
                style="Shop.TButton",
                command=lambda n=name: self.buy_detail(n)
            )
            button.pack(
                fill="x",
                pady=4
            )
            self.survive_buttons[name] = button

        # Вибрані деталі
        details_frame = ttk.LabelFrame(
            self.shop_frame,
            text="🔧 Деталі робота",
            padding=10
        )
        details_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )

        self.details_listbox = tk.Listbox(
            details_frame,
            height=5,
            font=("Arial", 11)
        )
        self.details_listbox.pack(
            fill="x"
        )

        ttk.Button(
            self.shop_frame,
            text="💰 Продати вибрану деталь",
            command=self.sell_detail
        ).pack(
            pady=5
        )

        ttk.Button(
            self.shop_frame,
            text="🏟 Перейти на арену",
            style="Game.TButton",
            command=self.open_battle
        ).pack(
            pady=10
        )

    # =========================
    # ВКЛАДКА БОЮ
    # =========================

    def create_battle_tab(self):
        self.battle_frame = ttk.Frame(self.notebook)
        self.notebook.add(
            self.battle_frame,
            text="🏟 Арена"
        )

        ttk.Label(
            self.battle_frame,
            text="🏟 ROBOT ARENA",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        # Інформація про роботів
        robots_frame = ttk.Frame(
            self.battle_frame
        )
        robots_frame.pack(
            fill="x",
            padx=30
        )

        self.robot1_label = ttk.Label(
            robots_frame,
            text="🤖 Robot 1",
            font=("Arial", 14)
        )
        self.robot1_label.grid(
            row=0,
            column=0,
            padx=30
        )

        self.robot2_label = ttk.Label(
            robots_frame,
            text="🤖 Robot 2",
            font=("Arial", 14)
        )
        self.robot2_label.grid(
            row=0,
            column=1,
            padx=30
        )

        # Здоров'я
        self.health1 = ttk.Progressbar(
            robots_frame,
            length=350,
            maximum=100
        )
        self.health1.grid(
            row=1,
            column=0,
            padx=30,
            pady=15
        )
        self.health1["value"] = 100

        self.health2 = ttk.Progressbar(
            robots_frame,
            length=350,
            maximum=100
        )
        self.health2.grid(
            row=1,
            column=1,
            padx=30,
            pady=15
        )
        self.health2["value"] = 100

        # Лог
        ttk.Label(
            self.battle_frame,
            text="📜 Журнал бою",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        self.battle_log = tk.Text(
            self.battle_frame,
            width=100,
            height=18,
            font=("Consolas", 10)
        )
        self.battle_log.pack(
            padx=30,
            pady=5
        )

        ttk.Button(
            self.battle_frame,
            text="⚔ ПОЧАТИ БІЙ",
            style="Game.TButton",
            command=self.start_battle
        ).pack(
            pady=10
        )

    # =========================
    # ДОДАВАННЯ ГРАВЦЯ
    # =========================

    def add_player(self):
        name = self.player_name_entry.get().strip()

        if len(name) < 3:
            messagebox.showwarning(
                "Помилка",
                "Ім'я повинно містити мінімум 3 символи."
            )
            return

        # Перевірка на дублікати
        for player in self.players:
            if player["name"].lower() == name.lower():
                messagebox.showwarning(
                    "Помилка",
                    "Гравець з таким ім'ям вже існує."
                )
                return

        try:
            money = int(
                self.start_money_entry.get()
            )
        except ValueError:
            messagebox.showerror(
                "Помилка",
                "Введіть число для стартового капіталу."
            )
            return

        money = max(
            MIN_START_SUM,
            min(money, MAX_START_SUM)
        )

        player = {
            "name": name.capitalize(),
            "money": money,
            "details": []
        }

        self.players.append(player)

        self.players_listbox.insert(
            "end",
            f"🤖 {player['name']} | 💰 {money}"
        )

        self.player_name_entry.delete(
            0,
            "end"
        )

        self.setup_status.config(
            text=f"Гравців створено: {len(self.players)}"
        )

    # =========================
    # ВИДАЛЕННЯ ГРАВЦЯ
    # =========================

    def remove_player(self):
        selected = self.players_listbox.curselection()

        if not selected:
            messagebox.showwarning(
                "Увага",
                "Виберіть гравця."
            )
            return

        index = selected[0]

        self.players.pop(index)

        self.players_listbox.delete(
            index
        )

        if self.players:
            self.current_player_index = 0
            self.update_shop()
        else:
            self.current_player_index = 0
            self.clear_shop()

        self.setup_status.config(
            text=f"Гравців створено: {len(self.players)}"
        )

    # =========================
    # ОНОВЛЕННЯ МАГАЗИНУ
    # =========================

    def update_shop(self):
        if not self.players:
            self.clear_shop()
            return

        player = self.players[
            self.current_player_index
        ]

        self.shop_player_label.config(
            text=f"🤖 {player['name']}"
        )

        self.money_label.config(
            text=f"💰 {player['money']} монет"
        )

        attack = self.get_attack(player)
        defense = self.get_defense(player)

        self.stats_label.config(
            text=f"⚔ Атака: {attack}   |   🛡 Захист: {defense}"
        )

        self.details_listbox.delete(
            0,
            "end"
        )

        for detail in player["details"]:
            if detail in DAMAGE_VALUE:
                icon = "⚔"
            else:
                icon = "🛡"

            self.details_listbox.insert(
                "end",
                f"{icon} {detail}"
            )

        # Оновлення кнопок магазину
        for name, button in self.damage_buttons.items():
            if name in player["details"]:
                button.config(
                    text=f"{name}\n✅ ВЖЕ Є"
                )
            else:
                button.config(
                    text=f"{name}\n💰 {DETAILS_DAMAGE_PRICE[name]}"
                )

        for name, button in self.survive_buttons.items():
            if name in player["details"]:
                button.config(
                    text=f"{name}\n✅ ВЖЕ Є"
                )
            else:
                button.config(
                    text=f"{name}\n💰 {DETAILS_SURVIVE_PRICE[name]}"
                )

    def clear_shop(self):
        self.shop_player_label.config(
            text="Гравець не вибраний"
        )

        self.money_label.config(
            text="💰 0 монет"
        )

        self.stats_label.config(
            text="⚔ Атака: 0 | 🛡 Захист: 0"
        )

        self.details_listbox.delete(
            0,
            "end"
        )

    # =========================
    # КУПІВЛЯ
    # =========================

    def buy_detail(self, detail):
        if not self.players:
            return

        player = self.players[
            self.current_player_index
        ]

        if detail in player["details"]:
            messagebox.showinfo(
                "Увага",
                "Ця деталь вже встановлена."
            )
            return

        if detail in DETAILS_DAMAGE_PRICE:
            price = DETAILS_DAMAGE_PRICE[detail]
        else:
            price = DETAILS_SURVIVE_PRICE[detail]

        if player["money"] < price:
            messagebox.showwarning(
                "Недостатньо монет",
                f"Потрібно {price} монет."
            )
            return

        player["money"] -= price
        player["details"].append(detail)

        self.update_shop()

        self.battle_log.insert(
            "end",
            f"🔧 {player['name']} купив {detail}\n"
        )

    # =========================
    # ПРОДАЖ
    # =========================

    def sell_detail(self):
        selected = self.details_listbox.curselection()

        if not selected:
            messagebox.showwarning(
                "Увага",
                "Виберіть деталь для продажу."
            )
            return

        player = self.players[
            self.current_player_index
        ]

        index = selected[0]
        detail = player["details"][index]

        if detail in DETAILS_DAMAGE_PRICE:
            price = DETAILS_DAMAGE_PRICE[detail]
        else:
            price = DETAILS_SURVIVE_PRICE[detail]

        # Повертаємо 80% вартості
        refund = int(price * 0.8)

        player["money"] += refund
        player["details"].remove(detail)

        self.update_shop()

    # =========================
    # НАСТУПНИЙ ГРАВЕЦЬ
    # =========================

    def next_player(self):
        if not self.players:
            return

        if self.current_player_index < len(self.players) - 1:
            self.current_player_index += 1
        else:
            self.current_player_index = 0

        self.update_shop()

    # =========================
    # СТАТИСТИКА
    # =========================

    def get_attack(self, player):
        attack = 10

        for detail in player["details"]:
            if detail in DAMAGE_VALUE:
                attack += DAMAGE_VALUE[detail]

        return attack

    def get_defense(self, player):
        defense = 0

        for detail in player["details"]:
            if detail in DEFENSE_VALUE:
                defense += DEFENSE_VALUE[detail]

        return defense

    # =========================
    # ПЕРЕХІД ДО МАГАЗИНУ
    # =========================

    def open_shop(self):
        if not self.players:
            messagebox.showwarning(
                "Увага",
                "Спочатку створіть хоча б одного гравця."
            )
            return

        self.notebook.select(
            self.shop_frame
        )
        self.update_shop()

    # =========================
    # ПЕРЕХІД НА АРЕНУ
    # =========================

    def open_battle(self):
        if len(self.players) < 2:
            messagebox.showwarning(
                "Недостатньо гравців",
                "Для бою потрібно мінімум 2 гравці."
            )
            return

        self.notebook.select(
            self.battle_frame
        )

        self.prepare_battle()

    # =========================
    # ПІДГОТОВКА БОЮ
    # =========================

    def prepare_battle(self):
        player1, player2 = random.sample(
            self.players,
            2
        )

        self.fighter1 = player1
        self.fighter2 = player2

        self.hp1 = 100
        self.hp2 = 100

        attack1 = self.get_attack(player1)
        attack2 = self.get_attack(player2)

        defense1 = self.get_defense(player1)
        defense2 = self.get_defense(player2)

        self.robot1_label.config(
            text=(
                f"🤖 {player1['name']}\n"
                f"⚔ {attack1} | 🛡 {defense1}"
            )
        )

        self.robot2_label.config(
            text=(
                f"🤖 {player2['name']}\n"
                f"⚔ {attack2} | 🛡 {defense2}"
            )
        )

        self.health1["value"] = 100
        self.health2["value"] = 100

        self.battle_log.delete(
            "1.0",
            "end"
        )

        self.battle_log.insert(
            "end",
            "🏟 БІЙ ПОЧИНАЄТЬСЯ!\n\n"
        )

        self.battle_log.insert(
            "end",
            f"🤖 {player1['name']} VS {player2['name']}\n\n"
        )

    # =========================
    # ПОЧАТОК БОЮ
    # =========================

    def start_battle(self):
        if not hasattr(self, "fighter1"):
            if len(self.players) < 2:
                messagebox.showwarning(
                    "Увага",
                    "Потрібно мінімум 2 гравці."
                )
                return

            self.prepare_battle()

        self.battle_log.insert(
            "end",
            "⚡ Раунд починається...\n"
        )

        self.run_round()

    # =========================
    # РАУНД
    # =========================

    def run_round(self):
        if self.hp1 <= 0 or self.hp2 <= 0:
            return

        # Атака першого робота
        damage1 = self.calculate_damage(
            self.fighter1,
            self.fighter2
        )

        self.hp2 -= damage1
        self.hp2 = max(
            0,
            self.hp2
        )

        self.health2["value"] = self.hp2

        self.battle_log.insert(
            "end",
            f"⚔ {self.fighter1['name']} завдав "
            f"{damage1} шкоди!\n"
        )

        if self.hp2 <= 0:
            self.finish_battle(
                self.fighter1
            )
            return

        # Другий робот атакує
        damage2 = self.calculate_damage(
            self.fighter2,
            self.fighter1
        )

        self.hp1 -= damage2
        self.hp1 = max(
            0,
            self.hp1
        )

        self.health1["value"] = self.hp1

        self.battle_log.insert(
            "end",
            f"💥 {self.fighter2['name']} завдав "
            f"{damage2} шкоди!\n"
        )

        if self.hp1 <= 0:
            self.finish_battle(
                self.fighter2
            )
            return

        self.battle_log.insert(
            "end",
            f"❤️ {self.fighter1['name']}: {self.hp1} HP | "
            f"{self.fighter2['name']}: {self.hp2} HP\n\n"
        )

        # Наступний раунд
        self.root.after(
            700,
            self.run_round
        )

    # =========================
    # РОЗРАХУНОК ШКОДИ
    # =========================

    def calculate_damage(self, attacker, defender):
        attack = self.get_attack(attacker)
        defense = self.get_defense(defender)

        # Випадковий бонус
        random_bonus = random.randint(
            -5,
            10
        )

        # Основна формула
        damage = attack + random_bonus - defense // 5

        # Evasion дає шанс повністю уникнути удару
        if "Evasion" in defender["details"]:
            if random.random() < 0.20:
                self.battle_log.insert(
                    "end",
                    f"💨 {defender['name']} ухилився!\n"
                )
                return 0

        # Shield дає шанс зменшити шкоду
        if "Shield" in defender["details"]:
            if random.random() < 0.25:
                damage = damage // 2
                self.battle_log.insert(
                    "end",
                    f"🛡 Щит {defender['name']} "
                    f"зменшив шкоду!\n"
                )

        return max(
            5,
            damage
        )

    # =========================
    # КІНЕЦЬ БОЮ
    # =========================

    def finish_battle(self, winner):
        self.battle_log.insert(
            "end",
            "\n"
            + "=" * 60
            + "\n"
        )

        self.battle_log.insert(
            "end",
            f"🏆 ПЕРЕМОЖЕЦЬ: {winner['name']}!\n"
        )

        self.battle_log.insert(
            "end",
            "🎉 Вітаємо! Робот переміг на арені.\n"
        )

        messagebox.showinfo(
            "🏆 Бій завершено",
            f"Переможець: {winner['name']}!"
        )

        # Після бою можна створити нову пару
        self.fighter1 = None
        self.fighter2 = None


# =========================
# ЗАПУСК
# =========================

if __name__ == "__main__":
    root = tk.Tk()

    game = RobotArena(root)

    root.mainloop()
