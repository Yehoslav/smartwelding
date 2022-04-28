from website import create_app


def main():
    """Creates and runs the server"""
    app = create_app()
    app.run(host="192.168.1.9", port="8080", debug=True)


if __name__ == "__main__":
    main()
