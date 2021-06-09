from pathlib import Path

root_path = Path(__file__).parent


def generate_config():
    config_path = root_path / "bot/config.py"
    config_example_path = root_path / "bot/config_example.py"

    if not config_example_path.exists():
        print("Не удалось найти файл шаблона конфига.")
        exit(0)

    if not config_path.exists():
        example_text = config_example_path.read_text("utf-8")
        config_path.touch()
        config_path.write_text(example_text, "utf-8")

    print(f"Конфиг успешно создан. Заполните его -> {config_path.resolve()}")


def generate_start():
    start_bat_path = root_path / "start.bat"
    start_script = f"""cd \"{root_path.absolute()}\"
    pip install wheel -r requirements.txt
    python -m bot
    """

    start_bat_path.touch()
    start_bat_path.write_text("\n".join(map(str.strip, start_script.splitlines())))
    print(f"Скрипт старта успешно создан -> {start_bat_path.resolve()}")


generate_config()
generate_start()
