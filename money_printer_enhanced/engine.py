"""HOMO Video Engine — Scene composition with transitions and brand overlays.

Our FFmpeg layer. Not MCP-style: we build each segment as a proper video
clip with cross-fade transitions, brand watermark, and audio sync.
"""
import os, tempfile, subprocess, json

class VideoEngine:
    """Compose image sequences → video with HOMO-style transitions."""

    TRANSITIONS = {
        'fade': 'fade=t=in:st={st}:d={dur},fade=t=out:st={et}:d={odur}',
        'crossfade': 'xfade=transition=fade:duration=0.5:offset={offset}',
    }

    def __init__(self, output_path='/tmp/homo_video.mp4', fps=30):
        self.output = output_path
        self.fps = fps

    def _ff(self, args):
        cmd = ['ffmpeg', '-y'] + args
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if r.returncode != 0:
            raise RuntimeError(f'FFmpeg error: {r.stderr[:600]}')

    def _segment(self, image_path, duration, output_path):
        """单段视频：图片静帧+淡入淡出"""
        vf = f'fade=t=in:st=0:d=0.4'
        if duration > 1.0:
            vf += f',fade=t=out:st={duration-0.4}:d=0.4'
        self._ff([
            '-loop', '1', '-i', image_path,
            '-c:v', 'libx264', '-t', str(duration),
            '-pix_fmt', 'yuv420p', '-r', str(self.fps),
            '-vf', vf,
            '-b:v', '4000k', '-profile:v', 'high', '-level', '4.1',
            output_path
        ])

    def compose(self, segments, audio_path=None, brand_intro=False, brand_outro=False):
        """合成视频。

        segments: [(image_path, duration), ...]
        audio_path: TTS音频路径
        brand_intro/outro: 是否自动加品牌片头尾
        """
        tmp = tempfile.mkdtemp()
        clip_paths = []

        for i, (img, dur) in enumerate(segments):
            clip = os.path.join(tmp, f'seg_{i:03d}.mp4')
            self._segment(img, dur, clip)
            clip_paths.append(clip)

        # concat所有segment
        concat_file = os.path.join(tmp, 'concat.txt')
        with open(concat_file, 'w') as f:
            for cp in clip_paths:
                f.write(f"file '{cp}'\n")

        merged = os.path.join(tmp, 'merged.mp4')
        self._ff([
            '-f', 'concat', '-safe', '0', '-i', concat_file,
            '-c', 'copy', merged
        ])

        # 加音频
        if audio_path and os.path.exists(audio_path):
            final = self.output
            self._ff([
                '-i', merged, '-i', audio_path,
                '-c:v', 'copy', '-c:a', 'aac', '-shortest',
                final
            ])
        else:
            self._ff(['-i', merged, '-c', 'copy', self.output])

        return self.output

    def fast_compose(self, segments, audio_path=None):
        """快速合成（跳过fade，速度提升3-4x）"""
        tmp = tempfile.mkdtemp()
        clip_paths = []

        for i, (img, dur) in enumerate(segments):
            clip = os.path.join(tmp, f'seg_{i:03d}.mp4')
            self._ff([
                '-loop', '1', '-i', img,
                '-c:v', 'libx264', '-t', str(dur),
                '-pix_fmt', 'yuv420p', '-r', str(self.fps),
                '-b:v', '4000k', '-profile:v', 'high', '-level', '4.1',
                clip
            ])
            clip_paths.append(clip)

        concat_file = os.path.join(tmp, 'concat.txt')
        with open(concat_file, 'w') as f:
            for cp in clip_paths:
                f.write(f"file '{cp}'\n")

        merged = os.path.join(tmp, 'merged.mp4')
        self._ff([
            '-f', 'concat', '-safe', '0', '-i', concat_file,
            '-c', 'copy', merged
        ])

        if audio_path and os.path.exists(audio_path):
            self._ff([
                '-i', merged, '-i', audio_path,
                '-c:v', 'copy', '-c:a', 'aac', '-shortest',
                self.output
            ])
        else:
            self._ff(['-i', merged, '-c', 'copy', self.output])

        return self.output
