from CTFd import create_app

app = create_app()
app.run(debug=False, threaded=True, host="10.1.111.90", port=80)
