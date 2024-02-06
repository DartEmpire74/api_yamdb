import csv

from django.core.management.base import BaseCommand, CommandError

from reviews.models import (
    Title, Category, Genre, Review, Comment, User
)
from .utils import (
    import_comment_model,
    import_category_model,
    import_genre_model,
    import_genre_title_model,
    import_review_model,
    import_title_model,
    import_user_model,
)


MODELS = {
    'title': Title,
    'category': Category,
    'genre': Genre,
    'review': Review,
    'comment': Comment,
    'user': User,
    'genre_title': (Genre, Title),
}


MODELS_FUNCTIONS = {
    'title': import_title_model,
    'category': import_category_model,
    'genre': import_genre_model,
    'genre_title': import_genre_title_model,
    'review': import_review_model,
    'comment': import_comment_model,
    'user': import_user_model,
}


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('csv_file_path', type=str, help='path to csv file')
        parser.add_argument('model', type=str, help='model to add')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file_path']
        model = MODELS.get(options['model'].lower())

        if not model:
            raise CommandError(
                (f'Model: {options["model"].capitalize()} does not exist'
                 f'\nExisting models: {", ".join(MODELS.keys())}')
            )

        func = MODELS_FUNCTIONS[options['model']]
        model_instances = []

        with open(csv_file_path, 'r', encoding='utf-8') as file:
            csv_file = csv.DictReader(file)

            if options['model'].lower() == 'genre_title':
                for line in csv_file:
                    func(line)

            else:

                for line in csv_file:
                    model_instance = func(line)

                    model_instances.append(model_instance)

                model.objects.bulk_create(
                    model_instances, ignore_conflicts=True
                )

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
