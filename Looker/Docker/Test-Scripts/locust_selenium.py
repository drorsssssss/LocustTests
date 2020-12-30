from realbrowserlocusts import HeadlessChromeLocust
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from locust import TaskSet, task, between
import random
import yaml
from LocustUtils.redis_utils import RedisUtils


class LocustUserBehavior(TaskSet):
    _account_id=None

    def on_start(self):
        f = open('/mnt/locust/config.yml')
        params = yaml.load(f)
        f.close()
        host='conf'
        self.SITE = params[host]['site']
        self.DASH_ID = params[host]['dashboard_id']
        self.user_entry = params[host]['email']
        self.pass_entry = params[host]['pass']
        self.filters_combinations_big = params[host]['filters_combinations_big']['list']
        self.filters_combinations_small = params[host]['filters_combinations_small']['list']
        redis_host = params[host]['redis_host']
        redis_conn= RedisUtils(redis_host)
        print(f"Number of Users In Queue: {redis_conn.redis_queue_length()}")
        self._account_id=redis_conn.redis_dequeue()
        redis_conn.redis_quit()
        self.login()

    def on_stop(self):
        self.logout()

    def login(self):
        self.client.get(self.SITE + "/login")

        username = self.client.find_element_by_id("login-email")
        pw = self.client.find_element_by_id("login-password")
        box = self.client.find_element_by_class_name("checkbox")
        username.clear()
        username.send_keys(self.user_entry)
        pw.clear()
        pw.send_keys(self.pass_entry)
        box.click()
        self.client.find_element_by_id("login-submit").click()

    def logout(self):
        print("stopping session")

    def open_dashboard(self,filter_container_type):
        script = """
        window.awaitPerformanceObservation("rendered").then(function() {
            var dash_render = document.createElement("div");
            dash_render.id = "dash_listener";
            document.body.appendChild(dash_render);
        });"""

        try:
            url = f"{self.SITE}dashboards-next/{str(self.DASH_ID)}?ACCOUNT={self._account_id}&{random.choice(filter_container_type)}"
            print(url)
            self.client.get(url)

            self.client.execute_script(script)

            self.client.wait.until(
                EC.presence_of_element_located(
                    (By.ID, "dash_listener")
                )
            )
        except TimeoutException:
            print("hit timeout")

    @task(4)
    def simple_dashboard_loading(self):
        self.client.timed_event_for_locust(
            "Load", "dashboard",
            self.open_dashboard, self.filters_combinations_small
        )


    @task(1)
    def heavy_dashboard_loading(self):
        self.client.timed_event_for_locust(
            "Load", "dashboard",
            self.open_dashboard, self.filters_combinations_big
        )

class LocustUser(HeadlessChromeLocust):

    host = "looker_cloud"
    timeout = 60
    wait_time = between(5, 10)
    screen_width = 1200
    screen_height = 600
    task_set = LocustUserBehavior

