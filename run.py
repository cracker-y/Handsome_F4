from app import create_app, routes

application = create_app()

if __name__ == "__main__":
    application.run(debug=True)