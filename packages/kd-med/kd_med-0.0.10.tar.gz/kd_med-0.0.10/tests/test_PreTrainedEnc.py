# -*- coding: utf-8 -*-
# @Time    : 7/28/21 3:23 PM
# @Author  : Jingnan
# @Email   : jiajingnan2222@gmail.com
import unittest
import tempfile
import os
import torch
import torch.nn as nn

from parameterized import parameterized
from kd_med.pre_trained_enc import pre_trained_enc
from kd_med import resnet3d
from kd_med.unet3d import UNet3D

import numpy as np


TEST_CASE_1 = ["resnet3d_10", resnet3d.resnet10(shortcut_type='B', num_seg_classes=99)]
TEST_CASE_2 = ["resnet3d_18", resnet3d.resnet18(shortcut_type='A', num_seg_classes=99)]
TEST_CASE_3 = ["resnet3d_34", resnet3d.resnet34(shortcut_type='A', num_seg_classes=99)]
TEST_CASE_4 = ["resnet3d_50", resnet3d.resnet50(shortcut_type='B', num_seg_classes=99)]
TEST_CASE_5 = ["resnet3d_101", resnet3d.resnet101(shortcut_type='B', num_seg_classes=99)]
TEST_CASE_6 = ["resnet3d_152", resnet3d.resnet152(shortcut_type='B', num_seg_classes=99)]
TEST_CASE_7 = ["resnet3d_200", resnet3d.resnet200(shortcut_type='B', num_seg_classes=99)]
TEST_CASE_8 = ["unet3d", UNet3D()]


class Testpre_trained_enc(unittest.TestCase):
    @parameterized.expand([TEST_CASE_1, TEST_CASE_2, TEST_CASE_3, TEST_CASE_4,
                           TEST_CASE_5, TEST_CASE_6, TEST_CASE_7, TEST_CASE_8])
    def test_pre_trained_enc(self, net_name, expected_net):
        net = pre_trained_enc(net_name)
        layer_names = [name for name, param in net.named_parameters()]
        expected_names = [name for name, param in expected_net.named_parameters()]
        self.assertEqual(layer_names, expected_names)

    @parameterized.expand([TEST_CASE_1, TEST_CASE_2, TEST_CASE_3, TEST_CASE_4,
                           TEST_CASE_5, TEST_CASE_6, TEST_CASE_7, TEST_CASE_8])
    def test_pre_trained_enc_same_weights(self, net_name, expected_net):
        net1 = pre_trained_enc(net_name)
        net2 = pre_trained_enc(net_name)
        net3 = pre_trained_enc(net_name)
        self.assertIsNot(net1, net2)
        self.assertIsNot(net1, net3)


if __name__ == "__main__":
    unittest.main()
