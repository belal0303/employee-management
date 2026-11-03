from flask import Flask, render_template_string

app = Flask(__name__)

employees = [
    {"id": 1, "name": "gokul", "role": "DevOps Engineer"},
    {"id": 2, "name": "yuva", "role": "Python Developer"},
    {"id": 3, "name": "krishna", "role": "Cloud Engineer"}
]

html = """
<!DOCTYPE html>
<html>
<head>
    <title>one data software solution</title>
</head>
<body>
    <h1>one data company</h1>
    <h2>Employee Management System</h2>

    <table border="1" cellpadding="10">
        <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Role</th>
        </tr>

        {% for employee in employees %}
        <tr>
            <td>{{ employee.id }}</td>
            <td>{{ employee.name }}</td>
            <td>{{ employee.role }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html, employees=employees)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

