#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#packages environment
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import gym
from gym import error, spaces, utils
#from gym.utils import seeding
#import statsmodels.api as sm
#import statsmodels.formula.api as smf
import pandas.util.testing as tm
from sklearn.linear_model import LogisticRegression

#Gym environment - continuous

class ContinEnv(gym.Env):
  def __init__(self):
    self.size = 200
    #get initial values for theta's
    #fit logit model to data
    self.df = pd.DataFrame(dict(
            Xs=np.random.normal(0,1,size=self.size),
            Xa=np.random.normal(0,1,size=self.size),
            Y=np.random.binomial(1, 0.05, self.size)))
    self.model = LogisticRegression().fit(self.df[["Xs", "Xa"]], np.ravel(self.df[["Y"]]))

    #extract theta parameters from the fitted logistic
    self.thetas = np.array([self.model.coef_[0,0] , self.model.coef_[0,1], self.model.intercept_[0]]) #thetas[1] coef for Xs, thetas[2] coef for Xa

    #set range for obs space
    #? not all values should be equaly likely to be sampled, this is missing here
    #? can I restrict the sampling space when an episode is run?
    self.minXa1 = pd.to_numeric(min(self.df[["Xa"]].values.flatten()))
    self.minXs1 = pd.to_numeric(min(self.df[["Xs"]].values.flatten()))
    
    self.maxXa1 = pd.to_numeric(max(self.df[["Xa"]].values.flatten()))
    self.maxXs1 = pd.to_numeric(max(self.df[["Xs"]].values.flatten()))
    
    self.min_Xas=np.array([np.float32(self.minXa1), np.float32(self.minXs1)])
    self.max_Xas=np.array([np.float32(self.maxXa1), np.float32(self.maxXs1)])


    #set range for action space
    self.XSA1 = np.add((self.thetas[1]*(self.df[["Xs"]])).to_numpy(), (self.thetas[2]*(self.df[["Xa"]])).to_numpy())
    self.XSA1 += self.thetas[0]
    self.Rho=(1/(1+np.exp(-self.XSA1)))
    self.actmin = (min(self.Rho))
    self.actmax = (max(self.Rho))

    self.min_action=np.array([np.float32(self.actmin)])
    self.max_action=np.array([np.float32(self.actmax)])
   
    #set ACTION SPACE
    #space.box handles continuous action space
    #it needs values for the bounds and the shape: low, high, shape (as in a tensor)
    #the bounds for a logit transformation of X's are 0, 1 (or min and max of the logit transform with initial values for theta)
    self.action_space = spaces.Box(
            low=self.min_action,
            high=self.max_action,
            dtype=np.float32)
    
    #set OBSERVATION SPACE
    #it is made of values for Xa, Xs for each observation
    self.observation_space = spaces.Box(low=self.min_Xas, 
                                   high=self.max_Xas, 
                                   dtype=np.float32)
    
    #self.Y_obs_space = spaces.Discrete(n=2)
    #combine them in a tuple - I think it doesn't work well
    #self.observation_space = spaces.Tuple([self.Xas_obs_space, self.Y_obs_space])

    #set an initial state, sample a random row from df to get 1 observation (Xs(0), Xa(0))
    #the step def will update self.state according to some value
    self.state=self.df.sample(n=1, random_state=1).values.reshape(3,)

    #introduce some length
    self.horizon=200
    

  def seed(self, seed=None):
    self.np_random, seed = seeding.np_random(seed)
    return [seed]    

#take an action with the environment
#it returns the next observation, the immediate reward, whether the episode is over (done) and additional information    
#"action" argument is one value in the range of the action space (logit transform)
  def step(self, action):

    #compute rho
    Xsa=(self.thetas[0])+(self.thetas[1])*(self.state[0])+(self.thetas[2])*(self.state[1])
    rho=(1/(1+np.exp(-Xsa)))
    
    #apply a value from the action space on the state by means of some function that depends on action
    #the function
    g = ((1/2)*(3-(2*(action)))*(self.state[1])+(1-(2*(action)))*((1+(self.state[1])**2)**0.5))
    
    #from here what?? does g value replace Xa? (reflecting the effect of an intervention)

    #rho (risk) high, intervene on Xa
    if (rho >= 0.5):
        new_Xa = g
    else: #if risk low, do not intervene
        new_Xa = (self.state[1])  
    #apply intervention on self.state
    self.state[1] = new_Xa
 
    #before setting the reward, predict Y_+1, as we have a new Xa
    self.Y_new =+ 0 + (self.thetas[0])+(self.thetas[1])*(self.state[0])+(self.thetas[2])*(self.state[1])
    #compute mean of Y (this is no longer 0-1 but a probability)
    self.Ynew_cumul = np.mean(self.Y_new)
    #reduce the horizon
    self.horizon -= 1
    
    #depending on the value of self.state, apply a reward
    reward = self.Ynew_cumul 

    #check if horion is over, otherwise keep on doing
    if self.horizon <= 0:
        done = True
    else:
        done = False

    #set placeholder for infos
    info ={}        
     
    return self.state, reward, done, {}

#reset state and horizon    
  def reset(self):
    self.state=self.df.sample(n=1, random_state=1).values.reshape(3,)
    self.horizon = 20
    return self.state
