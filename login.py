import firebase_admin
from firebase_admin import firestore, credentials

def main():
    welcome = int(input("Would you like to (1) login or (2) signup? "))

    match welcome:
        case 1:
            login()
        case 2:
            signup()
        case _:
            print("Invalid input, please try again.")

def login():
    print("Welcome!")
    user_found = False
    while user_found == False:
        username = input("What is your username? ")
        user_ref = db.collection('users').document(username)
        user = user_ref.get()
        
        if not user.exists:
            invalid_user()

        else:
            user_found = True

    logged_in = password_login(user)
    
    if logged_in:
        logged_in_user(user)

    else:
        print("you scammer get out of here")

    
def password_login(user):
    password_input = None
    password = user._data['password']
    password_tries = 0
    while password_tries < 3:
        if password_tries > 0:
            print(f"{3. - password_tries} more tries")
        password_input = input("What is your password? ")
        if password_input == password:
            return True
        password_tries += 1
    return False
            
def invalid_user():
    retry = input("Invalid username do you want to (1) try again or (2) make a new account? ")
    match retry:
        case 1:
            return
        case 2:
            signup()
        case _:
            print("Invalid input, please try again.")

def signup():
    new_username = input("What would you like your username to be? ")
    while already_used(new_username):
        print("This username has already been taken please try again")
        new_username = input("What would you like your username to be? ")
    doc_ref = db.collection("users").document(new_username)
    first = input("What is your first name? ").capitalize()
    last = input("What is your last name? ").capitalize()
    birth_year = int(input("What is your birth year? "))
    password = input("What would you like your password to be? ")
    # symbol = False
    # number = False
    # for letter in password:
    doc_ref.set({"first_name": first, "last_name": last, "birth_year": birth_year, 'password': password})


def already_used(new_username):
    user_ref = db.collection("users").document(new_username)
    user = user_ref.get()
    return user.exists

def logged_in_user(user):
    print(f"Welcome {user._data['first_name']} {user._data['last_name']}")
    update = int(input("Is there anything you would like to update (0) No, (1) Yes? "))
    match update:
        case 0:
            get_posts(user)

        case 1:
            update_database(user)
            get_posts(user)

        case _:
            print("This is invalid")

def get_posts(user):
    username = user.id
    posts_ref = db.collection("posts")
    query = posts_ref.where("username", "==", f"{username}")
    results = query.stream()

    for result in results:
        print(f"Title: {result._data['title']}")
        print(f"{result._data['post_text']}")

def update_database(user):
    print("Which field would you like to change? Choose the number corresponding with the data you would like to change.")
    fields = {}
    i = 0
    for field in user._data:
        print(f'\t({i}) {field}', end = " ")
        fields[i] = field
        i += 1
    print()
    to_change = int(input("Which one would you like to change? "))
    to_change = fields[to_change]
    new_value = input("What is the new value? ")
    user.reference.update({f"{to_change}": f"{new_value}"})

cred = credentials.Certificate("C:/Users/austi/Documents/Programming/cloud_database/websitewithpython-firebase-adminsdk-fbsvc-f6bb45bbc4.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

main()