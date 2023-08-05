# Bug with PyTorch source code makes torch.tensor as not callable for pylint.
# We also skip protected-access since we test the encoder and decoder step
# pylint: disable=not-callable, protected-access
import os
import unittest
from unittest import skipIf

import torch

from deepparse.network import FastTextSeq2SeqModel
from ..integration.base import Seq2SeqIntegrationTestCase


@skipIf(not torch.cuda.is_available(), "no gpu available")
class FastTextSeq2SeqIntegrationTest(Seq2SeqIntegrationTestCase):

    @classmethod
    def setUpClass(cls):
        super(FastTextSeq2SeqIntegrationTest, cls).setUpClass()
        cls.models_setup(model="fasttext")
        cls.a_retrain_model_path = os.path.join(cls.path, cls.retrain_file_name_format.format("fasttext") + ".ckpt")

    def setUp(self) -> None:
        super().setUp()
        # will load the weights if not local
        self.encoder_input_setUp("fasttext", self.a_torch_device)

        self.a_target_vector = torch.tensor([[0, 1, 1, 4, 5, 8], [1, 0, 3, 8, 0, 0]], device=self.a_torch_device)

    def test_whenForwardStep_thenStepIsOk(self):
        self.seq2seq_model = FastTextSeq2SeqModel(self.a_torch_device, self.number_of_tags)
        # forward pass for two address: '['15 major st london ontario n5z1e1', '15 major st london ontario n5z1e1']'
        self.decoder_input_setUp()

        predictions = self.seq2seq_model.forward(self.to_predict_tensor, self.a_lengths_tensor)

        self.assert_output_is_valid_dim(predictions, output_dim=self.number_of_tags)

    def test_whenForwardStepWithTarget_thenStepIsOk(self):
        self.seq2seq_model = FastTextSeq2SeqModel(self.a_torch_device, self.number_of_tags)
        # forward pass for two address: '['15 major st london ontario n5z1e1', '15 major st london ontario n5z1e1']'
        self.decoder_input_setUp()

        predictions = self.seq2seq_model.forward(self.to_predict_tensor, self.a_lengths_tensor, self.a_target_vector)

        self.assert_output_is_valid_dim(predictions, output_dim=self.number_of_tags)

    def test_retrainedModel_whenForwardStep_thenStepIsOk(self):
        self.seq2seq_model = FastTextSeq2SeqModel(self.a_torch_device,
                                                  self.re_trained_output_dim,
                                                  self.verbose,
                                                  path_to_retrained_model=self.a_retrain_model_path)
        # forward pass for two address: '['15 major st london ontario n5z1e1', '15 major st london ontario n5z1e1']'
        self.decoder_input_setUp()

        predictions = self.seq2seq_model.forward(self.to_predict_tensor, self.a_lengths_tensor)

        self.assert_output_is_valid_dim(predictions, output_dim=self.re_trained_output_dim)

    def test_retrainedModel_whenForwardStepWithTarget_thenStepIsOk(self):
        self.seq2seq_model = FastTextSeq2SeqModel(self.a_torch_device,
                                                  self.re_trained_output_dim,
                                                  self.verbose,
                                                  path_to_retrained_model=self.a_retrain_model_path)
        # forward pass for two address: '['15 major st london ontario n5z1e1', '15 major st london ontario n5z1e1']'
        self.decoder_input_setUp()

        predictions = self.seq2seq_model.forward(self.to_predict_tensor, self.a_lengths_tensor, self.a_target_vector)

        self.assert_output_is_valid_dim(predictions, output_dim=self.re_trained_output_dim)


if __name__ == "__main__":
    unittest.main()
