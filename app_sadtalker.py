import os, sys
import gradio as gr

from src import t2a
from src.gradio_demo import SadTalker

try:
    import webui  # in webui

    in_webui = True
except:
    in_webui = False


def toggle_audio_file(choice):
    if choice == False:
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)


def ref_video_fn(path_of_ref_video):
    if path_of_ref_video is not None:
        return gr.update(value=True)
    else:
        return gr.update(value=False)


def sadtalker_demo(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):
    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    with gr.Blocks(analytics_enabled=False) as sadtalker_interface:
        gr.Markdown("<div align='center'> <h2> 😭 SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation (CVPR 2023) </span> </h2> \
                    <a style='font-size:18px;color: #efefef' href='https://arxiv.org/abs/2211.12194'>Arxiv</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                    <a style='font-size:18px;color: #efefef' href='https://sadtalker.github.io'>Homepage</a>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                     <a style='font-size:18px;color: #efefef' href='https://github.com/Winfredy/SadTalker'> Github </div>")

        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                with gr.Tabs(elem_id="sadtalker_source_image"):
                    with gr.TabItem('上传图片'):
                        with gr.Row():
                            source_image = gr.Image(label="原图", source="upload", type="filepath", elem_id="img2img_image").style(width=512)

                with gr.Tabs(elem_id="sadtalker_driven_text"):
                    with gr.TabItem('请输入文本'):
                        with gr.Column(variant='panel'):
                            driven_text = gr.inputs.Textbox(label="文本", type="text")
                        # with gr.TabItem('语音'):
                        with gr.Column(variant='panel'):
                            voice = gr.Dropdown(
                                label="语音",
                                choices=['zh-CN-XiaoxiaoNeural',
                                         'zh-CN-XiaoyiNeural',
                                         'zh-CN-YunjianNeural',
                                         'zh-CN-YunxiNeural',
                                         'zh-CN-YunxiaNeural',
                                         'zh-CN-YunyangNeural',
                                         'zh-CN-liaoning-XiaobeiNeural',
                                         'zh-CN-shaanxi-XiaoniNeural'
                                         ],
                                value='zh-CN-XiaoxiaoNeural',
                                type='value',
                                interactive=True
                            )
                            rate = gr.Slider(
                                label="语速",
                                interactive=True,
                                step=10,
                            )
                            volume = gr.Slider(
                                label="音量",
                                interactive=True,
                                step=10,
                            )

                    b_t2a = gr.Button('文字->语音', elem_id="sadtalker_generate", variant='primary')

                with gr.Tabs(elem_id="sadtalker_driven_audio"):
                    # with gr.TabItem('上传音频'):
                    with gr.Column(variant='panel'):
                        driven_audio = gr.Audio(value="./audio/tmp.mp3", label="音频", source="upload", type="filepath")

                        if sys.platform != 'win32' and not in_webui:
                            from src.utils.text2speech import TTSTalker
                            tts_talker = TTSTalker()
                            with gr.Column(variant='panel'):
                                input_text = gr.Textbox(label="Generating audio from text", lines=5, placeholder="please enter some text here, we genreate the audio from text using @Coqui.ai TTS.")
                                tts = gr.Button('Generate audio', elem_id="sadtalker_audio_generate", variant='primary')
                                tts.click(fn=tts_talker.test, inputs=[input_text], outputs=[driven_audio])

            with gr.Column(variant='panel'):
                with gr.Tabs(elem_id="sadtalker_checkbox"):
                    with gr.TabItem('设置'):
                        gr.Markdown("帮助：请访问 [best practice page](https://github.com/OpenTalker/SadTalker/blob/main/docs/best_practice.md) 获取更多信息")
                        with gr.Column(variant='panel'):
                            # width = gr.Slider(minimum=64, elem_id="img2img_width", maximum=2048, step=8, label="Manually Crop Width", value=512) # img2img_width
                            # height = gr.Slider(minimum=64, elem_id="img2img_height", maximum=2048, step=8, label="Manually Crop Height", value=512) # img2img_width
                            pose_style = gr.Slider(minimum=0, maximum=46, step=1, label="姿态", value=0)  #
                            size_of_image = gr.Radio([256, 512], value=256, label='脸部模型分辨率（建议默认256）', info="使用256或512模型")  #
                            preprocess_type = gr.Radio(['crop', 'resize', 'full'], value='full', label='预处理器', info="如何处理原图:[只处理脸部，适应，全图]")
                            is_still_mode = gr.Checkbox(label="专注模式 (减少手部动作, 只对 `full`处理器生效)")
                            batch_size = gr.Slider(label="分区处理大小（建议默认2）", step=1, maximum=10, value=2)
                            enhancer = gr.Checkbox(label="脸部还原（更高清但更慢）")
                            submit = gr.Button('生成', elem_id="sadtalker_generate", variant='primary')

                with gr.Tabs(elem_id="sadtalker_genearted"):
                    gen_video = gr.Video(label="生成视频", format="mp4").style(width=256)

        if warpfn:
            submit.click(
                fn=warpfn(sad_talker.test),
                inputs=[source_image,
                        driven_audio,
                        preprocess_type,
                        is_still_mode,
                        enhancer,
                        batch_size,
                        size_of_image,
                        pose_style
                        ],
                outputs=[gen_video]
            )
        else:
            submit.click(
                fn=sad_talker.test,
                inputs=[source_image,
                        driven_audio,
                        preprocess_type,
                        is_still_mode,
                        enhancer,
                        batch_size,
                        size_of_image,
                        pose_style,
                        # driven_text
                        ],
                outputs=[gen_video]
            )
        # 文字转语音按钮
        b_t2a.click(
            fn=t2a.t2a,
            inputs=[driven_text,
                    voice,
                    rate,
                    volume
                    ],
            outputs=[driven_audio]
        )
    return sadtalker_interface


if __name__ == "__main__":
    demo = sadtalker_demo()
    demo.queue()
    demo.launch()
