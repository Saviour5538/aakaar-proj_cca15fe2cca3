import uuid
from datetime import datetime
from database.models import Base, engine, SessionLocal, User, Document, Chunk, Conversation, Message
from sqlalchemy.exc import SQLAlchemyError

def seed_database():
    session = SessionLocal()
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)

        # Seed Users
        user1 = User(
            id=str(uuid.uuid4()),
            email="alice@example.com",
            password_hash="hashed_password_1",
            role="admin",
            created_at=datetime(2023, 10, 1, 12, 0, 0)
        )
        user2 = User(
            id=str(uuid.uuid4()),
            email="bob@example.com",
            password_hash="hashed_password_2",
            role="member",
            created_at=datetime(2023, 10, 2, 12, 0, 0)
        )
        session.add_all([user1, user2])

        # Seed Documents
        document1 = Document(
            id=str(uuid.uuid4()),
            user_id=user1.id,
            filename="example.pdf",
            status="processed",
            chunk_count=10,
            created_at=datetime(2023, 10, 3, 12, 0, 0)
        )
        document2 = Document(
            id=str(uuid.uuid4()),
            user_id=user2.id,
            filename="example.docx",
            status="processing",
            chunk_count=None,
            created_at=datetime(2023, 10, 4, 12, 0, 0)
        )
        session.add_all([document1, document2])

        # Seed Chunks
        chunk1 = Chunk(
            id=str(uuid.uuid4()),
            document_id=document1.id,
            content="Chunk content 1",
            chunk_index=0,
            embedding=[0.1] * 1536
        )
        chunk2 = Chunk(
            id=str(uuid.uuid4()),
            document_id=document1.id,
            content="Chunk content 2",
            chunk_index=1,
            embedding=[0.2] * 1536
        )
        session.add_all([chunk1, chunk2])

        # Seed Conversations
        conversation1 = Conversation(
            id=str(uuid.uuid4()),
            user_id=user1.id,
            title="First conversation",
            created_at=datetime(2023, 10, 5, 12, 0, 0)
        )
        session.add(conversation1)

        # Seed Messages
        message1 = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation1.id,
            role="user",
            content="What is the content of the document?",
            sources=None,
            created_at=datetime(2023, 10, 5, 12, 5, 0)
        )
        message2 = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation1.id,
            role="assistant",
            content="The document contains information about...",
            sources={"chunks": [chunk1.id, chunk2.id]},
            created_at=datetime(2023, 10, 5, 12, 6, 0)
        )
        session.add_all([message1, message2])

        session.commit()
    except SQLAlchemyError as e:
        session.rollback()
        print(f"Error seeding database: {e}")
    finally:
        session.close()