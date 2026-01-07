import threading
import time
import customtkinter as ctk
from tkinter import END
from math import sin
from datetime import datetime

# Імпорт функцій з main.py
from main import (
    load_config, load_paths, attach_external_repos,
    import_agents, activate_agents, run_cloud_cycle
)

# -----------------------------
#  КЛАС UI
# -----------------------------

class SparkUI(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Spark‑1 Control Panel")
        self.geometry("1100x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Агентні змінні
        self.agent1 = None
        self.agent2 = None

        # Стан системи
        self.running = False        # Чи працює система
        self.paused = False         # Пауза (на майбутнє)
        self.protocol_mode = ctk.StringVar(value="short_cycle")  # Протокол циклу

        # Пульсація
        self.pulse_phase_1 = 0
        self.pulse_phase_2 = 0
        self.pulse_speed_1 = 0.05
        self.pulse_speed_2 = 0.05

        # -----------------------------
        #  ЛЕЙАУТ
        # -----------------------------

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Ліве коло (AgentAI1)
        self.canvas1 = ctk.CTkCanvas(self, width=300, height=300, bg="#1a1a1a", highlightthickness=0)
        self.canvas1.grid(row=0, column=0, padx=20, pady=20)

        # Праве коло (AgentAI2)
        self.canvas2 = ctk.CTkCanvas(self, width=300, height=300, bg="#1a1a1a", highlightthickness=0)
        self.canvas2.grid(row=0, column=1, padx=20, pady=20)

        # Статуси агентів
        self.status1 = ctk.CTkLabel(self, text="AgentAI1: Idle", font=("Arial", 16))
        self.status1.grid(row=1, column=0, pady=(0, 10))

        self.status2 = ctk.CTkLabel(self, text="AgentAI2: Idle", font=("Arial", 16))
        self.status2.grid(row=1, column=1, pady=(0, 10))

        # Лог
        self.log_box = ctk.CTkTextbox(self, width=1050, height=200)
        self.log_box.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

        # Кнопки керування
        self.btn_start = ctk.CTkButton(self, text="Start Spark‑1", command=self.start_system)
        self.btn_start.grid(row=3, column=0, pady=10)

        self.btn_stop = ctk.CTkButton(self, text="Stop", command=self.stop_system)
        self.btn_stop.grid(row=3, column=1, pady=10)

        # Вибір протоколу циклу
        self.protocol_selector = ctk.CTkOptionMenu(
            self,
            values=["short_cycle", "medium_cycle", "long_cycle"],
            variable=self.protocol_mode,
            width=200
        )
        self.protocol_selector.grid(row=4, column=0, columnspan=2, pady=10)
        self.protocol_selector.set("short_cycle")

        # Запуск анімації пульсації
        self.animate()

    # -----------------------------
    #  ЛОГ
    # -----------------------------

    def log(self, text):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(END, f"[{timestamp}] {text}\n")
        self.log_box.see(END)

    # -----------------------------
    #  ПУЛЬСУЮЧІ КОЛА
    # -----------------------------

    def animate(self):
        self.canvas1.delete("all")
        self.canvas2.delete("all")

        # Радіуси
        r1 = 100 + sin(self.pulse_phase_1) * 10
        r2 = 100 + sin(self.pulse_phase_2) * 10

        # Оновлення фази
        self.pulse_phase_1 += self.pulse_speed_1
        self.pulse_phase_2 += self.pulse_speed_2

        # Малюємо кола
        self.canvas1.create_oval(150 - r1, 150 - r1, 150 + r1, 150 + r1, outline="#4da6ff", width=4)
        self.canvas2.create_oval(150 - r2, 150 - r2, 150 + r2, 150 + r2, outline="#b366ff", width=4)

        # Текст всередині
        self.canvas1.create_text(150, 150, text="AI‑1", fill="white", font=("Arial", 22))
        self.canvas2.create_text(150, 150, text="AI‑2", fill="white", font=("Arial", 22))

        self.after(30, self.animate)

    # -----------------------------
    #  ЗАПУСК СИСТЕМИ
    # -----------------------------

    def start_system(self):
        if self.running:
            self.log("⚠ Spark‑1 вже працює.")
            return

        self.running = True
        self.log(f"🚀 Запуск Spark‑1 (protocol: {self.protocol_mode.get()})...")

        # Ініціалізація середовища
        config = load_config()
        paths = load_paths()
        attach_external_repos(paths)

        # Агенти
        AgentAI1, AgentAI2 = import_agents()
        self.agent1, self.agent2 = activate_agents(AgentAI1, AgentAI2)

        # Запуск фонової роботи відповідно до протоколу
        threading.Thread(target=self.run_loop, daemon=True).start()

    # -----------------------------
    #  ОДИН ЦИКЛ (будівельний блок)
    # -----------------------------

    def run_single_cycle(self):
        # Активна фаза
        self.status1.configure(text="AgentAI1: Analyzing...")
        self.status2.configure(text="AgentAI2: Thinking...")
        self.pulse_speed_1 = 0.15
        self.pulse_speed_2 = 0.12

        signals, strategy, results = run_cloud_cycle(self.agent1, self.agent2)

        # Завершення циклу
        self.log("✔ Цикл завершено.")
        self.status1.configure(text="AgentAI1: Idle")
        self.status2.configure(text="AgentAI2: Idle")
        self.pulse_speed_1 = 0.05
        self.pulse_speed_2 = 0.05

        return signals, strategy, results

    # -----------------------------
    #  CHECKPOINT ДЛЯ ДОВГИХ ЦИКЛІВ
    # -----------------------------

    def save_checkpoint(self):
        # Поки що просто лог; далі можна інтегрувати MemoryEngine напряму
        self.log("💾 Checkpoint збережено (long_cycle).")

    # -----------------------------
    #  ГОЛОВНИЙ ФОНОВИЙ ЦИКЛ
    # -----------------------------

    def run_loop(self):
        protocol = self.protocol_mode.get()

        # 1) Короткий цикл — один раз і стоп
        if protocol == "short_cycle":
            self.log("🌀 Протокол: short_cycle (1 цикл).")
            try:
                self.run_single_cycle()
            finally:
                self.running = False
                self.log("✅ short_cycle завершено.")
            return

        # 2) Середній цикл — обмежена кількість повторів з інтервалом
        elif protocol == "medium_cycle":
            self.log("🌀 Протокол: medium_cycle (серія циклів).")
            max_cycles = 36          # умовно: до ~3 годин, якщо інтервал великий
            interval_sec = 300       # 5 хвилин між циклами

            for i in range(max_cycles):
                if not self.running:
                    break

                self.log(f"🔁 medium_cycle — цикл {i+1}/{max_cycles}...")
                self.run_single_cycle()

                # Якщо це останній цикл — не чекаємо
                if i < max_cycles - 1 and self.running:
                    self.log(f"⏳ Очікування {interval_sec} сек до наступного циклу...")
                    for _ in range(interval_sec):
                        if not self.running:
                            break
                        time.sleep(1)

            self.running = False
            self.log("✅ medium_cycle завершено.")
            return

        # 3) Довгий цикл — працює, поки не натиснуто Stop
        elif protocol == "long_cycle":
            self.log("🌀 Протокол: long_cycle (тривалий режим).")
            interval_sec = 600       # 10 хвилин між циклами

            cycle_index = 0
            while self.running:
                cycle_index += 1
                self.log(f"🔁 long_cycle — цикл {cycle_index}...")
                self.run_single_cycle()
                self.save_checkpoint()

                # Інтервал між циклами з можливістю зупинки
                self.log(f"⏳ Очікування {interval_sec} сек до наступного циклу...")
                for _ in range(interval_sec):
                    if not self.running:
                        break
                    time.sleep(1)

            self.log("✅ long_cycle зупинено вручну.")
            return

        # На всякий випадок
        else:
            self.log(f"⚠ Невідомий протокол: {protocol}. Зупинка.")
            self.running = False

    # -----------------------------
    #  ЗУПИНКА
    # -----------------------------

    def stop_system(self):
        if not self.running:
            self.log("⚠ Spark‑1 вже зупинено.")
            return

        self.running = False
        self.log("🛑 Команда зупинки: Spark‑1 зупиняється...")
        self.status1.configure(text="AgentAI1: Stopped")
        self.status2.configure(text="AgentAI2: Stopped")
        self.pulse_speed_1 = 0.01
        self.pulse_speed_2 = 0.01


# -----------------------------
#  ЗАПУСК UI
# -----------------------------

if __name__ == "__main__":
    app = SparkUI()
    app.mainloop()
