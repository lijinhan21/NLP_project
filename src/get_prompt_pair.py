from diffusers import StableDiffusionPipeline
from eval.simple_inference import MetricModel

pipe = StableDiffusionPipeline.from_pretrained("/share/ljh", local_files_only=True).to("cuda")
model = MetricModel()

def checkPromptPair(good, bad):
	image_good = pipe(good, guidance_scale=10).images[0]
	print(type(image_good))
	score_good = model.getScore(img_path=image_good, text='a bridge')
	print(score_good)
	image_bad = pipe(bad, guidance_scale=10).images[0]
	print(type(image_bad))
checkPromptPair('末日永恒，都市大逃亡，游戏概念艺术，静脉和蠕虫，肌肉，甲壳类动物外骨骼，翅目动物头部，翅目耳朵，机甲，凶猛，凶猛，超现实主义，精细细节，艺术站，无背景', '末日永恒')