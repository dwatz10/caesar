import webapp2
import cgi


page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Caesar</title>
    <style type="text/css">
        .error {
            color: red;
        }
    </style>
</head>
<body>
    <h1>
        <a href="/">Caesar</a>
    </h1>
"""

page_footer = """
</body>
</html>
"""

class Index(webapp2.RequestHandler):

    def get(self):

        edit_header = "<h3>Encrypt</h3>"


        rot_form = """
        <form action="/rotations" method="post">
            <label for="rot_amount">Rotate by:</label>
                <input type="text" name="rot_amount" value="0"/>
                <br>
            <label for="text">Encrypt</label>
                <textarea type="text" name="text"></textarea>

            <input type="submit" value="Submit"/>
        </form>
        """

        error = self.request.get("error")
        error_element = "<p class='error'>" + error + "</p>" if error else ""


        main_content = edit_header + rot_form + error_element
        response = page_header + main_content + page_footer
        self.response.write(response)

class rotation(webapp2.RequestHandler):

    def post(self):
        rot = int(cgi.escape(self.request.get("rot_amount")))
        text = cgi.escape(self.request.get("text"))


        def encrypt(text, rot):
            newstring = ""
            for x in text:
                newstring += rotate_character(x, rot)
            return newstring

        def alphabet_position(letter):
            return ord(letter) % 32 - 1

        def rotate_character(char, rot):
            if char.isalpha() == True:
                if char.isupper() == True:
                    pos = (alphabet_position(char) + rot) % 26
                    newchar = pos + ord("A")

                if char.islower() == True:
                    pos = (alphabet_position(char) + rot) % 26
                    newchar = pos + ord("a")
                return chr(newchar)
            if char.isalpha() == False:
                return char

        newstring = encrypt(text, rot)
        response = page_header + "<p>" + newstring + "</p>" + page_footer
        self.response.write(response)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/rotations', rotation)

], debug=True)
