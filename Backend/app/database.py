from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings

# 1. Δημιουργία Engine
# Ο engine είναι η "γέφυρα" με τη MySQL
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG  # True = εμφανίζει τα SQL queries στο terminal
)

# 2. Δημιουργία SessionLocal
# Κάθε request θα έχει το δικό του session
SessionLocal = sessionmaker(
    autocommit=False,  # Θέλουμε να κάνουμε commit χειροκίνητα
    autoflush=False,   # Δεν στέλνει αυτόματα αλλαγές στη βάση
    bind=engine        # Συνδέεται με τον engine μας
)

# 3. Base class για τα models
# Όλα τα models σου θα κάνουν inherit από αυτό
Base = declarative_base()

# 4. Dependency για FastAPI
# Αυτή η συνάρτηση δίνει database session σε κάθε request
def get_db():
    
   # Generator που δημιουργεί DB session για κάθε request.
   # Με το 'finally' εξασφαλίζουμε ότι κλείνει ΠΑΝΤΑ.
    
    db = SessionLocal()
    try:
        yield db  # Δίνει το session στο endpoint
    finally:
        db.close()  # Κλείνει μετά το response