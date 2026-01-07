import os

class FileManager:
    """
    FileManager — модуль для роботи з файловою системою Spark‑1.
    Дає можливість створювати папки, файли, читати та записувати дані.
    Працює з повним доступом до диску E:\\.
    """

    def __init__(self, base_root="E:\\"):
        self.base_root = os.path.abspath(base_root)

    # ---------------------------------------------------------
    #  Перевірка, що шлях знаходиться на диску E:
    # ---------------------------------------------------------
    def _resolve_path(self, path: str) -> str:
        full_path = os.path.abspath(os.path.join(self.base_root, path))

        # Гарантуємо, що шлях починається з E:\
        if not full_path.lower().startswith(self.base_root.lower()):
            raise PermissionError(f"❌ Заборонено виходити за межі {self.base_root}")

        return full_path

    # ---------------------------------------------------------
    #  Створення папки
    # ---------------------------------------------------------
    def create_dir(self, path: str) -> str:
        full_path = self._resolve_path(path)
        os.makedirs(full_path, exist_ok=True)
        return f"📁 Папку створено: {full_path}"

    # ---------------------------------------------------------
    #  Створення або перезапис файлу
    # ---------------------------------------------------------
    def write_file(self, path: str, content: str) -> str:
        full_path = self._resolve_path(path)
        directory = os.path.dirname(full_path)
        os.makedirs(directory, exist_ok=True)

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(content)

        return f"📝 Файл створено/перезаписано: {full_path}"

    # ---------------------------------------------------------
    #  Дозапис у файл
    # ---------------------------------------------------------
    def append_file(self, path: str, content: str) -> str:
        full_path = self._resolve_path(path)
        directory = os.path.dirname(full_path)
        os.makedirs(directory, exist_ok=True)

        with open(full_path, "a", encoding="utf-8") as f:
            f.write(content)

        return f"➕ Додано в файл: {full_path}"

    # ---------------------------------------------------------
    #  Читання файлу
    # ---------------------------------------------------------
    def read_file(self, path: str) -> str:
        full_path = self._resolve_path(path)

        if not os.path.exists(full_path):
            return f"❌ Файл не знайдено: {full_path}"

        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
