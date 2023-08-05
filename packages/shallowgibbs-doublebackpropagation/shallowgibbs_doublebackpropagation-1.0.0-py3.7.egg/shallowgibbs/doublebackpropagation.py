import pandas as pd
import random
import numpy as np
from numpy import linalg as LA
import argparse
import csv
from joblib import Parallel, delayed
import multiprocessing
import math


import tensorflow as tf
from scipy.stats import invwishart
from scipy.optimize import minimize_scalar
from numpy.linalg import LinAlgError
from scipy.stats import invwishart
import sklearn.datasets as SD
import numpy as np
import math


##################################################################################### COPULE DATA ###################################################################################

global Znear_psd
def Znear_psd(x, epsilon=0):
        
    
    '''
    Calculates the nearest postive semi-definite matrix for a correlation/covariance matrix

    Parameters
    ----------
    x : array_like
      Covariance/correlation matrix
    epsilon : float
      Eigenvalue limit (usually set to zero to ensure positive definiteness)

    Returns
    -------
    near_cov : array_like
      closest positive definite covariance/correlation matrix

    Notes
    -----
    Document source
    http://www.quarchome.org/correlationmatrix.pdf

    '''

    xtemp = x
    minxtemp = min(np.linalg.eigvals(xtemp)) 
    
    if float(minxtemp) > 0 and np.all(xtemp == np.transpose(x)) :
        return x
    #Compute S
    
    S = 0.5*(x + np.transpose(x))#np.matmul(x, np.transpose(x))
    
    # getting the eigen values
    eigval_S, eigvec_S = np.linalg.eig(S)
    
    def optimize_S (a):

        new_eigval_S = np.where(eigval_S >= 0, eigval_S, a)

        new_S = np.matmul(np.matmul(eigvec_S, np.diag(new_eigval_S)),np.transpose(eigvec_S))

        return np.linalg.norm(S-new_S)
    
    res = minimize_scalar(optimize_S, method='bounded', bounds=(30, 10e100))
    print("My res.x", res.x)
    
    valide_new_eigval_S = np.where(eigval_S >= 0, eigval_S, res.x) 
    
    valide_S = np.matmul(np.matmul(eigvec_S, np.diag(valide_new_eigval_S)),np.transpose(eigvec_S))
    print("http://www.quarchome.org/correlationmatrix.pdf")
    print("http://www.quarchome.org/correlationmatrix.pdf")
    print("http://www.quarchome.org/correlationmatrix.pdf")
    print("http://www.quarchome.org/correlationmatrix.pdf")
    print("http://www.quarchome.org/correlationmatrix.pdf")
    frd = np.linalg.cholesky(valide_S) #print("http://www.quarchome.org/correlationmatrix.pdf")
    print("new near_cov, done#")
    print("Oops!  Random Initialisation in training does'nt fit.  Try again..BOOMBOOM.BOOMBOOMBOOMBOOMBOOMBOOMBOOMBOOMBOOMBOOM")
    return valide_S

global myg_1_function
def myg_1_function(a):
    return tf.reshape(tf.tanh(a), a.shape)

global myg_1_function_diff
def myg_1_function_diff(a):
    return tf.reshape( tf.tanh(a), a.shape )

global obtain_choleski_factor_for_Sigma
def obtain_choleski_factor_for_Sigma (My_Sigma):

    Near_Sigma = Znear_psd(My_Sigma, epsilon=0.1)
    x_dim = Near_Sigma.shape[1]        #la dimension de x
    
    """ Q must be semi-positive definite , or you'll get errors """
    
    
    Near_L = np.linalg.cholesky(Near_Sigma) #Cholesky de Q pour avoir L

    return Near_L 

def Double_Backpropagated_predictions (Cluster_ytrain_prediction, Cluster_ytest_prediction, W,b,Sigma, double_backpropagation_time, l_1, Cluster_xtrain,Cluster_ytrain,Cluster_xtest,Cluster_ytest,dbs_epsilon):


    x_ = Cluster_xtrain
    y_ = Cluster_ytrain
    
    xtest_ = Cluster_xtest
    ytest_ = Cluster_ytest

    l_0 = Cluster_xtrain.shape[1]#3
    l_1 = l_1
    l_2 = Cluster_ytrain.shape[1]#2
    
    lb_0 = l_1 #2, (must be equal to l_1)
    lb_1 = l_2 #2, (must be equal to l_2)
    
    print("DOUBLE BACKPROPAGATED GRANDEUR### Etape00000")
    y_test_prediction = []
    SPNNR_test_rmse = []

    # INTIALISATIONS
        
    #init = tf.initialize_all_variables()
    sess = tf.Session()
    #sess.run(init)

    #number of samples per parameters
    exp_time1 = Double_Backpropagated_exp_time1 = int(double_backpropagation_time)

    #number of samples per yi
    exp_time2 = Double_Backpropagated_exp_time2 = int(double_backpropagation_time)

    #stack1 = np.zeros((y.shape[0],exp_time1, 1,y.shape[1]))
    

    mean_b = U_b = tf.constant(np.zeros((lb_0 + lb_1)),dtype=tf.float64)
    mean_W = U_w = tf.constant(np.zeros((l_0*l_1 + l_1*l_2)),dtype=tf.float64)
    
    W_0_step0 = W[0:l_0*l_1]
    W_0_step0 = np.reshape(W_0_step0, [l_0,l_1])
    #store W_0
    stack1_W_0 = np.zeros((len(x_), exp_time1,l_0,l_1)) 
    
    #initialiser stack1_W_0

    for i in range(len(x_)):

        stack1_W_0[i,0,:,:] = W_0_step0

    W_1_step0 = W[l_0*l_1:(l_0*l_1 + l_1*l_2 )]
    W_1_step0 = np.reshape(W_1_step0, [l_1,l_2])
    #store W_1
    stack1_W_1 = np.zeros((len(x_), exp_time1,l_1,l_2))

    #initialiser stack1_W_0

    for i in range(len(x_)):

        stack1_W_1[i,0,:,:] = W_1_step0


    #remember: SIZE_gMRF_b = lb_0 + lb_1
    
    b_0_step0 = b[0:lb_0]
    b_0_step0 = np.reshape(b_0_step0,[-1])
    #store b_0
    stack1_b_0 = np.zeros((len(x_),exp_time1, b_0_step0.shape[0]))

    for i in range(len(x_)):

        stack1_b_0[i,0,:] = b_0_step0
    

    b_1_step0 = b[lb_0: (lb_0+lb_1)]
    b_1_step0 = np.reshape(b_1_step0,[-1])
     
    #store b_0
    stack1_b_1 = np.zeros((len(x_), exp_time1, b_1_step0.shape[0]))

    for i in range(len(x_)):

        stack1_b_1[i,0,:] = b_1_step0
   
    Sigma_step0 = Sigma
    #store b_0
    stack1_Sigma = np.zeros((len(x_), exp_time1, Sigma.shape[0],Sigma.shape[1]))

    for i in range(len(x_)):

        stack1_Sigma[i,0,:,:] = Sigma_step0


    
    
    L_step0 =  obtain_choleski_factor_for_Sigma (Sigma_step0)
    #store L_step0
    stack1_L_step = np.zeros((len(x_), exp_time1, L_step0.shape[0],L_step0.shape[1]))
    
    for k in range(len(x_)):

        stack1_L_step[k,0,:,:] = L_step0


    print("DOUBLE BACKPROPAGATED GRANDEUR### Etape0")

    stack1_ytrain_prediction = np.zeros((exp_time1, y_.shape[0],y_.shape[1]))
    
    #stack1_ytrain_prediction Need To be initialized 
    
    stack1_ytrain_prediction[0,:,:]  = Cluster_ytrain_prediction 
   
    
    #A function for g1 differentiated

    print("initialize U_i_t in double backpropagation too")

    stack1_U_t = np.zeros((exp_time1, y_.shape[0],y_.shape[1]))
    
    for j in range(len(x_)):
          stack1_U_t [0,j,:] = np.mean(np.random.multivariate_normal(np.reshape(np.zeros(y_.shape[1]),-1), np.identity(y_.shape[1]),exp_time2), axis=0) 

    for peter in range(1, exp_time1) : #prendre la moyenne sur le nombre de fois pour le expected

        #Work with the double propagation scheme :

        s = peter
        epsilon = dbs_epsilon #10e-10 #(1/(10**(exp_time1)))
        for i in range(x_.shape[0]):               # remember x.shape[0] = q
        
            xi = tf.reshape(x_[i,], [1,x_.shape[1]])
            #
            
            myg_1_function_diff_input = myg_1_function_input = np.reshape(b_0_step0,[1, b_0_step0.shape[0]])+ tf.matmul(tf.reshape(xi,[1, x_.shape[1]]),stack1_W_0[i,(s-1),:,:])
            
            myg_1_function_diff_input = myg_1_function_diff_input.eval(session=sess)

            myg_1_function_input  = myg_1_function_input.eval(session=sess)


            print("myg_1_function_diff_input FIRST FIRST ", myg_1_function_diff_input)
            
            My_array_Inputs = stack1_ytrain_prediction[(s-1),i,:]-y_[i,:]
            
            past_W_0 = stack1_W_0[i,(s-1),:,:]

            print(past_W_0 )
            print("HAHA IT IS DOUBLE BACK PROPAGATING", My_array_Inputs)


            print("test la fonction sil te plati", myg_1_function_diff( myg_1_function_diff_input ).eval(session=sess))

            print("my first test", tf.matmul(tf.reshape(xi,[x_.shape[1],1]),(myg_1_function_diff( myg_1_function_diff_input ))).eval(session=sess) )  



            Grad_W_O = (epsilon)*(2/len(x_))*tf.multiply(tf.matmul(tf.reshape(xi,[x_.shape[1],1]),(myg_1_function_diff( myg_1_function_diff_input ))),tf.reshape(tf.matmul(stack1_W_1[i,(s-1),:,:], ( My_array_Inputs ).reshape((y_.shape[1],1))  ), [-1]))
  
            print(Grad_W_O.eval(session=sess))
            stack1_W_0[i,s,:,:]= past_W_0 -  (Grad_W_O).eval(session=sess)  
            #stack1_W_1 [i,(s-1),:,:]
            print(stack1_W_0[i,s,:,:])
            past_W_1 = stack1_W_1[i,(s-1),:,:]
            print(past_W_1)
            Grad_W_1 = (epsilon)*(2/len(x_))*tf.matmul(tf.transpose(myg_1_function(myg_1_function_input)),np.array(My_array_Inputs).reshape((1,y_.shape[1])) )
    
            print(Grad_W_1.eval(session=sess))
            stack1_W_1[i,s,:,:] = past_W_1 - (Grad_W_1).eval(session=sess)  
            
            print(stack1_W_1[i,s,:,:])
            past_b_0 = stack1_b_0[i,(s-1),:]
             
            print("We are part", past_b_0)
            
            Grad_b_0 = (epsilon)*(2/len(x_))*tf.matmul((myg_1_function_diff(myg_1_function_diff_input)), tf.matmul(stack1_W_1 [i,(s-1),:,:],  np.array(stack1_ytrain_prediction[(s-1),i,:]-y_[i,:] ).reshape((y_.shape[1],1))  )    )
      
            print(Grad_b_0.eval(session=sess)) 
            stack1_b_0[i,s,:] = past_b_0 -  (Grad_b_0).eval(session=sess)
            
            
            past_b_1 = stack1_b_1[i,(s-1),:]
            
            Grad_b_1 = (epsilon)*(2/len(x_))* (stack1_ytrain_prediction[(s-1),i,:]-y_[i,:] )
            
            stack1_b_1[i,s,:] =  past_b_1  - Grad_b_1
            
            
            past_Sigma = stack1_Sigma[i,(s-1),:,:]
            
            
            Grad_Sigma = (epsilon)*(2/len(x_))* tf.matmul(tf.matmul(tf.matrix_inverse(stack1_L_step[i,(s-1),:,:] + tf.transpose(stack1_L_step[i,(s-1),:,:])  ), stack1_U_t [(s-1),i,:].reshape((y_.shape[1],1)) ) , np.array(stack1_ytrain_prediction[(s-1),i,:]-y_[i,:]).reshape((1,y_.shape[1])))
                        
   
            stack1_Sigma[i,s,:,:] = (past_Sigma - Grad_Sigma).eval(session=sess)
            

            stack1_U_t[s,i,:] = np.mean(np.random.multivariate_normal(np.reshape(np.zeros(y_.shape[1]),-1), np.identity(y_.shape[1]),exp_time2), axis=0) 

            print(stack1_Sigma[i,s,:,:])
            stack1_L_step[i,s,:,:] = obtain_choleski_factor_for_Sigma (stack1_Sigma[i,s,:,:])
            print("Choleski factor is:",stack1_L_step[i,s,:,:])
            #yi_mean = np.mean(np.random.multivariate_normal(np.reshape(NN2(xi, W_0, W_1, b_0, b_1).eval(session=sess),-1), Sigma,exp_time2), axis=0)

            print(stack1_b_0[i,s,:])

            myg_1_function_general_inputs2 = tf.matmul(tf.reshape(xi, [1, x_.shape[1]]), stack1_W_0 [i,s,:,:]).eval(session=sess)
            
            myg_1_function_general_inputs = stack1_b_0[i,s,:]+ myg_1_function_general_inputs2 #tf.matmul(tf.reshape(xi, [1, x_.shape[1]]), stack1_W_0 [i,s,:,:]).eval(session=sess)
            
            print("myg_1_function_general_inputs", myg_1_function_general_inputs)
            
            #print(tf.reshape(tf.matmul(stack1_L_step[i,s,:,:], stack1_U_t[i,s,:].reshape(y_.shape[1],1)), (y_.shape[1],1) ).shape)
            #np.array(stack1_ytrain_prediction[(s-1),i,:]-y_[i,:])

            print("Grad 1", tf.matmul(myg_1_function(myg_1_function_general_inputs),stack1_W_1 [i,s,:,:]).eval(session=sess) )
            
            Grad_Y = tf.matmul(myg_1_function(myg_1_function_general_inputs),stack1_W_1 [i,s,:,:]) + tf.reshape(tf.matmul(stack1_L_step[i,s,:,:], stack1_U_t[s,i,:].reshape(y_.shape[1],1)), (1, y_.shape[1]) )
            
            print(s, Grad_Y.eval(session=sess))
            
            Last_s = s
            
            stack1_ytrain_prediction[s,i,:] = stack1_b_1[i,s,:] + Grad_Y.eval(session=sess) + 2*(10e-2)*2*np.array(y_[i,:] -stack1_ytrain_prediction[(s-1),i,:]).reshape((1,y_.shape[1]))


    ################################################### TRAINING STATS #####################################################################
    
    errors = np.zeros((y_.shape[0],y_.shape[1]))


    errors = stack1_ytrain_prediction[(exp_time1-1),:,:] - y_

    print("DOUBLE BACKPROPAGATED GRANDEUR### Etape2")
    SPNNR_train_rmse = np.sqrt((LA.norm(errors)**2)/x_.shape[0] ) 
    print("DOUBLE BACKPROPAGATED train intermediary Cluster - DOUBLE BACKPROPAGATED GRANDEUR Root-Error ### Etape2", SPNNR_train_rmse)
    print("DOUBLE BACKPROPAGATED GRANDEUR### Etape3")
    #print("The Root Mean Square on train data for the SPNNR model is %f"%SPNNR_train_rmse)
    ################################################### TEST STATS #####################################################################
    errors_test = 10e3
    print(xtest_)
    print(ytest_) 
    
    
    if len(xtest_) > 0 :

       if xtest_.ndim == 1:
          xtest_ = xtest_.reshape(-1, xtest_.shape[0])
          ytest_ = ytest_.reshape(-1, ytest_.shape[0])
          Cluster_ytest_prediction = Cluster_ytest_prediction.reshape(-1, Cluster_ytest_prediction.shape[0]) 

       #print("We have differents shape", ytest_.shape[0] and ytest_.shape[1])
       stack1_ytest_prediction = np.zeros((exp_time1, ytest_.shape[0],ytest_.shape[1]))

       #stack1_ytest_prediction Need To be initialized 
    
       stack1_ytest_prediction[0,:,:]  = Cluster_ytest_prediction 

    
       print("DOUBLE BACKPROPAGATED test GRANDEUR### Etape1")
       
       #errors_test = np.zeros((ytest_.shape[0],ytest_.shape[1]))

       #stack2_test = np.zeros((ytest.shape[0], 1,ytest.shape[1]))

       for i in range(xtest_.shape[0]):

           #predict for the i-th test data
           

           Position_Closed_Neighbor_ = np.argmin( [ np.min(xtest_[i,:] - x_[observation,:]) for observation in range(len(x_)) ])     #LA.norm
              
           pos_train_j = Position_Closed_Neighbor_ = int(Position_Closed_Neighbor_)
           
           #print("DOUBLE BACKPROPAGATED Position_Closed_Neighbors",Position_Closed_Neighbor_)

           Y_Grad_Update = tf.matmul(   myg_1_function (stack1_b_0[pos_train_j,(Last_s),:] +  tf.matmul(tf.reshape(xtest_[i,:], [1, xtest_.shape[1]]), stack1_W_0 [pos_train_j,(Last_s),:,:])    )  , stack1_W_1 [pos_train_j,(Last_s),:,:]) + tf.reshape(tf.matmul(stack1_L_step[pos_train_j,(Last_s),:,:], stack1_U_t [(Last_s),pos_train_j,:].reshape(y_.shape[1],1)), (1,y_.shape[1]))
           stack1_ytest_prediction[1,i,:] = stack1_b_1[pos_train_j, (Last_s),:] + Y_Grad_Update.eval(session=sess) + 2*(10e-2)*2*np.array(y_[pos_train_j,:] -stack1_ytrain_prediction[(Last_s),pos_train_j,:]).reshape((1,ytest_.shape[1]))
          
       print(stack1_ytest_prediction[1,:,:]) 
       errors_test = stack1_ytest_prediction[1,:,:] - ytest_

          
       print("DOUBLE BACKPROPAGATED test GRANDEUR### Etape2")
       SPNNR_test_rmse = np.sqrt((LA.norm(errors_test)**2)/xtest_.shape[0] )  
       print("DOUBLE BACKPROPAGATED test intermediary Cluster - DOUBLE BACKPROPAGATED GRANDEUR Root-Error ### Etape2", SPNNR_test_rmse)
       print("DOUBLE BACKPROPAGATED test GRANDEUR### Etape3")
       #print("The Root Mean Square on test data for the SPNNR model is %f"%SPNNR_test_rmse)

       #y_test_prediction = np.reshape(stack2_test,(ytest.shape[0],ytest.shape[1]))
    
    if len(xtest_)> 0: 
    
       return stack1_ytrain_prediction[(exp_time1-1),:,:], SPNNR_train_rmse, stack1_ytest_prediction[1,:,:] , errors_test
    else:

       return stack1_ytrain_prediction[(exp_time1-1),:,:], SPNNR_train_rmse, [] , errors_test   

#if __name__ == "__main__":
    
     #main()



