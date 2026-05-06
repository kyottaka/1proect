import tkinter as tk
from tkinter import messagebox
import random

# Настройки
N, M = 6, 6
HP = [100, 100]
MAX_HP = 100
DMG = [10, 20]
POS = [[0, 0], [N - 1, M - 1]]
HEALS = []
NAMES = ["A", "B"]
TURN = 0


def spawn_heal():
    """Создает аптечки в пустых местах"""
    while len(HEALS) < 3:
        r, c = random.randint(0, N - 1), random.randint(0, M - 1)
        # Аптечка не может появиться там, где игрок или другая аптечка
        if [r, c] not in POS and [r, c] not in HEALS:
            HEALS.append([r, c])


def get_zones(p_idx):
    r, c = POS[p_idx]
    # Ход: 8 направлений
    moves = [(r + i, c + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if not (i == 0 and j == 0)]
    # Атака: А - 8 напр., B - 4 напр.
    if p_idx == 0:
        attacks = moves[:]
    else:
        attacks = [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
    return moves, attacks


def update_ui():
    foe = 1 - TURN
    moves, attacks = get_zones(TURN)

    for r in range(N):
        for c in range(M):
            btn = buttons[r][c]
            btn.config(text="", bg="white", state="disabled")

            # 1. Аптечки (показываем всегда, активируем только в зоне хода)
            if [r, c] in HEALS:
                if (r, c) in moves:
                    btn.config(bg="#2ecc71", text="+20", state="normal")
                else:
                    btn.config(bg="#27ae60", text="+20", state="disabled")

            # 2. Игроки (рисуем поверх всего)
            for i in range(2):
                if POS[i] == [r, c]:
                    color = "#3498db" if i == 0 else "#e74c3c"
                    btn.config(text=f"{NAMES[i]}\n{HP[i]}", bg=color, state="disabled")

            # 3. Зона атаки (ЖЕЛТЫЙ), если там враг
            if [r, c] == POS[foe] and (r, c) in attacks:
                btn.config(bg="#f1c40f", state="normal")

                # 4. Зона хода (СЕРЫЙ), только если клетка ПУСТАЯ (нет врага и нет аптечки)
            elif (r, c) in moves and 0 <= r < N and 0 <= c < M:
                if [r, c] != POS[foe] and [r, c] not in HEALS:
                    btn.config(bg="#ecf0f1", state="normal")

    status.set(f"ХОДИТ: {NAMES[TURN]} | HP A:{HP[0]} B:{HP[1]}")


def click(r, c):
    global TURN
    foe = 1 - TURN

    # КРИТИЧЕСКАЯ ПРОВЕРКА: Если кликнули по врагу
    if [r, c] == POS[foe]:
        # Только наносим урон, координаты НЕ МЕНЯЕМ
        HP[foe] -= DMG[TURN]
        if HP[foe] <= 0:
            messagebox.showinfo("Gg Wp", f"Игрок {NAMES[TURN]} разнёс кабину оппоненту!")
            root.destroy()
            return
    else:
        # Если кликнули по пустой клетке или аптечке — перемещаемся
        POS[TURN] = [r, c]
        if [r, c] in HEALS:
            HP[TURN] = min(MAX_HP, HP[TURN] + 20)
            HEALS.remove([r, c])
            if random.random() < 0.3: spawn_heal()

    TURN = foe
    update_ui()


# Интерфейс
root = tk.Tk()
root.title("Anti-Lego Arena")
spawn_heal()

status = tk.StringVar()
tk.Label(root, textvariable=status, font=("Arial", 12, "bold")).pack(pady=5)

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

buttons = []
for r in range(N):
    row = []
    for c in range(M):
        b = tk.Button(frame, width=8, height=4, command=lambda r=r, c=c: click(r, c))
        b.grid(row=r, column=c)
        row.append(b)
    buttons.append(row)

update_ui()
root.mainloop()