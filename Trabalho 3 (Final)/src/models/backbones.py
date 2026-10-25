"""
Backbones Convolucionais Customizados para GMIC
- ResNet-22 Global: Otimizada para Mamografias de Alta Resolução Preservando Resolução Espacial
- ResNet-18 Local: Otimizada para Patches de Alta Resolução Extraídos Localmente
"""

import math

try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
except ImportError:
    torch = None
    nn = object
    F = None


def conv3x3(in_planes, out_planes, stride=1):
    """Convolução 3x3 com padding de preservação dimensional"""
    return nn.Conv2d(in_planes, out_planes, kernel_size=3, stride=stride, padding=1, bias=False)


class BasicBlock(nn.Module if torch else object):
    """
    Bloco Residual Padrão com conexões de atalho (Skip Connection)
    """
    expansion = 1

    def __init__(self, inplanes, planes, stride=1, downsample=None):
        super().__init__()
        self.conv1 = conv3x3(inplanes, planes, stride)
        self.bn1 = nn.BatchNorm2d(planes)
        self.relu = nn.ReLU(inplace=True)
        self.conv2 = conv3x3(planes, planes)
        self.bn2 = nn.BatchNorm2d(planes)
        self.downsample = downsample
        self.stride = stride

    def forward(self, x):
        residual = x

        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)

        out = self.conv2(out)
        out = self.bn2(out)

        if self.downsample is not None:
            residual = self.downsample(x)

        out += residual
        out = self.relu(out)

        return out


class ResNet22Global(nn.Module if torch else object):
    """
    ResNet-22 Global Customizada (Shen et al., 2021 / Sampaio & Cordeiro, 2022).
    Projetada para mamografias de entrada de canal único (tons de cinza).
    Retorna o tensor espacial de características convolutivas S_g e o vetor global h_global.
    """
    def __init__(self, in_channels: int = 1, out_features: int = 512):
        super().__init__()
        self.inplanes = 64
        
        # Camada Convolucional Inicial adaptada para 1 canal (mamografia)
        self.conv1 = nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # 4 Estágios Residuais (Total de camadas conv = 1 + 2*(2+3+3+2) + 1 = 22 camadas)
        self.layer1 = self._make_layer(BasicBlock, 64, blocks=2, stride=1)
        self.layer2 = self._make_layer(BasicBlock, 128, blocks=3, stride=2)
        self.layer3 = self._make_layer(BasicBlock, 256, blocks=3, stride=2)
        self.layer4 = self._make_layer(BasicBlock, out_features, blocks=2, stride=2)

        # Global Average Pooling para geração do vetor de características global
        self.gap = nn.AdaptiveAvgPool2d((1, 1))

        # Inicialização Kaiming Normal
        self._initialize_weights()

    def _make_layer(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes * block.expansion),
            )

        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample))
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # x: [Batch, 1, H, W]
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        feat_map = self.layer4(x) # S_g: [Batch, 512, H_g, W_g]

        h_global = self.gap(feat_map) # [Batch, 512, 1, 1]
        h_global = torch.flatten(h_global, 1) # [Batch, 512]

        return feat_map, h_global


class ResNet18Local(nn.Module if torch else object):
    """
    ResNet-18 Local Customizada para Patches de Alta Resolução (256 x 256).
    Recebe patches locais em tons de cinza e extrai representações
    convolucionais detalhadas para agregação de múltiplas instâncias (MIL).
    """
    def __init__(self, in_channels: int = 1, out_features: int = 512):
        super().__init__()
        self.inplanes = 64

        self.conv1 = nn.Conv2d(in_channels, 64, kernel_size=7, stride=2, padding=3, bias=False)
        self.bn1 = nn.BatchNorm2d(64)
        self.relu = nn.ReLU(inplace=True)
        self.maxpool = nn.MaxPool2d(kernel_size=3, stride=2, padding=1)

        # 4 Estágios Residuais da ResNet-18 (2 blocos cada)
        self.layer1 = self._make_layer(BasicBlock, 64, blocks=2, stride=1)
        self.layer2 = self._make_layer(BasicBlock, 128, blocks=2, stride=2)
        self.layer3 = self._make_layer(BasicBlock, 256, blocks=2, stride=2)
        self.layer4 = self._make_layer(BasicBlock, out_features, blocks=2, stride=2)

        self.gap = nn.AdaptiveAvgPool2d((1, 1))
        self._initialize_weights()

    def _make_layer(self, block, planes, blocks, stride=1):
        downsample = None
        if stride != 1 or self.inplanes != planes * block.expansion:
            downsample = nn.Sequential(
                nn.Conv2d(self.inplanes, planes * block.expansion, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(planes * block.expansion),
            )

        layers = []
        layers.append(block(self.inplanes, planes, stride, downsample))
        self.inplanes = planes * block.expansion
        for _ in range(1, blocks):
            layers.append(block(self.inplanes, planes))

        return nn.Sequential(*layers)

    def _initialize_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                nn.init.kaiming_normal_(m.weight, mode='fan_out', nonlinearity='relu')
            elif isinstance(m, nn.BatchNorm2d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def forward(self, x):
        # x: [Batch * K, 1, Patch_Size, Patch_Size]
        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)
        x = self.maxpool(x)

        x = self.layer1(x)
        x = self.layer2(x)
        x = self.layer3(x)
        x = self.layer4(x)

        h_local = self.gap(x)
        h_local = torch.flatten(h_local, 1) # [Batch * K, 512]

        return h_local
