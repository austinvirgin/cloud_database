import firebase_admin
from firebase_admin import firestore, credentials
from google.cloud.firestore_v1.base_query import FieldFilter
import os

def main():
    # Give the main screen
    welcome = int(input("Would you like to (1) login or (2) signup? "))

    # See where they want to go
    match welcome:
        case 1:
            clear_terminal()
            login()
        case 2:
            clear_terminal()
            signup()
        case _:
            print("Invalid input, please try again.")

def clear_terminal():
    os.system('cls')

def login():

    # Initalize the while loop
    user_found = False
    while user_found == False:

        # Ask for their username
        username = input("What is your username? ")

        # Get the user reference and check if the user exists
        user_ref = db.collection('users').document(username)
        user = user_ref.get()
        clear_terminal()
        if not user.exists:
            invalid_user()
        else:
            user_found = True

    # Check if logged in if so go into the user
    logged_in = password_login(user)
    if logged_in:
        logged_in_user(user)
    else:
        print("you scammer get out of here")

    
def password_login(user):

    # Initalize the password checker
    password_input = None
    password = user._data['password']
    password_tries = 0

    # Give the user 3 tries to log in
    while password_tries < 3:
        if password_tries > 0:
            print(f"{3. - password_tries} more tries")
        password_input = input("What is your password? ")
        clear_terminal()
        if password_input == password:
            return True
        password_tries += 1
    return False
            
def invalid_user():

    # Let them know they got an invalid username
    retry = input("Invalid username do you want to (1) try again or (2) make a new account? ")
    match retry:
        case 1:
            clear_terminal()
            return
        case 2:
            clear_terminal()
            signup()
        case _:
            print("Invalid input, please try again.")


def signup():

    # Ask for a username that does not already exist and check
    new_username = input("What would you like your username to be? ")
    while exists_username(new_username):
        print("This username has already been taken please try again")
        new_username = input("What would you like your username to be? ")

    clear_terminal()

    # Add the username, their password, and their information
    doc_ref = db.collection("users").document(new_username)
    first = input("What is your first name? ").capitalize()
    last = input("What is your last name? ").capitalize()
    birth_year = int(input("What is your birth year? "))
    password = input("What would you like your password to be? ")
    doc_ref.set({"first_name": first, "last_name": last, "birth_year": birth_year, 'password': password})
    print("Congrats you have made an account!")
    clear_terminal()
    login()


def exists_username(username):
    
    # Check if the username already exists
    user_ref = db.collection("users").document(username)
    user = user_ref.get()
    clear_terminal()
    return user.exists

def logged_in_user(user):

    #Welcome the user to being logged in
    print(f"Welcome {user._data['first_name']} {user._data['last_name']}")
    logged_in_choices(user)

def get_posts(user):

    # Get the username and look for the posts that have their username
    username = user.id
    posts_ref = db.collection("posts")
    query = posts_ref.where(filter=FieldFilter("username", "==", f"{username}"))

    # Get all of their posts
    results = query.stream()
    for result in results:
        print(f"Title: {result._data['title']}")
        print(f"{result._data['post_text']}")

    input("Press enter to continue...")
    clear_terminal()

def update_user_profile(user):

    # Give all of the user fields and ask what they would like to change
    print("Which field would you like to change? Choose the number corresponding with the data you would like to change.")
    fields = {}
    i = 0
    for field in user._data:
        if field != 'friends':
            print(f'\t({i}) {field}', end = " ")
            fields[i] = field
        i += 1
    print()
    to_change = int(input("Which one would you like to change? "))
    to_change = fields[to_change]
    new_value = input("What is the new value? ")
    user.reference.update({f"{to_change}": f"{new_value}"})

def logged_in_choices(user):

    # Display all of the users choices and see what they would like to do
    print("\nWhat would you like to do?")
    user_choice = 0
    while user_choice != 8:
        choices = ("add a friend", "get a list of your friends", "look at a friends posts", "add a post", "get posts", "update your profile", "delete account", "quit")
        choice_amount = len(choices) - 1
        count = 0
        for choice in choices:
            if choice_amount == count:
                print(f"or ({count + 1}) {choice}", end = "? ")

            else:
                print(f"({count + 1}) {choice}", end = ", ")

            count += 1
        user_choice = int(input(""))
        clear_terminal()
        match user_choice:
            case 1:
                add_friend(user)

            case 2:
                list_friends(user)

            case 3:
                friends_posts(user)

            case 4:
                add_post(user)

            case 5:
                get_posts(user)

            case 6:
                update_user_profile(user)

            case 7:
                delete_account(user)

            case 8:        
                print(f"Goodbye, {user._data['first_name']}")
                return

def add_friend(user):

    # Check if the friend exist and add him to the friends array
    user_ref = db.collection('users').document(f'{user.id}')
    friend = input("What is your friend's username? ")
    while not exists_username(friend):
        print("invalid username")
        friend = input("What is your friend's username? ")
    clear_terminal()
    user_ref.update({"friends": firestore.ArrayUnion([f'{friend}'])})
    print(f"{friend} has been added")

def list_friends(user):
    # Print out all friends
    friends = user._data['friends']
    num_friend = 0
    for friend in friends:
        print(f"({num_friend + 1}) {friend}", end = "\t")
    print()

    input("Press enter to continue...")
    clear_terminal()

def friends_posts(user):

    # Ask for the friend they would like to look at
    print("Please choose the friend's number whose posts you would like to look at")
    list_friends(user)

    # Get the friends data and show their posts
    friends = user._data['friends']
    friend = int(input("What friend would you like to look at? ")) - 1
    friend = friends[friend]
    friend_ref = db.collection('users').document(f"{friend}")
    friend_ref = friend_ref.get()
    get_posts(friend_ref)

    input("Press enter to continue...")
    clear_terminal()

def add_post(user):

    # Get all of the info to add a post
    posts_ref = db.collection('posts')
    new_post = posts_ref.document()
    username  = user.id
    title = input("What would you like the title to be? ")
    post_text = input("What would you like the post to say? ")
    new_post.set({"username": username, "post_text": post_text, "title": title})
    clear_terminal()

def delete_account(user):

    # Delete the users account
    username = user.id
    user_ref = db.collection('users').document(f"{username}")
    user_ref.delete()
    print(f"user {username} has been deleted")

cred = credentials.Certificate("websitewithpython-firebase-adminsdk-fbsvc-f6bb45bbc4.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()


if __name__ == "__main__":
    main()