import random
import numpy as np 
import pandas as pd
from keras.utils import Sequence
from tqdm import tqdm
import dill as pickle







class MusicDatagen(Sequence):
    def __init__(self, inputs, outputs, picker, batchsize = 32):
        self.inputs = inputs
        self.outputs = outputs
        self.picker = picker
        self.df = picker.df
        self.batchsize = batchsize
        
    def testDatagen(self):
        while True:
            indices = self.picker.testIndices[:self.batchsize]
            inputs = [dc.getSamples(self.df, indices) for dc in self.inputs]
            outputs = [dc.getSamples(self.df, indices) for dc in self.outputs]
            yield inputs, outputs
        
    def __len__(self):
        return len(self.picker.trainIndices)//self.batchsize
        
    def __getitem__(self, index):
        indices = self.picker.trainIndices[index*self.batchsize:(index+1)*self.batchsize]
        inputs = [dc.getSamples(self.df, indices) for dc in self.inputs]
        outputs = [dc.getSamples(self.df, indices) for dc in self.outputs]
        return inputs, outputs
    
    def on_epoch_end(self):
        self.picker.shuffleIndices()
    
    def save(self, fp):
        f = open(fp, "wb")
        pickle.dump(self, f)
        f.close()
    
    def encodeSamples(self, df, indices):
        if(type(indices)!=list):
            indices = [indices]

        inputs = [dc.getSamples(self.df, indices) for dc in self.inputs]
        outputs = [dc.getSamples(self.df, indices) for dc in self.outputs]
        return inputs, outputs



    @staticmethod
    def load(fp):
        f = open(fp, "rb")
        datagen = pickle.load(f)
        f.close()
        return datagen
        
        
        

###########
# PICKERS #
###########

class DatagenPicker:
    def __init__(self, df, testSize = 0.2):
        self.df = df
        self.testSize = testSize
        self.indices = self.getIndices()
        self.trainIndices, self.testIndices = self.indSplit()
        self.shuffleIndices()
        
    def getIndices(self):
        raise NotImplementedError("Must add getIndices(self) function.")

    
    def shuffleIndices(self):
        random.shuffle(self.trainIndices)
        random.shuffle(self.testIndices)

    def indSplit(self):
        nTestIndices = round(self.testSize * len(self.indices))
        return self.indices[nTestIndices:], self.indices[:nTestIndices]
    
class DeepBachPopDP(DatagenPicker):
    def __init__(self, dt, *args, **kwargs):
        self.dt = dt
        super().__init__(*args, **kwargs)
        
    def getIndices(self):
        indices = []
        previousInds = 0
        for pieceID, piece in self.df.groupby("pieceID"):
            indices.extend(list(range(previousInds+self.dt, previousInds + len(piece)-1, self.dt)))
            previousInds += len(piece) - 1
        return indices
    
###########    
# Columns #
###########

class DatagenColumn:
    def __init__(self, rowSelector, columnName, encoder, dataFunctions = []):
        self.rowSelector = rowSelector
        self.dataFunctions = dataFunctions
        self.columnName = columnName
        self.encoder = encoder

    
    def getSample(self, df, index):
        data = df.loc[self.rowSelector(index), self.columnName]
        if(type(data)==int or type(data)==str):
            data = [data]
        else:
            data = data.tolist()
        for func in self.dataFunctions:
            data = func(data)
        data = np.array([data]).reshape(-1,1)
        return self.encoder.fit_transform(data).reshape(1,-1)

    #Todo: optimize getSamples!
    def getSamples(self, df, indices):
        return np.concatenate([self.getSample(df, index) for index in indices], axis = 0)





    
    
