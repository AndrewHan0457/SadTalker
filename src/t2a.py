import os.path

import edge_tts
import asyncio

# TEXT = ""
# txtfile = '孺子帝.txt'

# output = f'{os.path.splitext(txtfile)[0]}.mp3'

# with open(txtfile, 'rb') as f:
#     data = f.read()
#     TEXT = data.decode('utf-8')
# print(f"load file {TEXT[:100]} done!")
"""
Name: zh-CN-XiaoxiaoNeural
Gender: Female

Name: zh-CN-XiaoyiNeural
Gender: Female

Name: zh-CN-YunjianNeural
Gender: Male

Name: zh-CN-YunxiNeural
Gender: Male

Name: zh-CN-YunxiaNeural
Gender: Male

Name: zh-CN-YunyangNeural
Gender: Male

Name: zh-CN-liaoning-XiaobeiNeural
Gender: Female

Name: zh-CN-shaanxi-XiaoniNeural
Gender: Female
"""
# voice = 'zh-CN-XiaoxiaoNeural'
# rate = '+0%'
# volume = '+50%'


async def t2a(text, voice, rate, volume):
    rate = f"+{rate}%"
    volume = f"+{volume}%"
    output = "./audio/tmp.mp3"
    tts = edge_tts.Communicate(
        text=text,
        voice=voice,
        rate=rate,
        volume=volume
    )
    if os.path.exists(output):
        os.remove(output)
    await tts.save(output)
    return output


if __name__ == '__main__':
    asyncio.run(t2a("请上传您自己的音频文件", "zh-CN-XiaoxiaoNeural", "+0%", "+0%"))
