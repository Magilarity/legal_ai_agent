# app/document_generator.py
from typing import Any, Dict

import jinja2
from jinja2.sandbox import SandboxedEnvironment


class DocumentGenerator:
    """
    Генерує документи за шаблонами з використанням безпечного оточення Jinja2.
    """

    def __init__(self, template: str):
        # Створюємо sandbox-оточення з суворим Undefined, щоб невизначені змінні викликали помилку
        self.env = SandboxedEnvironment(
            undefined=jinja2.StrictUndefined,
            autoescape=False,
        )
        self.template_str = template

    def render(self, context: Dict[str, Any]) -> str:
        """
        Рендерить шаблон у переданому безпечному контексті.

        :param context: словник із ключами-шаблонами
        :raises jinja2.exceptions.UndefinedError: якщо в шаблоні є невизначена змінна
        :raises jinja2.exceptions.SecurityError: при порушенні правил sandbox
        """
        tmpl = self.env.from_string(self.template_str)
        return tmpl.render(**context)
