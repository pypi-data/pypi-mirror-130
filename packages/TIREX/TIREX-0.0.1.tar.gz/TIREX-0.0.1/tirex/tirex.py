#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  7 15:56:12 2021

@author: anass
"""
from sklearn.base import BaseEstimator,TransformerMixin
import numpy as np
from scipy.linalg import sqrtm,pinvh
from sklearn.decomposition import PCA

class TIREX(BaseEstimator,TransformerMixin):
    def __init__(self,n_components,k=None,method="SFO",mode="SIREX"):
        """ -------------------------Parameters-----------------------------
            -k : integer in [1,X.shape[0]] to define the treshold used in SIREX estimates 
            
            -dim : the number of components to keep
            
            -method={SFO,SSO} : 
                if method = SFO: use First order estimates C_n
                if method = SSO : use Second order estimates B_n
                
        ------------------------Attributes------------------------------
            -M_n : the matrix M_n from SIREX
            
            -Centrale_space : Return the components nu of the extreme central space E_c , 
            Note that E_c is the centrale space for the standardized version of X (Z) 
            
            -independent_column: The columns that are linearly independent 
                             """
        self.k=k
        self.dim=n_components
        self.method=method
        self.M_n=None
        self.CentralSpace= None
        self.Whiten=PCA(whiten=True)
        self.independent_column=None
        self.mode=mode
    def fit(self,X,y):
        if self.mode=="CUME":
            self.k=X.shape[0]
        if X.shape[0]!=y.shape[0]:
            print("X and y must have the same lenght")
            return self
        elif self.k>X.shape[0]:
            print("Select a proper value of k : the treshold must be smaller than the lenght of the dataframe ")
            return self
        elif self.k<=0:
            print("the parameter k must be a strictly positive integer")
        else:
                print("-----Removing linearly dependent columns from the covariance matrix-----")
                first_cov=np.cov(X.T)
                    
                q,r = np.linalg.qr(first_cov) #qr decomposition
                self.independent_column=[i for i in range(len(first_cov)) if (first_cov[i,i]>0 and abs(r[i,i])>1e-7)]
                X_f=X[:,self.independent_column]
               
                #SIREX algo
                n=X_f.shape[0]
                p=X_f.shape[1]
                
                if self.mode=="SIREX":
                    Y=-y 
                else:
                    Y=y
               
                sorted_X=(X_f[Y.argsort()])
                

                sorted_Z=self.Whiten.fit_transform(sorted_X)
                
                Sum_func=lambda x: np.matmul(x.reshape(-1,1),x.reshape(-1,1).T)*(1/self.k)
                Sum_func_SO=lambda x: np.matmul(x,x.T)*(1/self.k)
                
                if self.method=="SFO":
                    cumsum=np.cumsum(sorted_Z[:self.k,:],axis=0)
                    Sum_terms=np.apply_along_axis(Sum_func,-1,cumsum)
                    Sum=np.sum(Sum_terms,axis=0)
                    self.M_n=Sum/(self.k**2)
                    
                if self.method=="SSO":
                    
                    SSO_func=lambda x : (np.identity(p)-np.matmul(np.array(x.reshape(-1,1)),np.array(x.reshape(-1,1)).T))
                    B= np.apply_along_axis(SSO_func,-1,sorted_Z[:self.k,:])   
                    cumsum=np.cumsum(B[:self.k,:],axis=0)
                    Sum_terms=np.matmul(cumsum,cumsum.transpose((0, 2, 1)))/(self.k)
                    Sum=np.sum(Sum_terms,axis=0)     
                    Sum_func_SO=lambda x: np.matmul(x,x.T)*(1/self.k)
           
                    self.M_n= (Sum/(self.k**2))
            
                w,v=np.linalg.eigh(self.M_n)
                extreme_space=np.zeros((p,self.dim))
                w_cop,v_cop=np.absolute(w)/np.sqrt(np.sum(w**2)),v
                
                if p>=self.dim:
                    extreme_space= v_cop[:,((-w_cop).argsort())[:self.dim]]
                    self.CentralSpace= extreme_space
                else:
                    print("Select a proper value of dim")
                    return self
                                       
                                    
                return self
            
    def transform(self,X):
        X_cop=X[:,self.independent_column]
        Z=self.Whiten.transform(X_cop)
        return np.matmul(Z,self.CentralSpace)