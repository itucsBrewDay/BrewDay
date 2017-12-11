from locust import HttpLocust, TaskSet, task

class WebsiteTasks(TaskSet):
	def on_start(self):
		self.client.post("/register", {
			"name": "name",
			"surname": "surname",
			"email": "email",
			"username": "username",
			"password": "pwd",
			"confirm": "pwd"
		})

		self.client.post("/login", {
			"username": "username",
			"password": "pwd"
		})

	@task
	def index(self):
		self.client.get("/")

	@task
	def index2(self):
		self.client.get("/2")

	@task
	def about(self):
		self.client.get("/about")

	@task
	def search(self):
		self.client.get("/search_recipe")

	@task
	def profile(self):
		self.client.get("/profile")

	@task
	def profile_edit(self):
		self.client.post("/profile/edit/1", {
			"name": "name",
			"surname": "surname",
			"email": "email",
			"username": "username",
			"password": "pwd"
		})


class WebsiteUser(HttpLocust):
	task_set = WebsiteTasks
	min_wait = 5000
	max_wait = 15000