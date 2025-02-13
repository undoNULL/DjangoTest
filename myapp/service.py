from myapp.models import PostModel, User


def create_account(id, pw):
    return User.objects.create(id=id, pw=pw) 

def account_compare(id, pw):
    return User.objects.get(id=id, pw=pw)


def create_post(title, author_id, content):
    return PostModel.objects.create(title=title, author_id=author_id, content=content)

def get_all_post():
    return PostModel.objects.all()

def get_post_by_title(title):
    return PostModel.objects.filter(title=title)

def get_post_by_id(id):
    return PostModel.objects.filter(author_id=id)