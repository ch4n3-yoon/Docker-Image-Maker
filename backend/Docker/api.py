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

    def create_container(self, container_name, dockerfile=None):
        image = self.build_image()
        self.client.containers.run(image.tag, name=container_name, detach=True)
        container = Container.objects.create(name=container_name, image=image, command='', description='')
        return container
