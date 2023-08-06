#!/usr/bin/env python
# coding: utf-8
__version__='0.1.1'

import torch
def _get_module_type(module):
	return module.__class__.__name__
def _is_support_layer(module):
	return _get_module_type(module) in {'Linear', 'Conv2d','BatchNorm2d','BatchNorm1d'}

# -------------------------------------------------------
# inputs are tuple-type. that's why inputs[0] is needed.
#  https://pytorch.org/tutorials/beginner/former_torchies/nnft_tutorial.html
def _capture_forwardprops(module, inputs, _outputs):
	module.forward1		= inputs[0].detach()

def _capture_backwardprops(module, _grad_inputs, grad_outputs):
	module.backward1	= grad_outputs[0].detach()

def add_hooks(model):
	handles = []
	for module in model.modules():
		if _is_support_layer(module):
			handles.append(module.register_forward_hook(_capture_forwardprops))
			handles.append(module.register_full_backward_hook(_capture_backwardprops))
	model.__dict__.setdefault('autograd_hacks_hooks', []).extend(handles)

# -------------------------------------------------------
def clear_forward1(model):
	for module in model.modules():
		if hasattr(module, 'forward1'):
			del module.forward1

def clear_backword1(model):
	for module in model.modules():
		if hasattr(module, 'backward1'):
			del module.backward1

def remove_hooks(model):
	clear_forward1(model)
	clear_backword1(model)
	if hasattr(model, 'autograd_hacks_hooks'):
		for handle in model.autograd_hacks_hooks:
			handle.remove()
		del model.autograd_hacks_hooks

# -------------------------------------------------------
def _compute_grad1_for_linear(module, Fp, Bp):
	module.weight.grad1 = torch.einsum('ni,nj->nij', Bp, Fp)
	if module.bias is not None:
		module.bias.grad1 = Bp

def _compute_grad1_for_conv2d(module, Fp, Bp):
	n = Fp.shape[0]
	Fp = torch.nn.functional.unfold(Fp, module.kernel_size, module.dilation, module.padding, module.stride)
	Bp = Bp.reshape(n, -1, Fp.shape[-1])
	grad1 = torch.einsum('ijk,ilk->ijl', Bp, Fp)
	shape = [n] + list(module.weight.shape)
	grad1 = grad1.reshape(shape)
	module.weight.grad1 = grad1
	if module.bias is not None:
		module.bias.grad1 = torch.sum(Bp, dim=2)

def _compute_grad1_for_batchnorm2d(module, Fp, Bp):
	module.weight.grad1 = torch.sum(Fp*Bp, dim=[2,3])
	if module.bias is not None:
		module.bias.grad1 = torch.sum(Bp, dim=[2,3])

def _compute_grad1_for_batchnorm1d(module, Fp, Bp):
	module.weight.grad1 = Fp*Bp
	if module.bias is not None:
		module.bias.grad1 = Bp

# -------------------------------------------------------
def compute_grad1(model):
	for module in model.modules():
		if _is_support_layer(module):
			assert hasattr(module, 'forward1'),		'no forward1.  run forward  after add_hooks(model)'
			assert hasattr(module, 'backward1'),	'no backward1. run backward after add_hooks(model)'

			layer_type = _get_module_type(module)
			Fp = module.forward1
			Bp = module.backward1

			if layer_type=='Linear':
				_compute_grad1_for_linear(module, Fp, Bp)
			if layer_type=='Conv2d':
				_compute_grad1_for_conv2d(module, Fp, Bp)
			if layer_type=='BatchNorm2d':
				_compute_grad1_for_batchnorm2d(module, Fp, Bp)
			if layer_type=='BatchNorm1d':
				_compute_grad1_for_batchnorm1d(module, Fp, Bp)

# -------------------------------------------------------
