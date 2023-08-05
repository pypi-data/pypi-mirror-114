import torch
from typing import Union, List, Dict, Tuple, Optional, Callable
from .layers import Transformer, Embedding
from .layers import Linear, Dropout
from .layers import mask_chronological
from ._conversions import sentences_to_tensor, tensor_to_sentences
from ._conversions import floats_to_tensor
from ._neural_network_classifier import NeuralNetworkClassifier
from ._loss_functions import cross_entropy
from .layers._functional import positional_encoding
from pygmalion.unsupervised import tokenizers
from pygmalion.unsupervised.tokenizers import Tokenizer, SpecialToken
from pygmalion.utilities import document


class TraductorModule(torch.nn.Module):

    @classmethod
    def from_dump(cls, dump):
        assert cls.__name__ == dump["type"]
        obj = cls.__new__(cls)
        torch.nn.Module.__init__(obj)
        tkn = getattr(tokenizers, dump["tokenizer in"]["type"])
        obj.tokenizer_in = tkn.from_dump(dump["tokenizer in"])
        tkn = getattr(tokenizers, dump["tokenizer out"]["type"])
        obj.tokenizer_out = tkn.from_dump(dump["tokenizer out"])
        obj.embedding_in = Embedding.from_dump(dump["embedding in"])
        obj.embedding_out = Embedding.from_dump(dump["embedding out"])
        obj.dropout_in = Dropout.from_dump(dump["dropout in"])
        obj.dropout_out = Dropout.from_dump(dump["dropout out"])
        obj.transformer = Transformer.from_dump(dump["transformer"])
        obj.output = Linear.from_dump(dump["output"])
        return obj

    def __init__(self,
                 tokenizer_in: Tokenizer,
                 tokenizer_out: Tokenizer,
                 n_stages: int,
                 projection_dim: int,
                 n_heads: int,
                 max_length: Optional[int] = None,
                 activation: str = "relu",
                 dropout: Union[float, None] = None):
        """
        Parameters
        ----------
        ...
        max_length : int
            the maximum length of token sequence
            sequences bigger are dropped
        activation : str
            the default value for the 'activation' key of the kwargs
        dropout : float or None
            the default value for the 'dropout' key of the kwargs
        """
        super().__init__()
        self.max_length = max_length
        embedding_dim = projection_dim*n_heads
        self.tokenizer_in = tokenizer_in
        self.tokenizer_out = tokenizer_out
        self.embedding_in = Embedding(self.tokenizer_in.n_tokens+3,
                                      embedding_dim)
        self.embedding_out = Embedding(self.tokenizer_out.n_tokens+3,
                                       embedding_dim)
        self.dropout_in = Dropout(dropout)
        self.dropout_out = Dropout(dropout)
        self.transformer = Transformer(n_stages, projection_dim, n_heads,
                                       dropout=dropout, activation=activation)
        self.output = Linear(embedding_dim,
                             self.tokenizer_out.n_tokens+3)

    def forward(self, X):
        return self.encode(X)

    def encode(self, X):
        """
        performs the encoding part of the network

        Parameters
        ----------
        X : torch.Tensor
            tensor of longs of shape (N, L) with:
            * N : number of sentences
            * L : words per sentence

        Returns
        -------
        torch.Tensor :
            tensor of floats of shape (N, L, D) with D the embedding dimension
        """
        N, L = X.shape
        X = self.embedding_in(X)
        X = positional_encoding(X)
        X = self.dropout_in(X.reshape(N*L, -1)).reshape(N, L, -1)
        X = self.transformer.encode(X)
        return X

    def decode(self, encoded, Y):
        """
        performs the decoding part of the network

        Parameters
        ----------
        encoded : torch.Tensor
            tensor of floats of shape (N, Lx, D) with:
            * N : number of sentences
            * Lx : words per sentence in the input language
            * D : embedding dim

        Y : torch.Tensor
            tensor of long of shape (N, Ly) with:
            * N : number of sentences
            * Ly : words per sentence in the output language

        Returns
        -------
        torch.Tensor :
            tensor of floats of shape (N, Ly, D)
        """
        N, L = Y.shape
        Y = self.embedding_out(Y)
        Y = positional_encoding(Y)
        Y = self.dropout_out(Y.reshape(N*L, -1)).reshape(N, L, -1)
        mask = mask_chronological(L, L, Y.device)
        Y = self.transformer.decode(encoded, Y, mask=mask)
        return self.output(Y)

    def loss(self, encoded, y_target, weights=None):
        y_pred = self.decode(encoded, y_target[:, :-1])
        return cross_entropy(y_pred.transpose(1, 2), y_target[:, 1:],
                             weights, self.class_weights)

    def predict(self, X, max_words=100):
        n_tokens = self.tokenizer_out.n_tokens
        sentence_start = n_tokens
        sentence_end = n_tokens+1
        encoded = self(X)
        # Y is initialized as a single 'start of sentence' character
        Y = torch.full([1, 1], sentence_start,
                       dtype=torch.long, device=X.device)
        for _ in range(max_words):
            res = self.decode(encoded, Y)
            res = torch.argmax(res, dim=-1)
            index = res[:, -1:]
            Y = torch.cat([Y, index], dim=-1)
            new_token = index.item()
            if new_token == sentence_end or new_token > n_tokens:
                break
        else:
            Y = torch.cat([Y, index], dim=-1)
        return Y

    @property
    def dump(self):
        return {"type": type(self).__name__,
                "tokenizer in": self.tokenizer_in.dump,
                "tokenizer out": self.tokenizer_out.dump,
                "embedding in": self.embedding_in.dump,
                "embedding out": self.embedding_out.dump,
                "dropout in": self.dropout_in.dump,
                "dropout out": self.dropout_out.dump,
                "transformer": self.transformer.dump,
                "output": self.output.dump}


class Traductor(NeuralNetworkClassifier):

    ModuleType = TraductorModule

    @document(ModuleType.__init__, NeuralNetworkClassifier.__init__)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, sentence: str, max_words: int = 100):
        self.module.eval()
        x, _, _ = self._data_to_tensor([sentence], None, None,
                                       device=self.device)
        y = self.module.predict(x, max_words=max_words)
        return self._tensor_to_y(y)[0]

    def _data_to_tensor(self, X: List[str],
                        Y: Union[None, List[str]],
                        weights: None = None,
                        device: torch.device = torch.device("cpu")) -> tuple:
        if X is not None:
            x = sentences_to_tensor(X, self.module.tokenizer_in, device,
                                    max_sequence_length=self.module.max_length)
        else:
            x = None
        if Y is not None:
            y = sentences_to_tensor(Y, self.module.tokenizer_out, device,
                                    max_sequence_length=self.module.max_length)
        else:
            y = None
        w = None if weights is None else floats_to_tensor(weights, device)
        return x, y, w

    def _tensor_to_y(self, tensor: torch.Tensor) -> List[str]:
        return tensor_to_sentences(tensor, self.module.tokenizer_out)

    def _batch_generator(self, training_data: Tuple,
                         validation_data: Optional[Tuple],
                         batch_size: Optional[int], n_batches: Optional[int],
                         device: torch.device, shuffle: bool = True
                         ) -> Tuple[Callable, Callable]:
        if self.module.tokenizer_in.jit:
            generator = self._jit_generator
        else:
            generator = self._static_generator
        training = self._as_generator(training_data, generator,
                                      batch_size, n_batches, device, shuffle)
        val = self._as_generator(validation_data, self._static_generator,
                                 batch_size, n_batches, device, shuffle)
        return training, val

    @property
    def classes(self):
        start = SpecialToken("START")
        end = SpecialToken("END")
        pad = SpecialToken("PAD")
        return list(self.module.tokenizer_out.vocabulary) + [start, end, pad]

    @property
    def class_weights(self):
        return super().class_weights

    @class_weights.setter
    def class_weights(self, other: Union[Dict[object, float], None]):
        pad = SpecialToken("PAD")
        if other is not None:
            other[pad] = 0.
        else:
            other = {pad: 0.}
        NeuralNetworkClassifier.class_weights.fset(self, other)
