from django.http import HttpResponse
import docker


# Image Build
def build_image(request):
    dockerfile = request.body.encode('utf-8')
    with open('./tmp/Dockerfile', 'w') as f:
        f.write(dockerfile)

    client = docker.from_env()