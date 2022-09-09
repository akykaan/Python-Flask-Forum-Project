from werkzeug.wrappers import Request, Response


@Request.application
def application(request):
    return Response("Hello from Vercel!")
