from reviews.models import (
    Title, Category, Genre, Review, Comment, User
)


def import_title_model(data: dict[str:str]) -> Title:
    category = Category.objects.get(pk=data['category'])
    instance = Title(
        id=data.get('id'),
        name=data.get('name'),
        year=data.get('year'),
        category=category
    )

    return instance


def import_genre_model(data: dict) -> Genre:
    return Genre(**data)


def import_category_model(data: dict) -> Category:
    return Category(**data)


def import_genre_title_model(data: dict) -> None:
    title_id = data.get('title_id')
    genre_id = data.get('genre_id')

    title = Title.objects.get(pk=title_id)
    genre = Genre.objects.get(pk=genre_id)

    title.genre.add(genre)


def import_review_model(data: dict) -> Review:
    title_id = data.get('title_id')
    author_id = data.get('author')
    title = Title.objects.get(pk=title_id)
    author = User.objects.get(pk=author_id)

    instance = Review(
        id=data.get('id'),
        title=title,
        text=data.get('text'),
        author=author,
        score=data.get('score'),
        pub_data=data.get('pub_date'),
    )

    return instance


def import_comment_model(data: dict) -> Comment:
    review_id = data.get('review_id')
    author_id = data.get('author')
    review = Review.objects.get(pk=review_id)
    author = User.objects.get(pk=author_id)

    instance = Comment(
        id=data.get('id'),
        review=review,
        text=data.get('text'),
        author=author,
        pub_date=data.get('pub_date'),
    )

    return instance


def import_user_model(data: dict) -> User:
    instance = User(**data)

    return instance
