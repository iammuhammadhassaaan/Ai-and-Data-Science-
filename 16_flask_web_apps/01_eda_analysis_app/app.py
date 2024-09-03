from flask import Flask, render_template, request, send_file, Response
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64

app = Flask(__name__)

# List of datasets available in Seaborn
datasets = ["iris", "titanic", "tips", "penguins", "diamonds"]

# Route to the main page
@app.route("/", methods=["GET", "POST"])
def index():
    selected_dataset = request.form.get("dataset")
    plot_type = request.form.get("plot_type")
    x_column = request.form.get("x_column")
    y_column = request.form.get("y_column")
    
    data = None
    columns = []
    plot_url = None
    
    if selected_dataset:
        # Load selected dataset
        data = sns.load_dataset(selected_dataset)
        columns = data.columns.tolist()
        
        if plot_type and x_column and y_column:
            # Generate the selected plot type
            plt.figure(figsize=(10, 6))
            if plot_type == "scatter":
                sns.scatterplot(data=data, x=x_column, y=y_column)
            elif plot_type == "line":
                sns.lineplot(data=data, x=x_column, y=y_column)
            elif plot_type == "bar":
                sns.barplot(data=data, x=x_column, y=y_column)
            elif plot_type == "hist":
                sns.histplot(data=data[x_column])
            elif plot_type == "box":
                sns.boxplot(data=data, x=x_column, y=y_column)
            
            # Save the plot to a BytesIO object
            img = io.BytesIO()
            plt.savefig(img, format="png")
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode('utf8')
            plt.close()  # Close the plot to avoid memory leaks
    
    return render_template("index.html", datasets=datasets, columns=columns, plot_url=plot_url)

# Route to download the generated plot
@app.route("/download_plot")
def download_plot():
    plot_type = request.args.get("plot_type")
    x_column = request.args.get("x_column")
    y_column = request.args.get("y_column")
    selected_dataset = request.args.get("dataset")
    
    data = sns.load_dataset(selected_dataset)
    
    plt.figure(figsize=(10, 6))
    if plot_type == "scatter":
        sns.scatterplot(data=data, x=x_column, y=y_column)
    elif plot_type == "line":
        sns.lineplot(data=data, x=x_column, y=y_column)
    elif plot_type == "bar":
        sns.barplot(data=data, x=x_column, y=y_column)
    elif plot_type == "hist":
        sns.histplot(data=data[x_column])
    elif plot_type == "box":
        sns.boxplot(data=data, x=x_column, y=y_column)
    
    img = io.BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    
    return send_file(img, mimetype="image/png", as_attachment=True, download_name="plot.png")

if __name__ == "__main__":
    app.run(debug=True)
