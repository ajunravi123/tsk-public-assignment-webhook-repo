from app import create_app, template_renderer, get_data, jsonifyObj

render_template = template_renderer()
app = create_app()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fetch_history")
def fetch_history():
    all_data = get_data()
    return jsonifyObj(all_data)

if __name__ == '__main__':
    app.run(debug=True)
