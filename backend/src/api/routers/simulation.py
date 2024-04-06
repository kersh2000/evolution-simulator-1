from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas import schemas
from ...db.models import models
from ...db.db import get_db
from ..middleware import middleware
from sqlalchemy.orm import Session

router = APIRouter(prefix="/simulation", tags=['Simulations'])

@router.get("/", response_model=list[schemas.SimulationResponse])
def get_simulations(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    simulations = db.query(models.Simulation).filter(models.Simulation.owner_id == current_user.id).all()
    return simulations

@router.get("/public", response_model=list[schemas.SimulationResponse])
def get_public_simulations(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    simulations = db.query(models.Simulation).filter(models.Simulation.is_private == False).all()
    return simulations

# Only works for admin account, fetches public and private simulations
@router.get("/all", response_model=list[schemas.SimulationResponse])
def get_all_simulations(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    if (current_user.id != 1):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorised access, please contact admin/owner for further detail if access is needed.")
    simulations = db.query(models.Simulation).filter(models.Simulation.owner_id == 1).all()
    return simulations

@router.get("/full/{id}", response_model=schemas.SimulationFullResponse)
def get_full_simulations(simulation: models.Simulation = Depends(middleware.get_current_simulation), db: Session = Depends(get_db)):
    environment = db.query(models.Environment).filter(models.Environment.id == simulation.environment_id)
    dogma = db.query(models.Dogma).filter(models.Dogma.id == simulation.dogma_id)

    return {
        "simulation": simulation,
        "environment": environment,
        "dogma": dogma
    }

@router.get("/{id}", response_model=schemas.SimulationResponse)
def get_simulation(simulation: models.Simulation = Depends(middleware.get_current_simulation)):
    return simulation

@router.post("/", response_model=schemas.SimulationResponse)
def create_simulation(simulation: schemas.SimulationCreation ,db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    created_simulation = models.Simulation(**simulation.model_dump())
    created_simulation.owner_id = current_user.id
    db.add(created_simulation)
    db.commit()
    db.refresh()
    return created_simulation

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_simulation(simulation: models.Simulation = Depends(middleware.get_current_simulation), db: Session = Depends(get_db)):
    db.delete(simulation)
    db.commit()

@router.put("/{id}", response_model=schemas.SimulationResponse)
def update_simulation(simulation: schemas.SimulationCreation, old_simulation: models.Simulation = Depends(middleware.get_current_simulation), db: Session = Depends(get_db)):
    query = db.query(models.Simulation).filter(models.Simulation.id == old_simulation.id)
    query.update(simulation.model_dump(), synchronize_session=False)
    db.commit()

    updated_simulation = query.first()
    return updated_simulation

@router.patch("/{id}", response_model=schemas.SimulationResponse)
def patch_simulation(id: int, simulation_data: schemas.SimulationUpdate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    query = db.query(models.Simulation).filter(models.Simulation.id == id)
    old_simulation = query.first()

    if not old_simulation:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Simulation was not found.")

    if old_simulation.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No corresponding simulation were found.")
    
    updated_data = simulation_data.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No fields provided.")

    query.update(updated_data, synchronize_session=False)
    db.commit()

    updated_simulation = query.first()
    return updated_simulation
