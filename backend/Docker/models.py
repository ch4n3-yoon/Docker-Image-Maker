from django.db import models


class Dockerfile(models.Model):
    content = models.TextField()


class Image(models.Model):
    tag = models.CharField(max_length=255)


class Container(models.Model):
    image = models.CharField(max_length=255)
    imageId = models.TextField()
    command = models.TextField(null=True)


class Port(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    inner_port = models.IntegerField()
    outer_port = models.IntegerField()

