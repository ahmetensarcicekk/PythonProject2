import json
import os
from datetime import datetime

DATA_FILE = "study_group.json"


# --- Data Management (Ensar) ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


# --- Add a Subject (Sude) ---
def add_subject(data, user):
    subject = input("📘 Enter new subject name: ").strip()
    if not subject:
        print("⚠️ Subject name cannot be empty.")
        return
    if subject in data["subjects"]:
        print("❗ This subject already exists.")
    else:
        data["subjects"][subject] = {}
        print(f"✅ '{subject}' has been added successfully.")
    save_data(data)


# --- List All Subjects (Yağız) ---
def list_subjects(data):
    print("\n📚 Current Subjects:")
    if not data["subjects"]:
        print("⚠️ No subjects have been added yet.")
    else:
        for i, subject in enumerate(data["subjects"].keys(), 1):
            print(f"{i}. {subject}")
    print("────────────────────────────\n")


# --- Log Study Time (Burak) ---
def log_study_time(data, user):
    if not data["subjects"]:
        print("⚠️ No subjects yet. Please add one first.")
        return

    list_subjects(data)
    subject = input("Which subject do you want to log time for? ").strip()
    if subject not in data["subjects"]:
        print("❌ Subject not found.")
        return

    try:
        minutes = int(input("How many minutes did you study?: "))
    except ValueError:
        print("⚠️ Please enter a valid number.")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    if user not in data["subjects"][subject]:
        data["subjects"][subject][user] = []

    data["subjects"][subject][user].append({"minutes": minutes, "time": now})
    save_data(data)
    print(f"🕒 {minutes} minutes logged for '{subject}' by {user}.")


# --- Show Group Report (Eren) ---
def show_report(data):
    print("\n📊 GROUP STUDY REPORT 📊")
    total_all = 0
    for subject, users in data["subjects"].items():
        print(f"\n📘 {subject}:")
        subject_total = 0
        for user, records in users.items():
            total_user = sum(r["minutes"] for r in records)
            print(f"   - {user}: {total_user} min")
            subject_total += total_user
        print(f"   🔹 Total: {subject_total} min")
        total_all += subject_total
    print(f"\n💯 Group Total: {total_all} minutes")
    print("────────────────────────────\n")


# --- Show Individual Report (Ensar) ---
def user_report(data, user):
    print(f"\n📈 {user.upper()}'S STUDY REPORT 📈")
    total = 0
    for subject, users in data["subjects"].items():
        if user in users:
            minutes = sum(r["minutes"] for r in users[user])
            print(f"- {subject}: {minutes} min")
            total += minutes
    print(f"\nTotal: {total} minutes")
    print("────────────────────────────\n")


# --- Delete a Subject (Yağız) ---
def delete_subject(data):
    if not data["subjects"]:
        print("⚠️ No subjects yet.")
        return

    list_subjects(data)
    subject = input("Enter subject name to delete: ").strip()
    if subject in data["subjects"]:
        confirm = input(f"Are you sure you want to delete '{subject}'? (Y/n): ").lower()
        if confirm == "y":
            del data["subjects"][subject]
            save_data(data)
            print(f"🗑️ '{subject}' has been deleted.")
        else:
            print("❎ Deletion canceled.")
    else:
        print("❌ Subject not found.")


# --- Display Box Menu (Burak) ---
def show_menu(user):
    # Clear screen each time (works on Windows and macOS/Linux)
    os.system('cls' if os.name == 'nt' else 'clear')

    print("╔════════════════════════════════════╗")
    print("║        📘 STUDY ORGANIZER 📘        ║")
    print("╠════════════════════════════════════╣")
    print(f"║ 👤 User: {user:<28}║")
    print("╠════════════════════════════════════╣")
    print("║ 1️⃣  Add subject                    ║")
    print("║ 2️⃣  List subjects                  ║")
    print("║ 3️⃣  Log study time                 ║")
    print("║ 4️⃣  View personal report           ║")
    print("║ 5️⃣  View group report              ║")
    print("║ 6️⃣  Delete subject                 ║")
    print("║ 7️⃣  Exit                           ║")
    print("╚════════════════════════════════════╝")


# --- Main Function ---
def main():
    data = load_data()
    if "subjects" not in data:
        data["subjects"] = {}

    print("👋 Welcome to Study Organizer!")
    user = input("Enter your name: ").strip()
    if not user:
        user = "Unknown"

    while True:
        show_menu(user)
        choice = input("👉 Choose an option (1-7): ").strip()

        if choice == "1":
            add_subject(data, user)
        elif choice == "2":
            list_subjects(data)
        elif choice == "3":
            log_study_time(data, user)
        elif choice == "4":
            user_report(data, user)
        elif choice == "5":
            show_report(data)
        elif choice == "6":
            delete_subject(data)
        elif choice == "7":
            print("👋 Exiting... Data saved successfully.")
            break
        else:
            print("⚠️ Invalid choice. Please select between 1–7.")


if __name__ == "__main__":
    main()