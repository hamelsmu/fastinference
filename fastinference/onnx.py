# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/03_onnx.ipynb (unless otherwise specified).

__all__ = ['fastONNX']

# Cell
from fastai2.tabular.all import *
import onnxruntime as ort

# Cell
@patch
def to_onnx(x:Learner, fname='export.onnx'):
    "Export model to `ONNX` format"
    orig_bs = x.dls[0].bs
    x.dls[0].bs=1
    dummy_inp = next(iter(x.dls[0]))
    names = inspect.getfullargspec(x.model.forward).args[1:]
    torch.onnx.export(x.model, dummy_inp[:-1], fname,
                     input_names=names, output_names=['output'])

# Cell
class fastONNX():
    "Onnx wrapper for `predict`"
    def __init__(self, fn):
        self.ort_session = ort.InferenceSession(fn)
        try:
            self.ort_session.set_providers(['CUDAExecutionProvider'])
        except:
            self.ort_session.set_providers(['CPUExecutionProvider'])

    def predict(self, *inp):
        names = [i.name for i in self.ort_session.get_inputs()]
        inps = [x.cpu().numpy() for x in inp]
        xs = {name:x for name,x in zip(names,inps)}
        outs = self.ort_session.run(None, xs)
        return outs