



class VIagent:
    def __init__(self,env):
        self.P=env.P
        self.nA=env.nA
        self.nS=env.nS
        self.max_steps=env._max_episode_steps
        self.values = np.random.random(env.observation_space.n)
        self.policy = np.zeros(env.observation_space.n) 
        self.tolerance = 0.001
        self.val1=[]
        self.val2=[]
        self.tick=0
        self.tock=0
        
    def value_iteration(self):
        while True:
            delta=0
            previous_values = np.copy(self.values)
            
            for state in range(nS):
                Q=[]
                
                for action in range(nA):
                    expected_future_rewards=[]
                    
                    for next_state_prob in P[state][action]:
                        prob, nextstate, reward, is_terminal = next_state_prob
                        
  
                        expected_future_rewards.append((prob * (reward + self.values[nextstate])))
                
                    Q.append(sum(expected_future_rewards)) 

                
                self.values[state] = max(Q)  
                self.val2.append(self.mean_rewards_per_10())
                delta = max(delta,abs(self.values[state]-previous_values[state]))
            
            if (delta < self.tolerance):
                break
            self.tick=time.time()    
            self.val1.append(self.mean_rewards_per_500())
            self.tock=time.time()    
                
        return self.values
    
    def policy_extract(self):
        
        for state in range(self.nS):
            
            q_stateaction=[]
            for action in range(self.nA):
                
                expected_future_rewards=[]
                for next_state_prob in P[state][action]:
                    
                    prob, nextstate, reward, is_terminal = next_state_prob
                    expected_future_rewards.append(prob*(reward + self.values[nextstate]))
                
                q_stateaction.append(sum(expected_future_rewards))
            
            self.policy[state]=np.argmax(q_stateaction)
            
        
        return self.policy
        


          
    def choose_action(self,observation):

        return self.policy[observation]

                        
                        
    def mean_rewards_per_500(self):
        self.policy_extract()
        total_reward = 0
        for episodes in range(500):
            observation = env.reset()
            for _ in range(1000):

                action = self.choose_action(observation)
                observation, reward, done, info = env.step(action)
                total_reward += reward
                if done:
                    observation = env.reset()
        return (total_reward/500)
    
    def mean_rewards_per_10(self):
        self.policy_extract()
        total_reward = 0
        for episodes in range(10):
            observation = env.reset()
            for _ in range(1000):

                action = self.choose_action(observation)
                observation, reward, done, info = env.step(action)
                total_reward += reward
                if done:
                    observation = env.reset()
        return (total_reward/10)   