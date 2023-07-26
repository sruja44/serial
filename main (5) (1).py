
python
Copy
import random
import numpy as np
import matplotlib.pyplot as plt
from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.datacollection import DataCollector

class FluAgent(Agent):
    def __init__(self, unique_id, model, age, health_status, vaccination_status):
        super().__init__(unique_id, model)
        self.age = age
        self.health_status = health_status
        self.vaccination_status = vaccination_status
        self.infection_status = "susceptible"
        self.exposure_time = 0
        self.recovery_time = 0
    
    def step(self):
        if self.infection_status == "infected":
            self.exposure_time += 1
            if self.exposure_time >= self.model.exposure_duration:
                if random.random() < self.model.mortality_rate:
                    self.infection_status = "dead"
                else:
                    self.infection_status = "recovered"
                    self.recovery_time = 0
        elif self.infection_status == "recovered":
            self.recovery_time += 1
            if self.recovery_time >= self.model.recovery_duration:
                self.infection_status = "susceptible"
    
    def get_vaccinated(self):
        self.vaccination_status = "vaccinated"
    
    def get_infected(self):
        self.infection_status = "infected"
    
    def is_susceptible(self):
        return self.infection_status == "susceptible"
    
    def is_vaccinated(self):
        return self.vaccination_status == "vaccinated"
    
    def is_infected(self):
        return self.infection_status == "infected"

class FluModel(Model):
    def __init__(self, num_agents, exposure_duration, recovery_duration, mortality_rate, vaccination_rate):
        self.num_agents = num_agents
        self.exposure_duration = exposure_duration
        self.recovery_duration = recovery_duration
        self.mortality_rate = mortality_rate
        self.vaccination_rate = vaccination_rate
        self.schedule = RandomActivation(self)
        self.running = True
        
        for i in range(self.num_agents):
            age = np.random.normal(40, 10)
            health_status = np.random.normal(1, 0.1)
            vaccination_status = "unvaccinated"
            if random.random() < self.vaccination_rate:
                vaccination_status = "vaccinated"
            agent = FluAgent(i, self, age, health_status, vaccination_status)
            self.schedule.add(agent)
    
    def step(self):
        self.schedule.step()
    
    def run_model(self, num_steps):
        for i in range(num_steps):
            self.step()
    
    def get_agent_counts(self):
        num_susceptible = 0
        num_vaccinated = 0
        num_infected = 0
        num_recovered = 0
        num_dead = 0
        for agent in self.schedule.agents:
            if agent.is_susceptible():
                num_susceptible += 1
            elif agent.is_vaccinated():
                num_vaccinated += 1
            elif agent.is_infected() and agent.infection_status == "infected":
                num_infected += 1
            elif agent.is_infected() and agent.infection_status == "recovered":
                num_recovered += 1
            elif agent.is_infected() and agent.infection_status == "dead":
                num_dead += 1
        return {
            "susceptible": num_susceptible,
            "vaccinated": num_vaccinated,
            "infected": num_infected,
            "recovered": num_recovered,
            "dead": num_dead
        }

model = FluModel(num_agents=1000, exposure_duration=7, recovery_duration=14, mortality_rate=0.03, vaccination_rate=0.5)
model.run_model(num_steps=100)

agent_counts = model.get_agent_counts()
print(agent_counts)

plt.bar(range(len(agent_counts)), list(agent_counts.values()), align='center')
plt.xticks(range(len(agent_counts)), list(agent_counts.keys()))
plt.show()