# encode_credentials.py

from urllib.parse import quote_plus

# --- IMPORTANT ---
# Enter your actual MongoDB username and password here
# This script is run locally and will not be part of your main app
# so it's safe to temporarily hardcode them here for this one-time task.

my_username = "kothasanthan39"
my_password = "mongodb+srv://kothasanthan39:159159@Lsh@cluster0.9tk9zft.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# This function will encode the special characters
encoded_username = quote_plus(my_username)
encoded_password = quote_plus(my_password)

print("--- Use these in your connection string ---")
print(f"Encoded Username: {encoded_username}")
print(f"Encoded Password: {encoded_password}")
print("\n--- Example Connection String ---")
print(f"mongo_uri = \"mongodb+srv://{encoded_username}:{encoded_password}@your_cluster.xxxxx.mongodb.net/?retryWrites=true&w=majority\"")

