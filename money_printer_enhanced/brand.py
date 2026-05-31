"""Brand assets for HOMO visual identity in video output."""
import os
from PIL import Image, ImageDraw, ImageFont

_font_paths = [
    '/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf',
    '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
]

class BrandAssets:
    """HOMO品牌资产管理 — 水印/片头/片尾"""

    COLORS = {
        'bg': (10, 12, 28),
        'accent': (80, 180, 255),
        'white': (255, 255, 255),
        'gray': (160, 170, 190),
        'gold': (255, 215, 0),
    }

    def __init__(self):
        self.font = None
        for p in _font_paths:
            if os.path.exists(p):
                self.font = p
                break

    def make_watermark(self, img):
        """给图片打HOMO水印（右下角半透明）"""
        d = ImageDraw.Draw(img)
        f = ImageFont.truetype(self.font, 18)
        text = 'HOMO AI Studio'
        bbox = d.textbbox((0, 0), text, font=f)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        x, y = 1080 - tw - 20, 1920 - th - 20
        # 半透明背景
        overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rectangle([x-10, y-8, x+tw+10, y+th+10], fill=(0, 0, 0, 100))
        od.text((x, y), text, fill=(255, 255, 255, 160), font=f)
        img.paste(Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB'))
        return img

    def make_intro_card(self):
        """HOMO品牌片头卡"""
        img = Image.new('RGB', (1080, 1920), self.COLORS['bg'])
        d = ImageDraw.Draw(img)
        # 品牌色装饰
        d.rectangle([200, 400, 880, 406], fill=self.COLORS['accent'])
        d.rectangle([200, 1514, 880, 1520], fill=self.COLORS['accent'])
        # LOGO文字
        f = ImageFont.truetype(self.font, 96)
        d.text(((1080 - d.textlength('HOMO', font=f))/2, 600), 'HOMO', fill=self.COLORS['accent'], font=f)
        f2 = ImageFont.truetype(self.font, 36)
        d.text(((1080 - d.textlength('AI Studio', font=f2))/2, 740), 'AI Studio', fill=self.COLORS['gray'], font=f2)
        # 副标题
        f3 = ImageFont.truetype(self.font, 48)
        d.text(((1080 - d.textlength('AI 短视频生成引擎', font=f3))/2, 1300), 'AI 短视频生成引擎', fill=self.COLORS['white'], font=f3)
        return self.make_watermark(img)

    def make_outro_card(self):
        """HOMO品牌尾卡"""
        img = Image.new('RGB', (1080, 1920), self.COLORS['bg'])
        d = ImageDraw.Draw(img)
        d.rectangle([250, 500, 830, 503], fill=self.COLORS['accent'])
        f = ImageFont.truetype(self.font, 72)
        text = '感谢观看'
        d.text(((1080 - d.textlength(text, font=f))/2, 600), text, fill=self.COLORS['white'], font=f)
        f2 = ImageFont.truetype(self.font, 32)
        d.text(((1080 - d.textlength('HOMO AI Studio', font=f2))/2, 800), 'HOMO AI Studio', fill=self.COLORS['accent'], font=f2)
        return self.make_watermark(img)

    def apply_brand_overlay(self, img_path, output_path=None):
        """给指定图片打HOMO水印"""
        img = Image.open(img_path).convert('RGB')
        result = self.make_watermark(img)
        out = output_path or img_path
        result.save(out, quality=95)
        return out
