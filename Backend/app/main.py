from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine, Base
from app.config import settings

# Δημιουργία όλων των tables στη βάση
# Αυτό τρέχει όταν ξεκινάει ο server
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    if settings.DEBUG:
        print(f"Warning: database not available, skipping create_all: {e}", flush=True)
    else:
        raise

# Δημιουργία FastAPI app
app = FastAPI(
    title="EventFull API",
    description="API για διαχείριση εκδηλώσεων και κρατήσεων",
    version="1.0.0",
    debug=settings.DEBUG
)

# CORS Middleware
# Επιτρέπει στο frontend  να επικοινωνεί με το backend 

#Σημείωση: Για όσο γράφετε τον κώδικα τοπικά, το * είναι τέλειο. 
#Όταν όμως ανεβάσετε την εφαρμογή κανονικά (production),
#θα πρέπει να το αλλάξετε στο link του frontend σας (π.χ. ["[http://to-site-tis-nikis.gr](http://to-site-tis-nikis.gr)"])
#, ώστε να μην μπορεί να μπει κανένας άλλος!
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Στο production θα βάλεις συγκεκριμένα origins  
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, PUT, DELETE, κλπ
    allow_headers=["*"],
)

# --- ENDPOINTS ---

@app.get("/")
def root():
    """
    Root endpoint - επιστρέφει welcome message.
    Χρήσιμο για να ελέγξεις ότι ο server τρέχει.
    """
    return {
        "message": "Welcome to Eventfull API",
        "docs": "/docs",  # Swagger UI
        "version": "1.0.0"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint.
    Χρήσιμο για monitoring και load balancers.
    """
    return {"status": "healthy"}