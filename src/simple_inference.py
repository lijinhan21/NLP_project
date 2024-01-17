import webdataset as wds
from PIL import Image
import io
import matplotlib.pyplot as plt
import os
import json

from warnings import filterwarnings


# os.environ["CUDA_VISIBLE_DEVICES"] = "0"    # choose GPU if you are on a multi GPU server
import numpy as np
import torch
# import pytorch_lightning as pl
import torch.nn as nn
from torchvision import datasets, transforms
import tqdm

from os.path import join
from datasets import load_dataset
import pandas as pd
from torch.utils.data import Dataset, DataLoader
import json

import clip
from torchmetrics.multimodal.clip_score import CLIPScore

from PIL import Image, ImageFile

# if you changed the MLP architecture during training, change it also here:
class MLP(nn.Module):
    def __init__(self, input_size, xcol='emb', ycol='avg_rating'):
        super().__init__()
        self.input_size = input_size
        self.xcol = xcol
        self.ycol = ycol
        self.layers = nn.Sequential(
            nn.Linear(self.input_size, 1024),
            #nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(1024, 128),
            #nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(128, 64),
            #nn.ReLU(),
            nn.Dropout(0.1),

            nn.Linear(64, 16),
            #nn.ReLU(),

            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.layers(x)

    def training_step(self, batch, batch_idx):
            x = batch[self.xcol]
            y = batch[self.ycol].reshape(-1, 1)
            x_hat = self.layers(x)
            loss = F.mse_loss(x_hat, y)
            return loss
    
    def validation_step(self, batch, batch_idx):
        x = batch[self.xcol]
        y = batch[self.ycol].reshape(-1, 1)
        x_hat = self.layers(x)
        loss = F.mse_loss(x_hat, y)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.Adam(self.parameters(), lr=1e-3)
        return optimizer

def normalized(a, axis=-1, order=2):
    import numpy as np  # pylint: disable=import-outside-toplevel

    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2 == 0] = 1
    return a / np.expand_dims(l2, axis)

class MetricModel:
    def __init__(self):
        model = MLP(768)  # CLIP embedding dim is 768 for CLIP ViT L 14

        s = torch.load("/home/lch/NLP_project/eval/sac+logos+ava1-l14-linearMSE.pth")   # load the model you trained previously or the model available in this repo

        model.load_state_dict(s)

        model.to("cuda")
        model.eval()

        device = "cuda" if torch.cuda.is_available() else "cpu"
        model2, preprocess = clip.load("ViT-L/14", device=device)  #RN50x64   
        self.model = model
        self.model2 = model2
        self.device = device
        self.preprocess = preprocess
    def getScore(self, img_path, text):
        pil_image = Image.open(img_path) if isinstance(img_path, str) else img_path

        image = self.preprocess(pil_image).unsqueeze(0).to(self.device)

        with torch.no_grad():
            image_features = self.model2.encode_image(image)

        im_emb_arr = normalized(image_features.cpu().detach().numpy() )

        prediction = float(self.model(torch.from_numpy(im_emb_arr).to(self.device).type(torch.cuda.FloatTensor)))

        print( "Aesthetic score predicted by the model:", prediction)

        cos = torch.nn.CosineSimilarity(dim=0)
        text_inputs = clip.tokenize(text).to(self.device)
        text_features = self.model2.encode_text(text_inputs)
        similarity = cos(image_features[0], text_features[0]).item()
        print( "CLIP similarity predicted by the model:", similarity)

        return prediction, similarity

if __name__ == '__main__':
    model = MetricModel()
    model.getScore(img_path='1.png', text='a bridge')
    model.getScore(img_path='1.png', text='Small bridge, flowing water and household')
    model.getScore(img_path='1.png', text='Small bridge, flowing water and household, Van Gogh style')
    model.getScore(img_path='1.png', text='a scenary')


# metric = CLIPScore(model_name_or_path="openai/clip-vit-base-patch16")
# score = metric(torch.randint(255, (3, 224, 224), generator=torch.manual_seed(42)), "a photo of a cat")
# score.detach()
# print(score)
