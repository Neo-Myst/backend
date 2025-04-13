from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# User Schema
class UserBase(BaseModel):
    username: str
    email: EmailStr
    password: str

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


class CreateUser(UserBase):
    pass  # Inherits all fields and configurations from UserBase


class LoginUser(BaseModel):
    username_or_email: str
    password: str

    model_config = ConfigDict(
        from_attributes=False,
        populate_by_name=True
    )

class Progress(BaseModel):
    current_module: str
    current_chapter: int

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class UserProgressUpdate(BaseModel):
    progress: Progress

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )


# Module Schema
class ModuleBase(BaseModel):
    title: str
    description: str


class ModuleResponse(ModuleBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Chapter Schema
class ChapterBase(BaseModel):
    module_id: int
    title: str
    content: str


class ChapterResponse(ChapterBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Quiz Schema
class QuizBase(BaseModel):
    chapter_id: int
    question: str
    option_a: str
    option_b: str
    option_c: str
    hint_a: Optional[str] = None
    hint_b: Optional[str] = None
    hint_c: Optional[str] = None


class QuizCreate(QuizBase):
    correct_option: str


class QuizResponse(QuizBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
