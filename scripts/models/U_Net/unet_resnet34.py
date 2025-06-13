import segmentation_models_pytorch as smp
import torch.nn as nn
import torch

class UNetResNet34(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = smp.Unet(
            encoder_name="resnet34",        # transfer model
            encoder_weights= None,     # pretrained
            in_channels=1,                  # grayscale
            classes=1,                      # binary mask
            activation=None                 # sigmoid sonra uygulanacak
        )

    def forward(self, x):
        out=self.model(x)
        return out
