import torch
from typing import Union, List, Dict, Tuple, Optional, Callable
from .layers import TransformerEncoder, Embedding
from .layers import Linear, Pooling1d, Dropout
from ._conversions import sentences_to_tensor, tensor_to_classes
from ._conversions import floats_to_tensor, classes_to_tensor
from ._neural_network_classifier import NeuralNetworkClassifier
from ._loss_functions import cross_entropy
from .layers._functional import positional_encoding
from pygmalion.unsupervised import tokenizers
from pygmalion.unsupervised.tokenizers import Tokenizer, SpecialToken
from pygmalion.utilities import document


class TextClassifierModule(torch.nn.Module):

    @classmethod
    def from_dump(cls, dump):
        assert cls.__name__ == dump["type"]
        obj = cls.__new__(cls)
        torch.nn.Module.__init__(obj)
        obj.classes = dump["classes"]
        obj.max_length = dump["max length"]
        tkn = getattr(tokenizers, dump["tokenizer"]["type"])
        obj.tokenizer = tkn.from_dump(dump["tokenizer"])
        obj.embedding = Embedding.from_dump(dump["embedding"])
        obj.dropout = Dropout.from_dump(dump["dropout"])
        obj.transformer_encoder = TransformerEncoder.from_dump(
            dump["transformer encoder"])
        obj.pooling = Pooling1d.from_dump(dump["pooling"])
        obj.output = Linear.from_dump(dump["output"])
        return obj

    def __init__(self,
                 tokenizer: Tokenizer,
                 classes: List[str],
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
        """
        super().__init__()
        self.classes = list(classes)
        self.max_length = max_length
        embedding_dim = projection_dim*n_heads
        self.tokenizer = tokenizer
        self.embedding = Embedding(self.tokenizer.n_tokens+3,
                                   embedding_dim)
        self.dropout = Dropout(dropout)
        self.transformer_encoder = TransformerEncoder(n_stages, projection_dim,
                                                      n_heads, dropout=dropout,
                                                      activation=activation)
        self.pooling = Pooling1d(None)
        self.output = Linear(embedding_dim,
                             len(self.classes))

    def forward(self, X):
        N, L = X.shape
        X = self.embedding(X)
        X = positional_encoding(X)
        X = self.dropout(X.reshape(N*L, -1)).reshape(N, L, -1)
        X = self.transformer_encoder(X)
        X = self.pooling(X.transpose(1, 2))
        X = self.output(X)
        return X

    def loss(self, y_pred, y_target, weights=None):
        return cross_entropy(y_pred, y_target,
                             weights, self.class_weights)

    @property
    def dump(self):
        return {"type": type(self).__name__,
                "classes": self.classes,
                "max length": self.max_length,
                "tokenizer": self.tokenizer.dump,
                "embedding": self.embedding.dump,
                "dropout": self.dropout.dump,
                "transformer encoder": self.transformer_encoder.dump,
                "pooling": self.pooling.dump,
                "output": self.output.dump}


class TextClassifier(NeuralNetworkClassifier):

    ModuleType = TextClassifierModule

    @document(ModuleType.__init__, NeuralNetworkClassifier.__init__)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _data_to_tensor(self, X: List[str],
                        Y: Union[None, List[str]],
                        weights: None = None,
                        device: torch.device = torch.device("cpu")) -> tuple:
        if X is not None:
            x = sentences_to_tensor(X, self.module.tokenizer, device,
                                    max_sequence_length=self.module.max_length)
        else:
            x = None
        if Y is not None:
            y = None if Y is None else classes_to_tensor(Y, self.classes,
                                                        device)
        else:
            y = None
        w = None if weights is None else floats_to_tensor(weights, device)
        return x, y, w

    def _tensor_to_y(self, tensor: torch.Tensor) -> List[str]:
        return tensor_to_classes(tensor, self.module.classes)

    def _batch_generator(self, training_data: Tuple,
                         validation_data: Optional[Tuple],
                         batch_size: Optional[int], n_batches: Optional[int],
                         device: torch.device, shuffle: bool = True
                         ) -> Tuple[Callable, Callable]:
        if self.module.tokenizer.jit:
            generator = self._jit_generator
        else:
            generator = self._static_generator
        training = self._as_generator(training_data, generator,
                                      batch_size, n_batches, device, shuffle)
        val = self._as_generator(validation_data, self._static_generator,
                                 batch_size, n_batches, device, shuffle)
        return training, val

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
