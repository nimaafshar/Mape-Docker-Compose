from locust import HttpUser, task, between, events, TaskSet
from faker import Faker
from locust import LoadTestShape
import random
import time

# faker object
faker=Faker()


class PetTaskSet(TaskSet):
    """
    load testing pet section of the api
    """
    base = '/v3'
    max_pets = 500
    pet_tags = [{'id':i, 'name':faker.word()} for i in range(50)]

    def random_status(self):
        return random.choice(('available','pending','sold'))

    def pet_payload(self):
        name = faker.name()
        return {
            "id": random.randint(1,self.max_pets),
            "name": name,
            "url": name.replace(" ", "_").lower(),
            "status": self.random_status(),
            "photoUrls": [faker.image_url() for i in range(random.randint(1,5))],
            "tags": random.choices(self.pet_tags,k=random.randint(1,4))
        }

    @task
    def create_pet(self):
        payload = self.pet_payload()
        self.client.post(self.base+"/pet", json=payload,name='createPet')

    @task
    def find_pet_by_id(self):
        self.client.get(f'{self.base}/pet/{random.randint(1,self.max_pets)}',name='findById')

    @task
    def update_pet(self):
        payload = self.pet_payload()
        self.client.put(f'{self.base}/pet',json=payload,name='updatePet')

    @task
    def find_by_status(self):
        self.client.get(f'{self.base}/pet/findByStatus?status={self.random_status()}',name='findByStatus')

    @task
    def find_by_tags(self):
        self.client.get(f'{self.base}/pet/findByTags?tags={random.choice(self.pet_tags)}',name='findByTags')


class StoreTaskSet(TaskSet):
    """
    load testing store section of the api
    """
    base = '/v3'

# user scenario
class User(HttpUser):
    wait_time = between(0, 0)
    tasks = (PetTaskSet,)


    
    

# class CycleScheduleShape(LoadTestShape):
#     """
#     A simply load test shape class that has different user at different cycles for mape system.
#     every cycle is 60 seconds by default. workload schedule, which means the number of users in 
#     every cycle, loads from a csv file. swapn rate and cycle duration are constant.
#     """
#     cycle_duration = 60 #in seconds
#     spawn_rate = 10

#     def __init__(self) -> None:
#         super().__init__()
#         # loading workload schedule
#         self.workload_schedule: dict = {}
#         with open('workload_schedule.csv','r') as workload_schedule_file:
#             for line in workload_schedule_file:
#                 cycle, users =  map(int,line.split(','))
#                 self.workload_schedule[cycle] = users


#     def tick(self):
#         """
#         this function doesn't return anything for first cycle,
#         waiting for application to load properly
#         """
#         cycle = (self.get_run_time() // self.cycle_duration) + 1
#         number_of_users = self.workload_schedule.get(cycle)
#         if number_of_users:
#             return (number_of_users,self.spawn_rate)
#         else:
#             return None

