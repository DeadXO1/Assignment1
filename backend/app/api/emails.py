"""API endpoints for email capture."""
import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.database import get_db
from app.models import Email, Event
from app.schemas import EmailCreate, EmailResponse

router = APIRouter(prefix="/api/emails", tags=["emails"])


def validate_email_format(email: str) -> bool:
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


@router.post("", response_model=EmailResponse, status_code=201)
def create_email(email_data: EmailCreate, db: Session = Depends(get_db)):
    """Capture user email with opt-in consent."""
    
    # Validate email format
    if not validate_email_format(email_data.email):
        raise HTTPException(status_code=400, detail="Invalid email format")
    
    # Check if opt-in is required (must be True)
    if not email_data.opt_in:
        raise HTTPException(
            status_code=400,
            detail="Email opt-in is required. Please check the consent checkbox."
        )
    
    # Verify event exists
    event = db.query(Event).filter(Event.id == email_data.event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Check if email already exists
    existing_email = db.query(Email).filter(Email.email == email_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=409,
            detail="Email already registered. Each email can only be captured once."
        )
    
    # Create email record
    try:
        new_email = Email(
            email=email_data.email,
            event_id=email_data.event_id,
            opt_in=email_data.opt_in
        )
        db.add(new_email)
        db.commit()
        db.refresh(new_email)
        
        return EmailResponse.model_validate(new_email)
        
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already exists")

