import webapp2
from validate_email import validate_email
import json
import logging


def handle_404(request, response, exception):
    logging.exception(exception)
    response.set_status(404)
    response.headers['Content-Type'] = 'application/json'
    json.dump({"error": {"status": 404, "message": "Resource Not Found"}}, response.out)


def handle_500(request, response, exception):
    logging.exception(exception)
    response.headers['Content-Type'] = 'application/json'
    json.dump({"error": {"status": 500, "message": "Internal Server Error"}}, response.out)


class Home(webapp2.RequestHandler):
    def get(self):
        self.response.write('email-verifier')


class Validate(webapp2.RequestHandler):
    def jsonify(self, *args):
        self.response.headers['Content-Type'] = 'application/json'
        json.dump(args[0], self.response.out)
        return self.response

    def get(self):
        email = self.request.get("email") if self.request.get("email") else None
        if email is None:
            raise ValueError("email query param not provided.")

        self.jsonify({'email': email,
                      'is_valid': validate_email(email, verify=True)
                      })


app = webapp2.WSGIApplication([
    ('/', Home),
    ('/validate', Validate),
], debug=True)
app.error_handlers[404] = handle_404
app.error_handlers[500] = handle_500


def main():
    from paste import httpserver
    httpserver.serve(app, host='0.0.0.0', port='8080')

if __name__ == '__main__':
    main()
