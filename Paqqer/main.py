from app import create_app, io
# from engineio.async_drivers import gevent # Gevent para poder levantarlo en  auto-py-to-exe


app = create_app()


if __name__ == "__main__":
    io.run(app, host="0.0.0.0", port=80, debug=True)