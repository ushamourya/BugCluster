import csv
import random
from pathlib import Path

random.seed(42)

# ==========================================
# BugCluster - Synthetic Dataset Generator
# ==========================================

OUTPUT_PATH = Path("raw/bugs_large.csv")

developers = {
    "Authentication": "Rahul",
    "Payment": "Arjun",
    "Frontend": "Sneha",
    "Dashboard": "Priya",
    "Search": "Vikram",
    "Notifications": "Priya",
    "API": "Arjun",
    "Database": "Vikram",
    "Performance": "Priya",
    "File Upload": "Sneha",
}

bug_templates = {
    "Authentication": [
        ("Login page crashes", "Application crashes when users attempt to log in"),
        ("Password reset fails", "Users cannot complete the password reset process"),
        ("Invalid login error", "Valid credentials result in an unexpected authentication error"),
        ("Session expires unexpectedly", "Users are logged out while actively using the application"),
        ("Logout not working", "Logout action does not terminate the user session"),
        ("Two factor authentication fails", "Verification code is rejected even when it is valid"),
        ("Account lockout issue", "User account becomes locked after a normal login attempt"),
        ("Authentication timeout", "Login request takes too long and eventually times out"),
    ],

    "Payment": [
        ("Payment failure", "Credit card payment fails during checkout"),
        ("Checkout payment crash", "Checkout crashes when selecting a payment method"),
        ("Payment timeout", "Payment request remains pending and eventually times out"),
        ("Missing payment receipt", "Customers do not receive a receipt after payment"),
        ("Duplicate payment", "The same transaction is charged more than once"),
        ("Refund failure", "Refund request fails and the amount is not returned"),
        ("Card validation error", "Valid card details are incorrectly rejected"),
        ("Payment status incorrect", "Successful payments are displayed as failed"),
    ],

    "Frontend": [
        ("Button not working", "Submit button does not respond when clicked"),
        ("Mobile layout broken", "Page layout breaks on smaller mobile screens"),
        ("Broken navigation menu", "Navigation menu does not open correctly"),
        ("Form alignment issue", "Form fields are incorrectly aligned on the page"),
        ("Missing UI element", "Expected interface element is not displayed"),
        ("Modal does not close", "Popup remains visible after clicking the close button"),
        ("Text overlaps", "Page text overlaps with other interface elements"),
        ("Responsive layout issue", "Interface behaves incorrectly at different screen sizes"),
    ],

    "Dashboard": [
        ("Slow dashboard", "Dashboard takes too long to load its widgets"),
        ("Dashboard widgets missing", "Some dashboard widgets are not displayed"),
        ("Dashboard data incorrect", "Dashboard displays outdated information"),
        ("Dashboard layout issue", "Widgets overlap when the dashboard is loaded"),
        ("Dashboard loading error", "Dashboard fails while retrieving summary data"),
        ("Chart not displaying", "Analytics chart remains blank after loading"),
        ("Dashboard filter broken", "Dashboard filters do not update displayed data"),
        ("Dashboard refresh issue", "Refreshing the dashboard does not update metrics"),
    ],

    "Search": [
        ("Search is slow", "Search takes too long to return results"),
        ("Search returns wrong results", "Search displays unrelated results"),
        ("Search returns no results", "Existing records cannot be found through search"),
        ("Search filter broken", "Search filters do not correctly narrow results"),
        ("Search ranking incorrect", "Relevant results appear below unrelated results"),
        ("Search query error", "Certain search queries cause an unexpected error"),
        ("Search suggestions missing", "Autocomplete suggestions are not displayed"),
        ("Search pagination broken", "Search results pagination does not work correctly"),
    ],

    "Notifications": [
        ("Duplicate notification", "Users receive the same notification multiple times"),
        ("Notification missing", "Expected notifications are not delivered"),
        ("Notification delayed", "Notifications arrive several minutes late"),
        ("Wrong notification", "Users receive notifications intended for another event"),
        ("Email notification failure", "Notification emails are not sent successfully"),
        ("Push notification broken", "Push notifications do not appear on mobile devices"),
        ("Notification preference ignored", "Disabled notifications continue to be delivered"),
        ("Notification formatting issue", "Notification content is displayed incorrectly"),
    ],

    "API": [
        ("API returns 500 error", "API request fails with an internal server error"),
        ("API timeout", "API request takes too long and times out"),
        ("Invalid API response", "API returns an unexpected response structure"),
        ("Missing API field", "Expected field is missing from the API response"),
        ("API authentication failure", "Authenticated API requests are rejected"),
        ("API endpoint unavailable", "Expected API endpoint cannot be reached"),
        ("API rate limit issue", "Requests are incorrectly blocked by rate limiting"),
        ("API request validation failure", "Valid API requests fail validation"),
    ],

    "Database": [
        ("Database connection failure", "Application cannot connect to the database"),
        ("Database query slow", "Database query takes too long to complete"),
        ("Missing database record", "Expected record cannot be retrieved from the database"),
        ("Duplicate database record", "The same record is inserted multiple times"),
        ("Database update failure", "Changes are not saved correctly in the database"),
        ("Database timeout", "Database operation exceeds the expected response time"),
        ("Incorrect database value", "Stored value does not match the submitted data"),
        ("Database migration error", "Database migration fails during deployment"),
    ],

    "Performance": [
        ("Page loads slowly", "Application page takes too long to load"),
        ("High memory usage", "Application consumes excessive memory during normal usage"),
        ("CPU usage spike", "CPU usage becomes unusually high during requests"),
        ("Slow response time", "Application responses take several seconds"),
        ("Application freezes", "Application becomes unresponsive during normal usage"),
        ("Large data processing slow", "Processing large datasets takes too long"),
        ("Performance degradation", "Application becomes slower after extended usage"),
        ("Resource usage increase", "System resource consumption increases unexpectedly"),
    ],

    "File Upload": [
        ("File upload fails", "Users cannot upload supported files"),
        ("Large file upload timeout", "Large files fail to upload before completion"),
        ("Invalid file accepted", "Application accepts files with unsupported formats"),
        ("Uploaded file missing", "Successfully uploaded file cannot be found"),
        ("File upload crash", "Application crashes while uploading a file"),
        ("File upload progress broken", "Upload progress indicator does not update"),
        ("Duplicate file upload", "The same file is uploaded multiple times"),
        ("File size validation issue", "File size restrictions are not applied correctly"),
    ],
}


priorities = ["High", "Medium", "Low"]
severities = ["Critical", "Major", "Minor"]
statuses = ["Open", "Open", "Open", "Closed"]

rows = []

bug_number = 1

components = list(bug_templates.keys())

while len(rows) < 150:

    component = components[(bug_number - 1) % len(components)]

    title, description = random.choice(
        bug_templates[component]
    )

    priority = random.choices(
        priorities,
        weights=[3, 5, 2]
    )[0]

    severity = random.choices(
        severities,
        weights=[2, 6, 2]
    )[0]

    status = random.choice(statuses)

    developer = developers[component]

    rows.append([
        f"BUG-{bug_number:03d}",
        title,
        description,
        priority,
        severity,
        component,
        status,
        developer,
    ])

    bug_number += 1


# ==========================================
# Create output directory
# ==========================================

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


# ==========================================
# Write CSV
# ==========================================

with open(
    OUTPUT_PATH,
    "w",
    newline="",
    encoding="utf-8"
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "bug_id",
        "title",
        "description",
        "priority",
        "severity",
        "component",
        "status",
        "developer",
    ])

    writer.writerows(rows)


print("===================================")
print("Dataset generated successfully!")
print("===================================")
print("Total bugs:", len(rows))
print("Components:", len(components))
print("Output:", OUTPUT_PATH)
print("===================================")
