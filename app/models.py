try:
    from app.database import Base
except ImportError:
    from database import Base

from sqlalchemy import Column, Integer, Float, String, TIMESTAMP, ForeignKey, text
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    # Store progress as a JSON object for detailed progress tracking
    progress = Column(JSONB, nullable=False, server_default=text("'{}'::jsonb"))
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('CURRENT_TIMESTAMP'), nullable=False)


class Module(Base):
    __tablename__ = "modules"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)

    chapters = relationship("Chapter", back_populates="module")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, nullable=False)
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    module = relationship("Module", back_populates="chapters")
    quizzes = relationship("Quiz", back_populates="chapter")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, nullable=False)
    chapter_id = Column(Integer, ForeignKey("chapters.id"), nullable=False)
    question = Column(String, nullable=False)
    option_a = Column(String, nullable=False)
    option_b = Column(String, nullable=False)
    option_c = Column(String, nullable=False)
    correct_option = Column(String, nullable=False)
    hint_a = Column(String, nullable=True)
    hint_b = Column(String, nullable=True)
    hint_c = Column(String, nullable=True)

    chapter = relationship("Chapter", back_populates="quizzes")


class NeoverseLog(Base):
    __tablename__ = "neoverse_logs"

    player_id = Column(String, primary_key=True, nullable=False)
    timestamp = Column(TIMESTAMP, nullable=False)
    hours_played = Column(Integer, nullable=False)
    money_spent = Column(Integer, nullable=False)
    criminal_score = Column(Integer, nullable=False)
    missions_completed = Column(Integer, nullable=False)
    player_rank = Column(String, nullable=False)
    team_affiliation = Column(String, nullable=False)
    vip_status = Column(String, nullable=False)
    cash_on_hand = Column(Integer, nullable=False)
    sync_stability = Column(Float, nullable=False)
    quest_exploit_score = Column(Integer, nullable=False)
    player_level = Column(String, nullable=False)
    dark_market_transactions = Column(String, nullable=False)
    transaction_amount = Column(Integer, nullable=False)
    neural_link_stability = Column(Float, nullable=False)
