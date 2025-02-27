# Copyright (c) {2015 - 2021} Texas Instruments Incorporated
#
# All rights reserved not granted herein.
#
# Limited License.
#
# Texas Instruments Incorporated grants a world-wide, royalty-free, non-exclusive
# license under copyrights and patents it now or hereafter owns or controls to make,
# have made, use, import, offer to sell and sell ("Utilize") this software subject to the
# terms herein.  With respect to the foregoing patent license, such license is granted
# solely to the extent that any such patent is necessary to Utilize the software alone.
# The patent license shall not apply to any combinations which include this software,
# other than combinations with devices manufactured by or for TI ("TI Devices").
# No hardware patent is licensed hereunder.
#
# Redistributions must preserve existing copyright notices and reproduce this license
# (including the above copyright notice and the disclaimer and (if applicable) source
# code license limitations below) in the documentation and/or other materials provided
# with the distribution
#
# Redistribution and use in binary form, without modification, are permitted provided
# that the following conditions are met:
#
# *       No reverse engineering, decompilation, or disassembly of this software is
# permitted with respect to any software provided in binary form.
#
# *       any redistribution and use are licensed by TI for use only with TI Devices.
#
# *       Nothing shall obligate TI to provide you with source code for the software
# licensed and provided to you in object code.
#
# If software source code is provided to you, modification and redistribution of the
# source code are permitted provided that the following conditions are met:
#
# *       any redistribution and use of the source code, including any resulting derivative
# works, are licensed by TI for use only with TI Devices.
#
# *       any redistribution and use of any object code compiled from the source code
# and any resulting derivative works, are licensed by TI for use only with TI Devices.
#
# Neither the name of Texas Instruments Incorporated nor the names of its suppliers
#
# may be used to endorse or promote products derived from this software without
# specific prior written permission.
#
# DISCLAIMER.
#
# THIS SOFTWARE IS PROVIDED BY TI AND TI'S LICENSORS "AS IS" AND ANY EXPRESS
# OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL TI AND TI'S LICENSORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED
# OF THE POSSIBILITY OF SUCH DAMAGE.

import flatbuffers
import tflite.Model
import tflite.BuiltinOperator
import tflite.BuiltinOptions
import tflite.Tensor
import tflite.TensorType
import copy 
import struct
import argparse

def addNewOperator(modelT, operatorBuiltinCode):
    new_op_code                       = copy.deepcopy(modelT.operatorCodes[0])
    new_op_code.deprecatedBuiltinCode = operatorBuiltinCode
    modelT.operatorCodes.append(new_op_code)
    return (len(modelT.operatorCodes) - 1)

def getArgMax_idx(modelT):
    idx = 0
    for op in modelT.operatorCodes:
        if(op.deprecatedBuiltinCode == tflite.BuiltinOperator.BuiltinOperator.ARG_MAX):
            break
        idx = idx + 1
    return idx

def setTensorProperties(tensor, dataType, scale, zeroPoint):
    tensor.type                   = dataType
    tensor.quantization.scale     = [scale]
    tensor.quantization.zeroPoint = [zeroPoint]

def createTensor(modelT, dataType, quantization, tensorShape, tensorName):
    newTensor              = copy.deepcopy(modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].inputs[0]])
    newTensor.type         = dataType
    newTensor.quantization = quantization
    newTensor.shape        = tensorShape
    newTensor.name         = tensorName
    return newTensor

#Parse Basic Properties:
parser = argparse.ArgumentParser()
parser.add_argument("--model_path", type=str, default="", help="Specify the path to your tflite model to be converted")
parser.add_argument("--model_path_out", type=str, default="./convertedModel.tflite", help="Specify the name of your converted model")
parser.add_argument("--mean", type=str, default="-128.0,-128.0,-128.0",help="Specify mean values in a comma separated format. e.g.: --mean 128, 128, 128")
parser.add_argument("--scales",type=str, default="0.0078125,0.0078125,0.0078125",help="Specify scales in a comma separated format. e.g.: --scales 0.125, 0.125, 0.125")
parser.add_argument("--enableFloatInput",type=bool, default=False, help="Enable float input for your model (Surpresses addition of a dequantize node)")
args = parser.parse_args()

assert len(args.model_path) > 0, "You must specify path to your model to be converted via --model_path = <Model Path>"

#Construct scale and mean list:
scaleList = [float(scale) for scale in args.scales.split(",")]
meanList  = [float(mean) for mean in args.mean.split(",")]

#Open the tflite model
modelBin = open(args.model_path, 'rb').read()
modelBin = bytearray(modelBin)
model = tflite.Model.Model.GetRootAsModel(modelBin, 0)
modelT = tflite.Model.ModelT.InitFromObj(model)

#Add operators needed for preprocessing:
if (not args.enableFloatInput):
    setTensorProperties(modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].inputs[0]], tflite.TensorType.TensorType.UINT8, 1.0, 0)
mul_idx = addNewOperator(modelT, tflite.BuiltinOperator.BuiltinOperator.MUL)
add_idx = addNewOperator(modelT, tflite.BuiltinOperator.BuiltinOperator.ADD)
cast_idx = addNewOperator(modelT, tflite.BuiltinOperator.BuiltinOperator.CAST)

if (not args.enableFloatInput):
    dequantize_idx = addNewOperator(modelT, tflite.BuiltinOperator.BuiltinOperator.DEQUANTIZE)
#Find argmax in the network:
argMax_idx = getArgMax_idx(modelT)

#Create a tensor for the "ADD" operator:
bias_tensor = createTensor(modelT, tflite.TensorType.TensorType.FLOAT32, None, [modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].inputs[0]].shape[3]], bytearray(str("Preproc-bias"),'utf-8'))
#Create a new buffer to store mean values:
new_buffer = copy.copy(modelT.buffers[modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].inputs[0]].buffer])
new_buffer.data = struct.pack('%sf' % len(meanList), *meanList)
modelT.buffers.append(new_buffer)
new_buffer_idx = len(modelT.buffers) - 1
bias_tensor.buffer = new_buffer_idx

#Create a tensor for the "MUL" operator
scale_tensor = copy.deepcopy(bias_tensor)
scale_tensor.name  = bytearray(str("Preproc-scale"),'utf-8')
#Create a new buffer to store the scale values:
new_buffer = copy.copy(new_buffer)
new_buffer.data = struct.pack('%sf' % len(scaleList), *scaleList)
modelT.buffers.append(new_buffer)
new_buffer_idx = len(modelT.buffers) - 1
scale_tensor.buffer = new_buffer_idx

#Append tensors into the tensor list:
modelT.subgraphs[0].tensors.append(bias_tensor)
bias_tensor_idx = len(modelT.subgraphs[0].tensors) - 1 
modelT.subgraphs[0].tensors.append(scale_tensor)
scale_tensor_idx = len(modelT.subgraphs[0].tensors) - 1 
new_tensor = copy.deepcopy(modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].outputs[0]])
new_tensor.name = bytearray((str(new_tensor.name, 'utf-8') + str("/Mul")),'utf-8')
modelT.subgraphs[0].tensors.append(new_tensor)
new_tensor_idx = len(modelT.subgraphs[0].tensors) - 1 
new_buffer = copy.deepcopy(modelT.buffers[modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].outputs[0]].buffer])
modelT.buffers.append(new_buffer)
new_buffer_idx = len(modelT.buffers) - 1
modelT.subgraphs[0].tensors[new_tensor_idx].buffer = new_buffer_idx

#Add the MUL Operator for scales:
new_op = copy.deepcopy(modelT.subgraphs[0].operators[0])
modelT.subgraphs[0].operators.insert(0,new_op)
modelT.subgraphs[0].operators[0].outputs[0] = new_tensor_idx
modelT.subgraphs[0].operators[0].inputs = [modelT.subgraphs[0].operators[1].inputs[0],scale_tensor_idx]
modelT.subgraphs[0].operators[1].inputs[0] = new_tensor_idx
modelT.subgraphs[0].tensors[new_tensor_idx].shape = modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].inputs[0]].shape
modelT.subgraphs[0].operators[0].opcodeIndex = mul_idx
modelT.subgraphs[0].operators[0].builtinOptionsType = tflite.BuiltinOptions.BuiltinOptions.MulOptions
modelT.subgraphs[0].operators[0].builtinOptions = None

#Add the ADD operator for mean:
new_tensor = copy.deepcopy(modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].outputs[0]])
new_tensor.name = bytearray((str(new_tensor.name, 'utf-8') + str("/Bias")),'utf-8')
modelT.subgraphs[0].tensors.append(new_tensor)
new_tensor_idx = len(modelT.subgraphs[0].tensors) - 1 
new_buffer = copy.deepcopy(modelT.buffers[modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].outputs[0]].buffer])
modelT.buffers.append(new_buffer)
new_buffer_idx = len(modelT.buffers) - 1
modelT.subgraphs[0].tensors[new_tensor_idx].buffer = new_buffer_idx
new_op_code = copy.deepcopy(modelT.operatorCodes[0])
new_op = copy.deepcopy(modelT.subgraphs[0].operators[0])
modelT.subgraphs[0].operators.insert(0,new_op)
modelT.subgraphs[0].operators[0].outputs[0] = new_tensor_idx
modelT.subgraphs[0].operators[0].inputs = [modelT.subgraphs[0].operators[1].inputs[0],bias_tensor_idx]
modelT.subgraphs[0].operators[1].inputs[0] = new_tensor_idx
modelT.subgraphs[0].tensors[new_tensor_idx].shape = modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].inputs[0]].shape
modelT.subgraphs[0].operators[0].opcodeIndex = add_idx
modelT.subgraphs[0].operators[0].builtinOptionsType = tflite.BuiltinOptions.BuiltinOptions.AddOptions
modelT.subgraphs[0].operators[0].builtinOptions = None

#Add the dequantize operator:
if (not args.enableFloatInput):
    new_tensor = copy.deepcopy(modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].outputs[0]])
    new_tensor.name = bytearray((str(new_tensor.name, 'utf-8') + str("/Dequantize")),'utf-8')
    modelT.subgraphs[0].tensors.append(new_tensor)
    new_tensor_idx = len(modelT.subgraphs[0].tensors) - 1 
    new_buffer = copy.deepcopy(modelT.buffers[modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].outputs[0]].buffer])
    modelT.buffers.append(new_buffer)
    new_buffer_idx = len(modelT.buffers) - 1
    modelT.subgraphs[0].tensors[new_tensor_idx].buffer = new_buffer_idx
    new_op_code = copy.deepcopy(modelT.operatorCodes[0])
    new_op = copy.deepcopy(modelT.subgraphs[0].operators[0])
    modelT.subgraphs[0].operators.insert(0,new_op)
    modelT.subgraphs[0].operators[0].outputs[0] = new_tensor_idx
    modelT.subgraphs[0].operators[0].inputs = [modelT.subgraphs[0].operators[1].inputs[0]]
    modelT.subgraphs[0].operators[1].inputs[0] = new_tensor_idx
    modelT.subgraphs[0].tensors[new_tensor_idx].shape = modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[0].inputs[0]].shape
    modelT.subgraphs[0].operators[0].opcodeIndex = dequantize_idx
    modelT.subgraphs[0].operators[0].builtinOptionsType = tflite.BuiltinOptions.BuiltinOptions.DequantizeOptions
    modelT.subgraphs[0].operators[0].builtinOptions = None

#Detect and convert ArgMax's output data type:
for operator in modelT.subgraphs[0].operators:
    #Find ARGMAX:
    if(operator.opcodeIndex == argMax_idx):
        if(modelT.subgraphs[0].tensors[operator.inputs[0]].shape[3] < 256): #Change dType only if #Classes can fit in UINT8 
            #Add CAST Op on ouput of Argmax:
            new_op = copy.deepcopy(modelT.subgraphs[0].operators[0])
            modelT.subgraphs[0].operators.append(new_op)
            new_op_idx = len(modelT.subgraphs[0].operators) - 1
           
            modelT.subgraphs[0].operators[new_op_idx].outputs[0] = operator.outputs[0]

            new_tensor = copy.deepcopy(modelT.subgraphs[0].tensors[operator.outputs[0]])
            new_tensor.name = bytearray((str(new_tensor.name, 'utf-8') + str("_org")),'utf-8')
            modelT.subgraphs[0].tensors.append(new_tensor)
            new_tensor_idx = len(modelT.subgraphs[0].tensors) - 1 
            new_buffer = copy.deepcopy(modelT.buffers[modelT.subgraphs[0].tensors[operator.outputs[0]].buffer])
            modelT.buffers.append(new_buffer)
            new_buffer_idx = len(modelT.buffers) - 1
            modelT.subgraphs[0].tensors[new_tensor_idx].buffer = new_buffer_idx

            operator.outputs[0] = new_tensor_idx

            modelT.subgraphs[0].tensors[modelT.subgraphs[0].operators[new_op_idx].outputs[0]].type  = tflite.TensorType.TensorType.UINT8

            modelT.subgraphs[0].operators[new_op_idx].inputs[0] = new_tensor_idx
            modelT.subgraphs[0].operators[new_op_idx].opcodeIndex = cast_idx
            modelT.subgraphs[0].operators[new_op_idx].builtinOptionsType = tflite.BuiltinOptions.BuiltinOptions.CastOptions
            modelT.subgraphs[0].operators[new_op_idx].builtinOptions = None


# Packs the object class into another flatbuffer.
b2 = flatbuffers.Builder(0)
b2.Finish(modelT.Pack(b2), b"TFL3")
modelBuf = b2.Output() 
newFile = open(args.model_path_out, "wb")
newFile.write(modelBuf)