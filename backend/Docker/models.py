from django.db import models


class Dockerfile(models.Model):
    filepath = models.TextField()
    content = models.TextField()


class Image(models.Model):
    tag = models.CharField(max_length=255)
    dockerfile = models.ForeignKey(Dockerfile, on_delete=models.CASCADE)


class Container(models.Model):
    name = models.CharField(max_length=255)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    command = models.TextField(null=True)
    description = models.TextField(null=True)


class Port(models.Model):
    container = models.ForeignKey(Container, on_delete=models.CASCADE)
    inner_port = models.IntegerField()
    outer_port = models.IntegerField()
    description = models.TextField(null=True)

