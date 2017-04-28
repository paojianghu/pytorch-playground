import torch
import torch.nn as nn
from collections import OrderedDict
import os
import torch.utils.model_zoo as model_zoo
from IPython import embed
from utee import misc
print = misc.logger.info

model_urls = {
    'mnist': 'none'
}

class MLP(nn.Module):
    def __init__(self, input_dims, n_hiddens, n_class):
        super(MLP, self).__init__()
        assert isinstance(input_dims, int), 'Please provide int for input_dims'
        self.input_dims = input_dims
        current_dims = input_dims
        layers = OrderedDict()

        if isinstance(n_hiddens, int):
            n_hiddens = [n_hiddens]
        else:
            n_hiddens = list(n_hiddens)
        for i, n_hidden in enumerate(n_hiddens):
            layers['fc{}'.format(i+1)] = nn.Linear(current_dims, n_hidden)
            layers['relu{}'.format(i+1)] = nn.ReLU()
            layers['drop{}'.format(i+1)] = nn.Dropout(0.2)
            current_dims = n_hidden
        layers['out'] = nn.Linear(current_dims, n_class)

        self.model= nn.Sequential(layers)
        print(self.model)

    def forward(self, input):
        input = input.view(input.size(0), -1)
        assert input.size(1) == self.input_dims
        return self.model.forward(input)

def mnist(input_dims=784, n_hiddens=[256, 256], n_class=10, pretrained=None):
    model = MLP(input_dims, n_hiddens, n_class)
    if pretrained is not None:
        pretrained = misc.expand_user(pretrained)
        if os.path.exists(pretrained):
            print("Restoring parameters from {}".format(pretrained))
            m = torch.load(pretrained)
            state_dict = m.state_dict() if isinstance(m, nn.Module) else m
            assert isinstance(state_dict, (dict, OrderedDict)), type(state_dict)
            model.load_state_dict(state_dict)
    return model
