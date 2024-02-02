from authentication.controllers import AuthenticationController, MainMenuController, CollaborateurController
import subprocess as sp

class Application:
    routes = {
        "login": AuthenticationController.login,
        "main_menu": MainMenuController.display_menu,
        "collaborateur_management": CollaborateurController.display_collaborateur_menu,
        "create_collaborateur": CollaborateurController.create_collaborateur,
        "update_collaborateur": CollaborateurController.update_collaborateur,
        "delete_collaborateur": CollaborateurController.delete_collaborateur,
    }

    def __init__(self) -> None:
        self.route = "login"
        self.exit = False
        self.route_params = None
        self.session = {
            "user": None
        }


    def run(self):
        while not self.exit:
            # Clear the shell output
            sp.call('clear', shell=True)

            # Get the controller method that should handle our current route
            controller_method = self.routes[self.route]

            # Call the controller method, we pass the store and the route's
            # parameters.
            # Every controller should return two things:
            # - the next route to display
            # - the parameters needed for the next route
            next_route, next_params = controller_method(
                self.session, self.route_params
            )

            # set the next route and input
            self.route = next_route
            self.route_params = next_params

            # if the controller returned "quit" then we end the loop
            if next_route == "quit":
                self.exit = True

if __name__ == "__main__":
    app = Application()
    app.run()