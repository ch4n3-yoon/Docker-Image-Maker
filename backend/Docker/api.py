import os
import docker
from Lib.misc import API as MiscAPI
from .models import Dockerfile, Image, Container, Port


class Api:
    def __init__(self):
        self.client = docker.from_env()

    def build_image(self, dockerfile=None):
        cwd = os.getcwd()
        path = ""
        dockerfile_name = ""
        dockerfile_path = ""

        if dockerfile:
            path = f"{cwd}/Docker/tmp"
            dockerfile_name = MiscAPI.get_random_string(16)
            dockerfile_path = f"{path}/{dockerfile_name}"

            with open(dockerfile_path, 'w') as f:
                f.write(dockerfile)

        else:
            path = f"{os.getcwd()}/Docker/"
            dockerfile_name = "Dockerfile"
            dockerfile_path = f"{path}/{dockerfile_name}"


        tag = MiscAPI.get_random_string(16)
        image = self.client.images.build(path=path, dockerfile=dockerfile_name, tag=tag)
        dockerfile_object = Dockerfile.objects.create(filepath=dockerfile_path, content=dockerfile)
        Image.objects.create(tag=tag, dockerfile=dockerfile_object)

        return image

    def get_all_images(self):
        return self.client.images.list()

    def get_image_by_name(self, name):
        try:
            return self.client.images.get(name)
        except docker.errors.ImageNotFound:
            return None

    def delete_image(self, name):
        image = self.get_image_by_name(name)
        if image is None:
            return False

        image.remove()

        if self.get_image_by_name(name):
            return False
        else:
            return True

    def create_container(self, container_name, dockerfile=None):
        image = self.build_image()
        self.client.containers.run(image.tag, name=container_name, detach=True)
        container = Container.objects.create(name=container_name, image=image, command='', description='')
        return container

    def get_container_by_id_or_name(self, id_or_name):
        try:
            return self.client.containers.get(id_or_name)
        except docker.errors.NotFound:
            return None

    def delete_container(self, id_or_name):
        container = self.get_container_by_id_or_name(id_or_name)
        container.remove()

    def commit_container(self, id_or_name, repository=None, tag=None, **kwargs):
        container = self.get_container_by_id_or_name(id_or_name)
        if container is None:
            return None

        repository = repository or kwargs.get('repository')
        tag = tag or kwargs.get('tag')
        message = kwargs.get('message')
        author = kwargs.get('author')

        container.commit(
            repository=repository,
            tag=tag,
            message=message,
            author=author
        )

        image = self.get_image_by_name(repository)
        if image:
            return image
        else:
            return None
