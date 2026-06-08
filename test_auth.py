from auth import sign_up

print("Auth loaded successfully")

user = sign_up(
    "bhavyasriboddeti16@gmail.com",
    "Bhavyasri@2006"
)

if user:
    print("User created successfully")
else:
    print("Failed to create user")