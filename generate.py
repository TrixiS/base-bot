import os
import platform

from pathlib import Path

from bot import root_path


def create_config() -> Path:
    config_path = root_path / "bot/config.py"
    config_template_path = root_path / "bot/config_template.py"

    if not config_template_path.exists():
        raise Exception(
            f"Не удалось найти файл шаблона конфига -> {config_template_path.absolute()}"
        )

    if config_path.exists():
        raise Exception(f"Конфиг уже создан -> {config_path.absolute()}")

    example_text = config_template_path.read_text("utf-8")
    config_path.write_text(example_text, "utf-8")
    return config_path


def create_start_script_file(source_script_path: Path, windows: bool = False) -> Path:
    source_script = source_script_path.read_text(encoding="utf-8")

    if windows:
        new_script = f"cd /D {root_path.absolute()}\n{source_script}"
    else:
        new_script = f"cd {root_path.absolute()}\n{source_script}"

    new_script_path = root_path / source_script_path.name
    new_script_path.write_text(new_script)
    return new_script_path


def create_start_script(windows: bool):
    if windows:
        return create_start_script_file(root_path / "scripts/start.bat", windows)

    return create_start_script_file(root_path / "scripts/start.sh", windows)


def main():
    try:
        config_path = create_config()
    except Exception as e:
        print(e)
    else:
        print(f"Конфиг успешно создан. Заполните его -> {config_path.absolute()}")

    current_os = platform.system()
    is_on_windows = current_os == "Windows"
    start_script_path = create_start_script(is_on_windows)

    print(f"Скрипт запуска успешно создан -> {start_script_path.absolute()}")

    if is_on_windows:
        os.system("pause")


if __name__ == "__main__":
    main()
