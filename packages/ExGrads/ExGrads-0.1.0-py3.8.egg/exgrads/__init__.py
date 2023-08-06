#!/usr/bin/env python
# coding: utf-8
__version__='0.1.0'


import warnings
warnings.filterwarnings("ignore")
# Need to prevent following warning
# > UserWarning: Using a non-full backward hook when the forward contains multiple autograd Nodes is deprecated and will be removed in future versions. This hook will be missing some grad_input. Please use register_full_backward_hook to get the documented behavior.
# > warnings.warn("Using a non-full backward hook when the forward contains multiple autograd Nodes "

import torch
def _get_layer_type(layer):
	return layer.__class__.__name__
def _is_support_layer(layer):
	return _get_layer_type(layer) in {'Linear', 'Conv2d','BatchNorm2d','BatchNorm1d'}

# -------------------------------------------------------
# inputs are tuple-type. that's why inputs[0] is needed.
#  https://pytorch.org/tutorials/beginner/former_torchies/nnft_tutorial.html
def _capture_forwardprops(layer, inputs, _outputs):
	layer.forward1	= inputs[0].detach()

def _capture_backwardprops(layer, _grad_inputs, grad_outputs):
	layer.backward1	= grad_outputs[0].detach()

def add_hooks(model):
	handles = []
	for layer in model.modules():
		if _is_support_layer(layer):
			handles.append(layer.register_forward_hook(_capture_forwardprops))
			handles.append(layer.register_backward_hook(_capture_backwardprops))
	model.__dict__.setdefault('autograd_hacks_hooks', []).extend(handles)

# -------------------------------------------------------
def clear_forward1(model):
	for layer in model.modules():
		if hasattr(layer, 'forward1'):
			del layer.forward1

def clear_backword1(model):
	for layer in model.modules():
		if hasattr(layer, 'backward1'):
			del layer.backward1

def remove_hooks(model):
	clear_forward1(model)
	clear_backword1(model)
	if hasattr(model, 'autograd_hacks_hooks'):
		for handle in model.autograd_hacks_hooks:
			handle.remove()
		del model.autograd_hacks_hooks

# -------------------------------------------------------
def _compute_grad1_for_linear(layer, Fp, Bp):
	layer.weight.grad1 = torch.einsum('ni,nj->nij', Bp, Fp)
	if layer.bias is not None:
		layer.bias.grad1 = Bp

def _compute_grad1_for_conv2d(layer, Fp, Bp):
	n = Fp.shape[0]
	Fp = torch.nn.functional.unfold(Fp, layer.kernel_size, layer.dilation, layer.padding, layer.stride)
	Bp = Bp.reshape(n, -1, Fp.shape[-1])
	grad1 = torch.einsum('ijk,ilk->ijl', Bp, Fp)
	shape = [n] + list(layer.weight.shape)
	grad1 = grad1.reshape(shape)
	layer.weight.grad1 = grad1
	if layer.bias is not None:
		layer.bias.grad1 = torch.sum(Bp, dim=2)

def _compute_grad1_for_batchnorm2d(layer, Fp, Bp):
	layer.weight.grad1 = torch.sum(Fp*Bp, dim=[2,3])
	if layer.bias is not None:
		layer.bias.grad1 = torch.sum(Bp, dim=[2,3])

def _compute_grad1_for_batchnorm1d(layer, Fp, Bp):
	layer.weight.grad1 = Fp*Bp
	if layer.bias is not None:
		layer.bias.grad1 = Bp

# -------------------------------------------------------
def compute_grad1(model):
	for layer in model.modules():
		if _is_support_layer(layer):
			assert hasattr(layer, 'forward1'),	'no forward1.  run forward  after add_hooks(model)'
			assert hasattr(layer, 'backward1'),	'no backward1. run backward after add_hooks(model)'

			layer_type = _get_layer_type(layer)
			Fp = layer.forward1
			Bp = layer.backward1

			if layer_type=='Linear':
				_compute_grad1_for_linear(layer, Fp, Bp)
			if layer_type=='Conv2d':
				_compute_grad1_for_conv2d(layer, Fp, Bp)
			if layer_type=='BatchNorm2d':
				_compute_grad1_for_batchnorm2d(layer, Fp, Bp)
			if layer_type=='BatchNorm1d':
				_compute_grad1_for_batchnorm1d(layer, Fp, Bp)

# -------------------------------------------------------
