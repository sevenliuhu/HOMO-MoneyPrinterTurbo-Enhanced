"""HOMO Visual Card Engine — Multi-layout card generator with progressive text animation.

Supports: title cards, bullet-point cards, list cards, and free-form layouts.
Each card type has its own visual DNA — unified by brand colors.
"""
import os, json
from PIL import Image, ImageDraw, ImageFont

# Resolution
W, H = 1080, 1920

# Brand palette
PALETTE = {
    'bg': (10, 12, 28),
    'accent': (80, 180, 255),
    'white': (255, 255, 255),
    'gray': (160, 170, 190),
    'muted': (60, 70, 100),
}

class CardCanvas:
    """A blank canvas ready for card composition."""

    def __init__(self, bg=PALETTE['bg']):
        self.img = Image.new('RGB', (W, H), bg)
        self.d = ImageDraw.Draw(self.img)

    def save(self, path):
        self.img.save(path)
        return path


class CardComposer:
    """Card layout engine — generates progressive text cards.

    Layout types:
    - 'title': big centered text, decorative top line
    - 'bullet': header + bullet items with dot markers
    - 'numbered': header + numbered items
    - 'split': two-column layout
    - 'quote': large quote text
    """

    def __init__(self, font_path=None):
        self._font_path = font_path
        if not font_path:
            for p in ['/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
                       '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc']:
                if os.path.exists(p):
                    self._font_path = p
                    break
        if not self._font_path:
            raise RuntimeError('No CJK font available')

    def _f(self, size): return ImageFont.truetype(self._font_path, size, encoding='unic')

    # ---- Layout primitives ---- #

    def _deco_line(self, canvas, y, w=500, h=3):
        """装饰细线"""
        x0 = (W - w) // 2
        canvas.d.rectangle([x0, y, x0 + w, y + h], fill=PALETTE['accent'])

    def _dot(self, canvas, x, y, r=8):
        """小圆点"""
        canvas.d.ellipse([x - r, y - r, x + r, y + r], fill=PALETTE['accent'])

    def _centered_text(self, canvas, text, font, y, color=PALETTE['white']):
        w = canvas.d.textlength(text, font=font)
        canvas.d.text(((W - w) / 2, y), text, fill=color, font=font)
        return w

    # ---- Card layouts ---- #

    def title_card(self, text, subtitle=None):
        """Type: title — 大字居中，上下装饰线"""
        c = CardCanvas()
        self._deco_line(c, 480, 600)
        self._deco_line(c, 1440, 600)
        f = self._f(72)
        self._centered_text(c, text, f, 700)
        if subtitle:
            fs = self._f(36)
            self._centered_text(c, subtitle, fs, 880, PALETTE['gray'])
        return c.img

    def bullet_card(self, header, items, accent_color=PALETTE['accent']):
        """Type: bullet — 标题 + 小圆点列表"""
        c = CardCanvas()
        # 顶部装饰线
        self._deco_line(c, 380)
        # 标题
        fh = self._f(56)
        self._centered_text(c, header, fh, 460)
        # 列表项
        fn = self._f(40)
        for i, item in enumerate(items):
            y = 660 + i * 100
            self._dot(c, 260, y + 14)
            c.d.text((300, y), item, fill=PALETTE['white'], font=fn)
        return c.img

    def numbered_card(self, header, items):
        """Type: numbered — 标题 + 带序号列表"""
        c = CardCanvas()
        self._deco_line(c, 380)
        fh = self._f(56)
        self._centered_text(c, header, fh, 460)
        fn = self._f(40)
        for i, item in enumerate(items):
            y = 660 + i * 100
            # 数字圆圈
            num = str(i + 1)
            fn2 = self._f(28)
            cx = 260
            c.d.ellipse([cx - 16, y - 4, cx + 16, y + 28], outline=PALETTE['accent'], width=2)
            tw = self._centered_text(c, num, fn2, y, PALETTE['accent'])
            c.d.text((300, y), item, fill=PALETTE['white'], font=fn)
        return c.img

    def quote_card(self, quote, author=None):
        """Type: quote — 大引文"""
        c = CardCanvas()
        self._deco_line(c, 500, 200)
        # 左引号
        fq = self._f(120)
        c.d.text((200, 580), '"', fill=PALETTE['accent'], font=fq)
        # 正文
        fb = self._f(48)
        lines = self._wrap_text(quote, fb, 700)
        for i, line in enumerate(lines):
            self._centered_text(c, line, fb, 720 + i * 70, PALETTE['white'])
        if author:
            fa = self._f(32)
            self._centered_text(c, f'— {author}', fa, 720 + len(lines) * 70 + 40, PALETTE['gray'])
        return c.img

    def _wrap_text(self, text, font, max_w):
        """简单换行（按字符数粗分）"""
        lines = []
        current = ''
        for ch in text:
            test = current + ch
            if len(test) > 12:  # 大约12个中文字换行
                lines.append(current)
                current = ch
            else:
                current = test
        if current:
            lines.append(current)
        return lines

    # ---- Progressive sequence generator ---- #

    def generate_sequence(self, scene_config, output_dir):
        """Generate a progressive image sequence from a scene config.

        scene_config = {
            'layout': 'bullet',
            'header': '标题文字',
            'items': ['子1', '子2'],
            'duration': 2.0,          # base duration per step
            'durations': [1.5, 2.0],  # per-step overrides
        }
        Returns: [(image_path, duration), ...]
        """
        os.makedirs(output_dir, exist_ok=True)

        layout = scene_config.get('layout', 'bullet')
        header = scene_config.get('header', '')
        items = scene_config.get('items', [])
        durations = scene_config.get('durations',
                                     [scene_config.get('duration', 2.0)] * (len(items) + 1))

        paths = []

        if layout == 'title':
            # Title card: single image
            p = os.path.join(output_dir, f'{scene_config.get("id", "card")}_title.png')
            img = self.title_card(header, scene_config.get('subtitle'))
            img.save(p)
            paths.append((p, durations[0] if durations else 3.0))

        elif layout == 'bullet':
            # Progressive: header first, then items one-by-one
            for i in range(len(items) + 1):
                p = os.path.join(output_dir, f'{scene_config.get("id", "card")}_step_{i}.png')
                img = self.bullet_card(header, items[:i])
                img.save(p)
                dur = durations[i] if i < len(durations) else durations[-1]
                paths.append((p, dur))

        elif layout == 'numbered':
            for i in range(len(items) + 1):
                p = os.path.join(output_dir, f'{scene_config.get("id", "card")}_step_{i}.png')
                img = self.numbered_card(header, items[:i])
                img.save(p)
                dur = durations[i] if i < len(durations) else durations[-1]
                paths.append((p, dur))

        elif layout == 'quote':
            p = os.path.join(output_dir, f'{scene_config.get("id", "card")}_quote.png')
            img = self.quote_card(header, scene_config.get('subtitle'))
            img.save(p)
            paths.append((p, durations[0] if durations else 3.0))

        return paths
