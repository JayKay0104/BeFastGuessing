
class HTMLContent:
    """ contains our static html repsonses """

    @staticmethod
    def hello() -> str:
        """ returns the standard html content """
        return """
            <html>
                <head>
                    <title>Here we go!</title>
                </head>
                <body>
                    <h1>Hello!</h1>
                </body>
            </html>
            """
