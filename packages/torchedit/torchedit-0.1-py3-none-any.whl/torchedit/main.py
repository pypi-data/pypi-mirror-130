import torch
import torchvision.models as models

def Edit_out_features(model, model_type, out_feature):
    if model_type == "resnet":
        model.fc = torch.nn.Linear(in_features=512, out_features=out_feature, bias=True)
    if model_type == "VGG":
        model.classifier[-1] = torch.nn.Linear(in_features=4096, out_features=out_feature, bias=True)

    return model
    
