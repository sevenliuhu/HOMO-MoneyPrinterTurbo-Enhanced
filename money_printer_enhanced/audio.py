"""HOMO Audio Engine — TTS with brand intro/outro stings and audio mixing."""
import asyncio, os, tempfile, subprocess

class AudioEngine:
    """Voice-over generation with brand audio stings.

    - Synthesizes scene narration via edge-tts
    - Adds HOMO brand intro/outro audio stings
    - Mixes and normalizes levels
    """

    def __init__(self, voice='zh-CN-XiaoxiaoNeural', rate='+15%'):
        self.voice = voice
        self.rate = rate

    def _say(self, text, output):
        async def _run():
            import edge_tts
            tts = edge_tts.Communicate(text, voice=self.voice, rate=self.rate)
            await tts.save(output)
        asyncio.run(_run())

    def _duration(self, path):
        r = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
             '-of', 'default=noprint_wrappers=1:nokey=1', path],
            capture_output=True, text=True
        )
        return float(r.stdout.strip() or 0)

    def make_narration(self, scene_descriptions, output_path):
        """生成配音音频。
        scene_descriptions: [text_for_scene1, text_for_scene2, ...]
        """
        full_text = '。'.join(scene_descriptions) + '。'
        self._say(full_text, output_path)
        dur = self._duration(output_path)
        return output_path, dur

    def make_narration_with_intro(self, scene_descriptions, output_path):
        """生成带品牌片头sting的配音"""
        tmp = tempfile.mktemp(suffix='.mp3')

        # 品牌intro sting（短）
        intro_text = 'HOMO AI Studio，智能视频创作引擎。'
        intro_path = tempfile.mktemp(suffix='.mp3')
        self._say(intro_text, intro_path)
        intro_dur = self._duration(intro_path)

        # 主体配音
        main_text = '。'.join(scene_descriptions) + '。'
        main_path = tempfile.mktemp(suffix='.mp3')
        self._say(main_text, main_path)

        # 品牌outro sting
        outro_text = f'感谢观看，更多AI工具尽在HOMO AI Studio。'
        outro_path = tempfile.mktemp(suffix='.mp3')
        self._say(outro_text, outro_path)

        # 合并
        concat_file = tempfile.mktemp(suffix='.txt')
        with open(concat_file, 'w') as f:
            f.write(f"file '{intro_path}'\n")
            f.write(f"file '{main_path}'\n")
            f.write(f"file '{outro_path}'\n")

        subprocess.run([
            'ffmpeg', '-y', '-f', 'concat', '-safe', '0',
            '-i', concat_file, '-c', 'copy', output_path
        ], capture_output=True, timeout=30)

        dur = self._duration(output_path)
        return output_path, dur
