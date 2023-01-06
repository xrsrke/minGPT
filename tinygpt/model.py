# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/05_model.ipynb.

# %% auto 0
__all__ = ['GELU', 'CasualSelfAttention', 'forward', 'GPT']

# %% ../nbs/05_model.ipynb 3
import math

import torch
from torch import nn
import torch.nn.functional as F
from einops import rearrange

from .utils import CfgNode as CN

# %% ../nbs/05_model.ipynb 5
class GELU(nn.Module):
    def forward(self, x):
        return 0.5 * x * (1.0 + torch.tanh(math.sqrt(2.0 / math.pi) * (x + 0.044715 * torch.pow(x, 3.0))))

# %% ../nbs/05_model.ipynb 6
class CasualSelfAttention(nn.Module):
    def __init__(self, config):
        super().__init__()
        assert config.n_embd % config.n_head == 0
        
        # key, query, value projections for all heads in a batch
        self.c_attn = nn.Linear(config.n_embd, 3 * config.n_head)
        
        # output projection
        self.c_proj = nn.Linear(config.n_embd, config.n_embd)
        
        # regularization
        self.attn_dropout = nn.Dropout(config.attn_pdrop)
        self.resid_dropout = nn.Dropout(config.resid_pdrop)
        
        # causal mask to ensure that attention is
        # only applied to the left in the input sequence
        self.register_buffer(
            "bias",
            torch.tri(torch.ones(config.block_size, config.block_size))
                 .view(1, 1, config.block_size, config.block_size)
        )
        
        self.n_head = config.n_head
        self.n_embd = config.n_embd

def forward(self, x):
    B, T, C = x.size()  # batch size, sequence length, embedding dimensionality (n_embd)
    
    q, j, v = self.c_attn(x).split(self.n_embd, dim=2)

# %% ../nbs/05_model.ipynb 8
class GPT(nn.Module):
    """GPT Language Model"""
    
    @staticmethod
    def get_default_config():
        C = CN()
        # either model_type or (n_layer, n_head, n_embd) must be given in the config
        C.model_type = 'gpt'
        C.n_layer = None
        C.n_head = None
        C.n_embd = None
        # these options must be filled in externally
        C.vocab_size = None
        C.block_size = None
        # dropout hyperparameters
        C.embd_pdrop = 0.1
        C.resid_pdrop = 0.1
        C.attn_pdrop = 0.1
        return C
        
