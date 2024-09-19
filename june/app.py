from flask import Flask, render_template_string, request

app = Flask(__name__)

# HTML template with embedded CSS
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Grade Computation Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }

        h1 {
            text-align: center;
            color: #333;
        }

        form {
            display: flex;
            flex-direction: column;
            margin-bottom: 20px;
        }

        input[type="number"] {
            padding: 10px;
            margin: 10px 0;
            font-size: 1em;
            border: 1px solid #ddd;
            border-radius: 5px;
        }

        button {
            background: #28a745;
            color: white;
            padding: 10px;
            border: none;
            cursor: pointer;
            font-size: 1em;
            border-radius: 5px;
        }

        button:hover {
            background: #218838;
        }

        .result, .error {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #ddd;
            background: #f8f8f8;
        }

        .error {
            color: #d9534f;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Grade Computation Tool</h1>
        <form method="POST" action="/">
            <label for="prelim_grade">Enter your Prelim Grade:</label>
            <input type="number" name="prelim_grade" id="prelim_grade" min="0" max="100" step="0.01" required>
            <button type="submit">Calculate</button>
        </form>

        {% if error %}
        <div class="error">
            <p>{{ error }}</p>
        </div>
        {% endif %}

        {% if prelim_grade is not none %}
        <div class="result">
            <h3>Results:</h3>
            <p>Prelim Grade: {{ prelim_grade }}</p>
            <p>Required Midterm Grade: {{ midterm_required }}</p>
            <p>Required Final Grade: {{ final_required }}</p>
            <p>{{ message }}</p>
            <p>Dean's Lister Status: {{ dean_lister_message }}</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Get the prelim grade from the form
            prelim_grade = float(request.form['prelim_grade'])
            
            if prelim_grade < 0 or prelim_grade > 100:
                raise ValueError("Grade must be between 0 and 100")

            # Define grade weights
            prelim_weight = 0.20
            midterm_weight = 0.30
            final_weight = 0.50
            passing_grade = 75
            dean_lister_threshold = 90

            # Calculate prelim contribution
            prelim_contribution = prelim_grade * prelim_weight

            # Calculate required total contribution to reach passing grade
            required_total_contribution = passing_grade - prelim_contribution
            
            # Calculate required grades
            if required_total_contribution <= 0:
                midterm_required = final_required = "N/A"
                chance_to_pass = "You have a chance to pass!"
            else:
                combined_weight = midterm_weight + final_weight
                required_combined_avg = required_total_contribution / combined_weight
                midterm_required = round(required_combined_avg * midterm_weight, 2)
                final_required = round(required_combined_avg * final_weight, 2)

                if midterm_required > 100 or final_required > 100:
                    midterm_required = final_required = "N/A"
                    chance_to_pass = "It is difficult to pass. Required grades exceed maximum limit."
                else:
                    chance_to_pass = "You have a chance to pass!"

            # Calculate Dean's Lister requirements
            required_for_dean = dean_lister_threshold - prelim_contribution
            if required_for_dean <= 0:
                dean_lister_message = "Already qualified for Dean’s Lister with current Prelim grade."
            else:
                dean_combined_weight = midterm_weight + final_weight
                dean_midterm_required = round(required_for_dean * midterm_weight / dean_combined_weight, 2)
                dean_final_required = round(required_for_dean * final_weight / dean_combined_weight, 2)

                if dean_midterm_required > 100 or dean_final_required > 100:
                    dean_lister_message = "Not possible to achieve Dean’s Lister with current Prelim grade."
                else:
                    dean_lister_message = f"Required: {dean_midterm_required} (Midterm) and {dean_final_required} (Final)."

            return render_template_string(
                HTML_TEMPLATE,
                prelim_grade=prelim_grade,
                midterm_required=midterm_required,
                final_required=final_required,
                message=chance_to_pass,
                dean_lister_message=dean_lister_message
            )
        except ValueError:
            error_message = "Please enter a valid numerical input between 0 and 100."
            return render_template_string(HTML_TEMPLATE, error=error_message)
    else:
        return render_template_string(HTML_TEMPLATE)

if __name__ == '__main__':
    app.run(debug=True)



