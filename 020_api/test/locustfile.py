import numpy as np
from locust import HttpLocust, TaskSet, task
from sklearn import datasets


class UserBehavior(TaskSet):
    def on_start(self):
        self.iris = datasets.load_iris().data



    @task(1)
    def predict(self):
        rnd = np.random.randint(0,self.iris.shape[0],1)
        dict_data = dict(zip(['p_l','p_w','s_l','s_w'],self.iris[rnd].tolist()[0]))
        headers = {'content-type': 'application/json'}
        with self.client.post("/predict", json=dict_data, headers=headers, catch_response=True) as response:
            if response.status_code == 200:
                response.success()

class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000


#locust -f 020_api/test/locustfile.py --host=http://127.0.0.1:5000 --no-web -c 1000 -r 100
#-c specifies the number of Locust users to spawn, and -r specifies the hatch rate (number of users to spawn per second).
