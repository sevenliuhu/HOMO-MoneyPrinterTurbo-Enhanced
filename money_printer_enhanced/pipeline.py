"""HOMO Pipeline — Turn structured scripts into branded Douyin-style videos.

One-shot entry point for the entire engine.
"""
import os, json, tempfile, subprocess
from .composer import CardComposer
from .audio import AudioEngine
from .engine import VideoEngine
from .brand import BrandAssets

class HOMOPipeline:
    """端到端视频管线：脚本→卡片→配音→品牌水印→视频合成"""

    def __init__(self, font_path=None, voice='zh-CN-XiaoxiaoNeural', rate='+15%'):
        self.composer = CardComposer(font_path)
        self.audio = AudioEngine(voice, rate)
        self.video = VideoEngine()
        self.brand = BrandAssets()

    def from_script(self, script, output_path='/tmp/homo_output.mp4', brand=True):
        """从结构化脚本生成视频。

        script = [
            {'layout': 'title', 'header': '标题', 'duration': 3.0},
            {'layout': 'bullet', 'header': '第一节', 'items': ['a', 'b'],
             'durations': [2.0, 2.0, 2.0]},
            {'layout': 'numbered', 'header': '第二节', 'items': ['x', 'y']},
            {'layout': 'quote', 'header': '名言', 'subtitle': '作者'},
        ]
        output_path: 输出视频路径
        brand: 是否自动加HOMO品牌片头尾卡
        """
        tmp = tempfile.mkdtemp()
        all_segments = []

        # ===== 品牌片头 =====
        if brand:
            intro_card = os.path.join(tmp, 'brand_intro.png')
            self.brand.make_intro_card().save(intro_card)
            all_segments.append((intro_card, 2.5))

        # ===== 场景卡片 =====
        for idx, scene in enumerate(script):
            scene = dict(scene)
            scene['id'] = f'scene_{idx}'
            seq = self.composer.generate_sequence(scene, tmp)
            all_segments.extend(seq)

        # ===== 品牌片尾 =====
        if brand:
            outro_card = os.path.join(tmp, 'brand_outro.png')
            self.brand.make_outro_card().save(outro_card)
            all_segments.append((outro_card, 2.5))

        # ===== 配音 =====
        descs = []
        for scene in script:
            descs.append(scene.get('header', ''))
            for item in scene.get('items', []):
                descs.append(item)

        audio_path = os.path.join(tmp, 'narration.mp3')
        audio_path, audio_dur = self.audio.make_narration_with_intro(descs, audio_path)

        # ===== 合成 =====
        self.video.output = output_path
        self.video.compose(all_segments, audio_path)

        # ===== 自检 =====
        size_mb = os.path.getsize(output_path) / 1024 / 1024
        r = subprocess.run([
            'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1', output_path
        ], capture_output=True, text=True)
        dur = float(r.stdout.strip() or 0)

        print(f'HOMO Pipeline complete:')
        print(f'  Output: {output_path}')
        print(f'  Duration: {dur:.1f}s')
        print(f'  Size: {size_mb:.1f}MB')
        print(f'  Scenes: {len(script)} + brand intro/outro')
        print(f'  Audio: {audio_path} ({audio_dur:.1f}s)')

        return output_path

    def from_template(self, template_name, output_path='/tmp/homo_output.mp4'):
        """从JSON模板生成"""
        tpl_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
        tpl_path = os.path.join(tpl_dir, f'{template_name}.json')
        if not os.path.exists(tpl_path):
            raise FileNotFoundError(f'Template "{template_name}" not found')
        with open(tpl_path) as f:
            script = json.load(f)
        return self.from_script(script, output_path)


def quick_homo(script, output='/tmp/homo_quick.mp4'):
    """One-liner: 结构化脚本→品牌视频"""
    p = HOMOPipeline()
    return p.from_script(script, output)
