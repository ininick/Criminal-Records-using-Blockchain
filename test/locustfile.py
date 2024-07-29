# locustfile.py

from locust import HttpUser, TaskSet, task, between, LoadTestShape
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import time
import os

class UserBehavior(TaskSet):
    def on_start(self):
        # Setup Selenium WebDriver for Edge with user_agent
        options = Options()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0"
        options.add_argument(f"user-agent={user_agent}")
        
        edge_driver_path = os.path.join(os.getcwd(), "msedgedriver.exe")
        self.driver = webdriver.Edge(service=EdgeService(edge_driver_path), options=options)
        self.driver.get("http://localhost:5000")  # URL aplikasi Flask kamu

        # Simulate Metamask connection
        self.connect_metamask()

    def on_stop(self):
        self.driver.quit()

    def connect_metamask(self):
        # Klik tombol connect metamask
        connect_button_add = self.driver.find_element(By.ID, "connectMetaMaskAdd")
        connect_button_add.click()
        
        # Tunggu beberapa saat untuk user manual input di Metamask
        time.sleep(10)

    @task(1)
    def view_record(self):
        self.client.get("/get_records")

    @task(1)
    def add_record(self):
        name = "John Doe"
        age = 30
        city = "New York"
        region = "NY"
        crime = "Theft"
        punishment = "2 years"

        data = {
            'name': name,
            'age': age,
            'city': city,
            'region': region,
            'crime': crime,
            'punishment': punishment
        }
        
        self.client.post("/add_record", json=data)

    @task(1)
    def update_record(self):
        index = 1  # Sesuaikan dengan index record yang ingin diupdate
        name = "John Doe Updated"
        age = 31
        city = "Los Angeles"
        region = "CA"
        crime = "Fraud"
        punishment = "3 years"

        data = {
            'index': index,
            'name': name,
            'age': age,
            'city': city,
            'region': region,
            'crime': crime,
            'punishment': punishment
        }

        self.client.post("/update_record", json=data)

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)
    host = "http://localhost:5000"  # Tambahkan host di sini

class StepLoadShape(LoadTestShape):
    step_time = 60
    step_load = 5
    spawn_rate = 10
    time_limit = 1200

    def tick(self):
        run_time = self.get_run_time()

        if run_time < self.time_limit:
            current_step = run_time // self.step_time + 1
            return (current_step * self.step_load, self.spawn_rate)

        return None
