from .HelloWorldController import HelloWorldController


def MainController(app, request, dao, render_template,redirect,session):

    @app.route("/")
    def HelloWorld():
        return HelloWorldController()