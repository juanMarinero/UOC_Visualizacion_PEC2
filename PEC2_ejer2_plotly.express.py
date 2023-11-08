#!/usr/bin/env python3

#  vim: set foldmethod=indent foldcolumn=4 :

import pandas as pd
import plotly.express as px


def create_gantt_chart(data):
    # Expand rows to individual pairs of start-end dates
    rows = []
    for _, row in data.iterrows():
        if not isinstance(row["start"], list):
            row["start"] = [row["start"]]
        if not isinstance(row["end"], list):
            row["end"] = [row["end"]]
        for start, end in zip(row["start"], row["end"]):
            rows.append(
                {
                    "sub-project": row["sub-project"],
                    "start": start,
                    "end": end,
                    "genre": row["genre"],
                }
            )

    # Create an interactive Gantt chart
    expanded_data = pd.DataFrame(rows)
    print("expanded_data:", expanded_data)
    expanded_data["start"] = pd.to_datetime(expanded_data["start"])
    expanded_data["end"] = pd.to_datetime(expanded_data["end"])

    fig = px.timeline(
        expanded_data,
        x_start="start",
        x_end="end",
        y="sub-project",
        color="genre",
        title="Google-dataset sports Gantt Chart",
    )

    # Customize the figure layout
    fig.update_layout(xaxis_title="Timeline", yaxis_title="Tasks", xaxis_type="date")

    # Show the Gantt chart
    fig.show()


def get_df():
    df = pd.DataFrame(
        {
            "sub-project": [
                "Spring 2014",
                "Summer 2014",
                "Autumn 2014",
                "Winter 2014",
                "Spring 2015",
                "Summer 2015",
                "Autumn 2015",
                "Winter 2015",
                "Football Season",
                "Baseball Season",
                "Basketball Season",
                "Hockey Season",
            ],
            "start": [
                "2014-02-22",
                ["2014-05-21", "2014-06-21"],
                "2014-08-21",
                "2014-11-21",
                "2015-02-22",
                "2015-05-21",
                "2015-08-21",
                "2015-11-21",
                "2014-08-4",
                "2015-02-28",
                "2014-09-28",
                "2014-09-8",
            ],
            "end": [
                "2014-05-20",
                ["2014-05-30", "2014-08-20"],
                "2014-11-20",
                "2015-02-21",
                "2015-05-20",
                "2015-08-20",
                "2015-11-20",
                "2016-02-21",
                "2015-01-1",
                "2015-09-20",
                "2015-05-20",
                "2015-05-21",
            ],
            "genre": [
                "spring",
                "summer",
                "autumn",
                "winter",
                "spring",
                "summer",
                "autumn",
                "winter",
                "sports",
                "sports",
                "sports",
                "sports",
            ],
        }
    )
    df["start"].iloc[-1] = ["2014-09-8", "2014-10-20", "2014-11-25", "2015-01-20"]
    df["end"].iloc[-1] = ["2014-10-8", "2014-11-20", "2014-12-25", "2015-02-20"]
    return df


def main():
    #  https://developers.google.com/chart/interactive/docs/gallery/ganttchart#no-dependencies

    df = get_df()

    create_gantt_chart(df)


if __name__ == "__main__":
    main()
