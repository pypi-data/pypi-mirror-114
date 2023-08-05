#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

"""
Test agent which overrides the `get_prefix_tokens` function for Transformer
Generator Agent in order to test its functionality.

All text generated by this agent should begin with '4 3 2 1 '.
"""
import torch
from typing import Optional

from parlai.agents.transformer.transformer import TransformerGeneratorAgent
from parlai.core.torch_agent import Batch


PREFIX_TEXT = '4 3 2 1'


class TransformerGeneratorPrefixAgent(TransformerGeneratorAgent):
    def get_prefix_tokens(self, batch: Batch) -> Optional[torch.LongTensor]:
        bsz = batch.batchsize
        dev = batch.text_vec.device
        prefix_toks = self.dict.txt2vec(PREFIX_TEXT)
        prefix_toks_batch = [prefix_toks for _ in range(bsz)]
        return torch.LongTensor(prefix_toks_batch).to(dev)
