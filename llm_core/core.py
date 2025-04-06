import torch
import torch.nn as nn
import torch.nn.functional as F
import logging

logging.basicConfig(level=logging.INFO, format='[FIONA][Mini-LLM] %(message)s')

class TransformerBlock(nn.Module):
    def __init__(self, embed_dim: int, heads: int):
        super().__init__()
        self.attn = nn.MultiheadAttention(embed_dim, heads, batch_first=True)
        self.ff = nn.Sequential(
            nn.Linear(embed_dim, embed_dim * 4),
            nn.ReLU(),
            nn.Linear(embed_dim * 4, embed_dim)
        )
        self.norm1 = nn.LayerNorm(embed_dim)
        self.norm2 = nn.LayerNorm(embed_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        B, T, C = x.size()
        mask = torch.tril(torch.ones(T, T, device=x.device)).unsqueeze(0).expand(B, -1, -1)
        attn_out, _ = self.attn(x, x, x, attn_mask=~mask.bool())
        x = self.norm1(x + attn_out)
        x = self.norm2(x + self.ff(x))
        return x

class LanguageModel(nn.Module):
    def __init__(self, vocab_size: int, embed_dim: int, n_heads: int, n_layers: int, block_size: int):
        super().__init__()
        self.token_embed = nn.Embedding(vocab_size, embed_dim)
        self.pos_embed = nn.Embedding(block_size, embed_dim)
        self.blocks = nn.Sequential(*[TransformerBlock(embed_dim, n_heads) for _ in range(n_layers)])
        self.norm = nn.LayerNorm(embed_dim)
        self.head = nn.Linear(embed_dim, vocab_size)
        self.block_size = block_size
        self.apply(self._init_weights)
        logging.info(f"Initialized LanguageModel with {n_layers} layers, {n_heads} heads, dim {embed_dim}")

    def _init_weights(self, module):
        if isinstance(module, nn.Linear):
            nn.init.kaiming_uniform_(module.weight, a=0.01)
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.Embedding):
            nn.init.normal_(module.weight, mean=0.0, std=0.02)

    def forward(self, idx: torch.Tensor, targets: torch.Tensor | None = None) -> torch.Tensor:
        B, T = idx.shape
        if T > self.block_size:
            raise ValueError(f"Input sequence length {T} exceeds block size {self.block_size}")

        token_embed = self.token_embed(idx)
        pos = torch.arange(T, device=idx.device).unsqueeze(0)
        pos_embed = self.pos_embed(pos)
        x = token_embed + pos_embed

        x = self.blocks(x)
        x = self.norm(x)
        logits = self.head(x)

        if targets is None:
            return logits
        else:
            B, T, C = logits.shape
            loss = F.cross_entropy(logits.view(B * T, C), targets.view(B * T))
            return loss
