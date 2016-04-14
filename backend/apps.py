from django.apps import AppConfig

class BackendConfig(AppConfig):
	name = 'backend'
	verbose_name = 'A temporary app until I refactor it out into a booking app'

	def ready(self):
		import signals
