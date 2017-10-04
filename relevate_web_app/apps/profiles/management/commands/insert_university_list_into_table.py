from django.core.management.base import BaseCommand, CommandError
from ...models.university_model import Universities
from ...modules.list_of_universities import WORLD_UNIVERSITIES_LISTS
from django.core.exceptions import ObjectDoesNotExist


class Command(BaseCommand):

	help="Put universities into database"

	def add_arguments(self, parser):
		pass

	def handle(self, *args, **options):
		"""
			Inserts university dictionary into a university database method.
			This function is called as a script by a bash process.
			If universities' name already exist it skips over it.
			:return:
		"""
		for each_uni in WORLD_UNIVERSITIES_LISTS:
			self.stdout.write(self.style.SUCCESS('Writing %s '
												 'from list to University Table' % each_uni))
			try:
				Universities.objects.get(name_of_university=each_uni)
				self.stdout.write(self.style.SUCCESS('Already added %s '
																 'from list to University Table' % each_uni))
			except ObjectDoesNotExist:
				new_uni = Universities(name_of_university=each_uni)
				new_uni.save()
				self.stdout.write(self.style.SUCCESS('Successfully added %s '
																 'from list to University Table' % each_uni))
		self.stdout.write(self.style.SUCCESS('Successfully added items from list to University Table'))