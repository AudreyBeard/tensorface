# tensorface

Tensorboard log interface, to make it easier to manipulate data encoded in Tensorboard logs in Python

I made this repo to more easily get at scalar data for a bunch of different neural net runs, since I wanted to gather some stats and run comparisons for different models. Hopefully you'll find it useful too! Please contribute if you're into it!

## Install:

```
git clone https://gitlab.com/AudreyBeard/tensorface
cd tensorface
pip install .
```

## Usage:

```
from tensorface import TensorFace
face = TensorFace('path/to/tensorboard/logs', True)
all_scalars_dict = face.all_scalars()
```
It's that easy!

## Reference

Original idea [here](https://stackoverflow.com/questions/41074688/how-do-you-read-tensorboard-files-programmatically)