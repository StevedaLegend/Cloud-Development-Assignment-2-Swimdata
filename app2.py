from flask import Flask, redirect, render_template, request, url_for
import os
import hfpy_utils
import swim_utils  # Assuming you have a swim_utils module

app = Flask(__name__)


@app.route("/")
def get_swimmers_names():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    names = set()
    for swimmer in files:
        names.add(swim_utils.get_swimmers_data(swimmer)[0])
    return render_template(
        "select.html",
        title="Select a swimmer to chart",
        data=sorted(names),
    )


@app.get("/chart")
def display_chart():
    (
        name,
        age,
        distance,
        stroke,
        the_times,
        converts,
        the_average,
    ) = swim_utils.get_swimmers_data("Darius-13-100m-Fly.txt")

    the_title = f"{name} (Under {age}) {distance} {stroke}"
    from_max = max(converts) + 50
    the_converts = [hfpy_utils.convert2range(n, 0, from_max, 0, 350) for n in converts]

    the_data = zip(the_converts, the_times)

    return render_template(
        "chart.html",
        title=the_title,
        average=the_average,
        data=the_data,
    )


@app.route("/displayevents", methods=["GET", "POST"])
def display_events():
    files = os.listdir(swim_utils.FOLDER)
    files.remove(".DS_Store")
    swimmers_data = [swim_utils.get_swimmers_data(swimmer) for swimmer in files]

    return render_template(
        "events.html",
        title="Select an event to chart",
        swimmers_data=swimmers_data,
    )


@app.route("/events", methods=["POST"])
def events():
    selected_swimmer = request.form["swimmer"]
    selected_event = request.form["events"]

    # Do processing based on the selected swimmer and event

    return redirect(url_for("display_events", selected_swimmer=selected_swimmer))


if __name__ == "__main__":
    app.run(debug=True)
