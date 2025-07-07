import re
from .data import COLORS

class MarkdownFormatter:
    """Markdown formatter for AI requests"""
    def __init__(self):
        self.rules = [
            (r'<think>(.*?)</think>', f"{COLORS['cyan']}\\1{COLORS['reset']}"),
            (r'^(#+)(.*)', self._handle_headers),  # Заголовки
            (r'\*\*(.*?)\*\*', f"{COLORS['bold']}\\1{COLORS['reset']}"),  # Жирный
            (r'\*(.*?)\*', f"{COLORS['italic']}\\1{COLORS['reset']}"),  # Курсив
            (r'`{3}(.*?)`{3}', self._handle_code_block),  # Блок кода
            (r'`(.*?)`', f"{COLORS['blue']}\\1{COLORS['reset']}"),  # Инлайн код
            (r'!\[(.*?)\]\((.*?)\)', f"{COLORS['cyan']}[Image: \\1]{COLORS['reset']}"),  # Картинки
            (r'\[(.*?)\]\((.*?)\)', f"{COLORS['blue']}\\1{COLORS['reset']}"),  # Ссылки
            (r'^> (.*)', f"{COLORS['yellow']}│ \\1{COLORS['reset']}"),  # Цитаты
            (r'^(\d+\.)(.*)', self._handle_ordered_list),  # Нумерованные списки
            (r'^[-*+] (.*)', self._handle_unordered_list),  # Маркированные списки
        ]

        self.md_colors = {
            'bold': '\033[1m',
            'italic': '\033[3m',
            'reset': '\033[0m',
            'blue': '\033[34m',
            'cyan': '\033[36m',
            'yellow': '\033[33m',
            'gray': '\033[90m'
        }

    def _handle_headers(self, match):
        level = len(match.group(1))
        color = self.md_colors['yellow'] if level < 3 else self.md_colors['gray']
        return f"{color}{'#'*level} {match.group(2)}{self.md_colors['reset']}"

    def _handle_code_block(self, match):
        code = match.group(1)
        return (f"\n{self.md_colors['blue']}┌     \n"
                f"{code}\n"
                f"└     {self.md_colors['reset']}\n")

    def _handle_ordered_list(self, match):
        return f"{self.md_colors['cyan']}{match.group(1)}{self.md_colors['reset']}{match.group(2)}"

    def _handle_unordered_list(self, match):
        return f"{self.md_colors['cyan']}•{self.md_colors['reset']} {match.group(1)}"

    def format(self, text):
        for pattern, replacement in self.rules:
            text = re.sub(pattern, replacement, text, flags=re.MULTILINE|re.DOTALL)
        return text
