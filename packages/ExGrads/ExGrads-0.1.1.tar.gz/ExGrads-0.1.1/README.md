this repository is still under construction (2021/07/21)


ExGrads
===
This repository provides a hook script: calculating Example-wise Gradients efficiently.


Note
---
This script use [the work](https://github.com/cybertronai/autograd-hacks) as an important reference.\
I think it is the great first step to handle per-example gradients efficiently.\
I'd like to express my respect for the step.


Features of This Script
----
+ Calculate example-wise gradient efficiently\
	There is no method calculating Hessian in contrast to [the referenced work](https://github.com/cybertronai/autograd-hacks).
+ Handle general modules\
	Including Linear, Conv2d, BatchNorm2d, and BatchNorm1d. More modules will be added soon.
+ How to use this script in practice
	1. 	[Fast and Exact calculating $`\text{tr}[\bold{H}]`$](https://gitlab.com/takuo-h/fast-exact-trh)
	2. other usages (comming soon in a month, I hope)
+ Less memory mode (WIP)

How to Use
----
```python
import torch
import exgrads as ExGrads

batch,dim,label = 5,3,2
x = torch.randn(batch,dim)                                  #: inputs
y = torch.randint(low=0,high=label-1,size=(batch,))         #: outputs
model   = torch.nn.Sequential(torch.nn.Linear(dim, label))  #: PyTorch model
loss_fn = torch.nn.functional.cross_entropy                 #: loss function

ExGrads.add_hooks(model)
model.zero_grad()
loss_fn(model(x), y).backward()
ExGrads.compute_grad1(model)

# param.grad:     gradient averaged over the batch
# param.grad1[i]: gradient of i-th example
for param in model.parameters():
	assert(torch.allclose(param.grad1.sum(dim=0), param.grad))
```
