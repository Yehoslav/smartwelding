from website import create_app


def main():
    """Creates and runs the server"""
    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()
