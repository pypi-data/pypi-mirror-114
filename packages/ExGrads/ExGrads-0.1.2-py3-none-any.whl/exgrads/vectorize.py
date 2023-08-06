#!/usr/bin/env python
# coding: utf-8

__version__='0.1.2'
import torch

#refered : SOURCE CODE FOR TORCH.NN.UTILS.CONVERT_PARAMETERS
# https://pytorch.org/docs/stable/_modules/torch/nn/utils/convert_parameters.html#parameters_to_vector
# -------------------------------------------------------
def grad(model):
	vectors = []
	for param in model.parameters():
		assert hasattr(param, 'grad'), 'something wrong. please check all parameters has grad'
		vectors.append(param.grad.flatten())
	return torch.cat(vectors)
	
# -------------------------------------------------------
def grad1(model):
	vectors = []
	for param in model.parameters():
		assert hasattr(param, 'grad1'), 'something wrong. please check all parameters has grad1'
		grad1 = param.grad1.detach()
		grad1 = grad1.flatten(1,-1)
		vectors.append(grad1)
	return torch.cat(vectors,dim=1)

# -------------------------------------------------------

