import os
from argparse import ArgumentParser
import re

import numpy as np
import pandas as pd

import transformers

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, RandomSampler, SequentialSampler, BatchSampler

import utils
import brands

class SimpleBatchDataLoader:
    def __init__(self, dataset, shuffle=True, drop_last=False, batch_size=8):
        self.dataset = dataset
        if shuffle:
            self.sampler = RandomSampler(dataset)
        else:
            self.sampler = SequentialSampler(dataset)

        self.batch_sampler = BatchSampler(self.sampler, drop_last=drop_last, batch_size=batch_size)

    def __len__(self):
        return len(self.batch_sampler)

    def __iter__(self):
        for batch_idx in self.batch_sampler:
            yield self.dataset[batch_idx]


class DatasetForTokenizedSentimentClassification(torch.utils.data.Dataset):
    def __init__(
        self,
        texts,
        args=None,
        idx2sentiment=None,
        brand2sentiment=None,
    ):
        self.hparams = args
        self.texts = texts
        self.brand2sentiment = brand2sentiment
        self.idx2sentiment = idx2sentiment
        self.tokenizer = transformers.AutoTokenizer.from_pretrained("ganeshkharad/gk-hinglish-sentiment")

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):

        texts = [self.texts[idxi] for idxi in idx]
        
        if self.brand2sentiment is not None:
            brand2sentiment = [self.brand2sentiment[idxi] for idxi in idx]
            return self.preprocess_batch(texts, brand2sentiment)
        
        elif self.idx2sentiment is not None:
            idx2sentiment = [self.idx2sentiment[idxi] for idxi in idx]
            split_texts = texts
            batch = self.tokenizer(
                split_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors='pt',
                is_split_into_words=True,
            )
            
            labels = []
            for i in range(len(texts)):
                word_ids = batch.word_ids(batch_index=i)
                label = [idx2sentiment[i][idx] if idx is not None else -100 for idx in word_ids]
                labels.append(label)
            batch["labels"] = torch.tensor(labels, dtype=torch.long)
            return batch
        
        else:
            # raise Exception("Neither idx2sentiment or brand2sentiment were provided")
            brands_found = brands.get_brands(texts)
            split_texts = [re.findall(r"[\w]+|[^\s\w]", text) for text in texts]
            batch = self.tokenizer(
                split_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors='pt',
                is_split_into_words=True,
            )
            batch['brands'] = brands_found
            return batch
            

    def preprocess_batch(self, texts, brand2sentiment):
        """
        texts: List of strings
        brand2sentiment: List of Dicts
        """
        brand2idx = brands.get_brand_indices(texts)
        # brand2idx: List of Dicts
        split_texts = [re.findall(r"[\w]+|[^\s\w]", text) for text in texts]
        batch = self.tokenizer(
            split_texts,
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors='pt',
            is_split_into_words=True,
        )

        labels = []
        for i in range(len(texts)):
            idx2sentiment = {}
            for brand, idxs in brand2idx[i].items():
                for idx in idxs:
                    idx2sentiment[idx] = brand2sentiment[i].get(brand, -100)

            word_ids = batch.word_ids(batch_index=i)
            label = [idx2sentiment.get(idx, -100) for idx in word_ids]
            labels.append(label)

        batch["labels"] = torch.tensor(labels, dtype=torch.long)
        return batch

class TokenClassifier(torch.nn.Module):
    def __init__(self, model, for_inference):
        super().__init__()

        self.base = model.bert
        self.dropout = model.dropout
        self.clf = model.classifier
        self.for_inference = for_inference
    
    @staticmethod
    def loss_fn(inp, ytrue):
        ce = torch.nn.CrossEntropyLoss(weight=torch.tensor([0.,1.,1.], device=inp.device))
        return ce(inp,ytrue)    

    def forward(self, batch, **kwargs):
        out = self.base(
            input_ids=batch['input_ids'],
            attention_mask=batch['attention_mask'],
            token_type_ids=batch.get('token_type_ids', None),
        )
        out = self.dropout(out['last_hidden_state'])
        out = self.clf(out)
        if not self.for_inference:
            loss = self.loss_fn(out.view(-1,3), batch['labels'].view(-1))
        else:
            loss=0
        return {'loss':loss, 'logits':out}

if __name__ == '__main__':
    gk_model = transformers.AutoModelForSequenceClassification.from_pretrained('ganeshkharad/gk-hinglish-sentiment', num_labels=3)
    model = TokenClassifier(gk_model)
