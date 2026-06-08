from firestore_db import db

db.collection("test").document("sample").set({
    "message": "ResolveIQ connected successfully"
})

print("Success!")