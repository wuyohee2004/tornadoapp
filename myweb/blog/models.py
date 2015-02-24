from django.db import models

# Create your models here.

# <primitive>
# CREATE TABLE "article"(
#     "id" serial NOT NULL PRIMARY KEY,
#     "title" varchar(30) NOT NULL,
#     "content" text NOT NULL,
# );

#<orm>
class Article(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()

class Comment(models.Model):
    Article = models.ForeignKey(Article,related_name="article_comment")
    detail = models.TextField()