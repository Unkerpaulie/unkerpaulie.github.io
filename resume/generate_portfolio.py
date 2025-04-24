import json
from datetime import UTC, datetime
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


# Resume data source
src = "corey"

# Load JSON data
with Path(src, "portfolio.json").open(encoding="utf-8") as f:
    data = json.load(f)

# Add any extra context if needed
data["current_year"] = datetime.now(tz=UTC).year
data["image_folder"] = src

if "social_links" in data:
    for link in data["social_links"]:
        if link.get("svg_path"):
            with Path(link["svg_path"]).open(encoding="utf-8") as svg_file:
                link["svg_data"] = svg_file.read()

# Set up Jinja environment
env = Environment(loader=FileSystemLoader("."), autoescape=True)
resume_template = env.get_template("templates/resume_template.html")
simple_template = env.get_template("templates/simple_template.html")

# Render the template with the data
resume_output = resume_template.render(**data)
simple_output = simple_template.render(**data)

# This is equivalent to...
# resume_output = resume_template.render(name=data["name"], label=data["label"]...)
# simple_output = simple_template.render(name=data["name"], label=data["label"]...)

# Write the output to an HTML file
with Path("index.html").open("w", encoding="utf-8") as f:
    f.write(resume_output)

with Path("simple.html").open("w", encoding="utf-8") as f:
    f.write(simple_output)

print("HTML file generated successfully!")
