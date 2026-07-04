from backend.app.core.database import get_database
from backend.app.models.user import UserCreate, UserDB
from backend.app.utils.security import hash_password


class UserRepository:

    @staticmethod
    async def get_user_by_email(email: str):
        db = get_database()
        user_doc = await db.users.find_one({"email": email})
        return user_doc

    @staticmethod
    async def create_user(user: UserCreate):
        db = get_database()

        user_data = user.model_dump()

        password = user_data.pop("password")

        new_user = UserDB(
            **user_data,
            hashed_password=hash_password(password)
        )

        await db.users.insert_one(
            new_user.model_dump(by_alias=True)
        )

        return new_user