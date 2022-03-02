#!/usr/bin/python
# -*- coding: UTF-8 -*-

import torch
import torch.nn as nn
from pytorch_pretrained import BertModel, BertTokenizer

class Config(object):

    def __init__(self, dataset):
        self.model_name = 'ERNIE'
        self.train_path = dataset + '/data/train.txt'
        self.test_path = dataset + '/data/test.txt'
        self.dev_path = dataset + '/data/dev.txt'
        self.datasetpkl = dataset + '/data/dataset.pkl'
        self.class_list = [ x.strip() for x in open(dataset + '/data/class.txt').readlines()]
        self.save_path = dataset + '/saved_dict/' + self.model_name + '.ckpt'
        self.device = torch.device( 'cuda' if torch.cuda.is_available() else 'cpu')
        self.require_improvement = 1000
        self.num_classes = len(self.class_list)
        self.num_epochs = 3
        self.batch_size = 128
        self.pad_size = 32
        self.learning_rate = 1e-5
        self.bert_path = 'ERNIE_pretrain'
        self.tokenizer = BertTokenizer.from_pretrained(self.bert_path)
        self.hidden_size = 768


class Model(nn.Module):

    def __init__(self, config):
        super(Model, self).__init__()
        self.bert = BertModel.from_pretrained(config.bert_path)
        for param in self.bert.parameters():
            param.requires_grad = True
        self.fc = nn.Linear(config.hidden_size, config.num_classes)

    def forward(self, x):
        # x [ids, seq_len, mask]
        context = x[0] #对应输入的句子 shape[128,32]
        mask = x[2] #对padding部分进行mask shape[128,32]
        _, pooled = self.bert(context, attention_mask=mask, output_all_encoded_layers=False) #shape [128,768]
        out = self.fc(pooled) # shape [128,10]
        return out
