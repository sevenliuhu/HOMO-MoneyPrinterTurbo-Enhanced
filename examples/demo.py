#!/usr/bin/env python3
"""HOMO-MoneyPrinterTurbo-Enhanced — 快速演示"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from money_printer_enhanced import HOMOPipeline

def main():
    pipeline = HOMOPipeline()

    # 演示1：从模板生成
    print('=== Demo 1: 从模板生成 ===')
    result = pipeline.from_template('five-goals', '/tmp/homo_demo_template.mp4')
    print(f'Result: {result}\n')

    # 演示2：自定义脚本
    print('=== Demo 2: 自定义脚本 ===')
    script = [
        {'layout': 'title', 'header': '今日AI分享', 'duration': 2.5},
        {'layout': 'numbered', 'header': '三步骤', 'items': ['想清楚', '开始做', '坚持'],
         'durations': [1.5, 1.5, 1.5, 1.5]},
    ]
    result2 = pipeline.from_script(script, '/tmp/homo_demo_custom.mp4')
    print(f'Result: {result2}\n')

if __name__ == '__main__':
    main()
