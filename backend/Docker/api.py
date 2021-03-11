import os
from Lib.misc import API as MiscAPI
from .models import Dockerfile, Image, Container, Port


class Api:
    def __init__(self):
        self.django_root_path = os.getcwd()
        self.dockerfiles_path = f"{self.django_root_path}/dockerfiles"

    @staticmethod
    def get_image(name):
        try:
            return Image.objects.get(name=name)
        except Image.DoesNotExist:
            return None

    @staticmethod
    def get_dockerfile(filename):
        try:
            return Dockerfile.objects.get(filepath__contains=filename)
        except Dockerfile.DoesNotExist:
            return None

    def create_image(self, name, **kwargs):
        if self.get_image(name):
            return None

        dockerfile_content = kwargs.get('dockerfile_content')
        dockerfile_path = kwargs.get('dockerfile_path')

        dockerfile = {}
        if dockerfile_path:
            content = ""
            with open(dockerfile_path) as f:
                content = f.read()

            if len(content) >= 0:
                dockerfile = Dockerfile.objects.create(filepath=dockerfile_path, content=content)

        elif dockerfile_content:
            random_dockerfile_name = MiscAPI.get_random_string(32)
            dockerfile_path = f"{self.dockerfiles_path}/{random_dockerfile_name}"
            with open(dockerfile_path, 'w', encoding='utf-8') as f:
                f.write(dockerfile_content)

            dockerfile = Dockerfile.objects.create(filepath=dockerfile_path, content=dockerfile_content)

        else:
            # Is Default Dockerfile Exist ?
            dockerfile = self.get_dockerfile('Dockerfile')
            if dockerfile is None:
                dockerfile_path = f"{self.dockerfiles_path}/Dockerfile"
                content = ""
                with open(dockerfile_path) as f:
                    content = f.read()

                dockerfile = Dockerfile.objects.create(filepath=dockerfile_path, content=content)

        image = Image.objects.create(name=name, dockerfile=dockerfile)

        return image, dockerfile

    def delete_image(self, name):
        image = self.get_image(name)
        image.delete()




API = Api()
