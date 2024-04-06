from fastapi import APIRouter, HTTPException, status, Depends
from ..schemas import schemas
from ...db.models import models
from ...db.db import get_db
from ..middleware import middleware
from sqlalchemy.orm import Session

router = APIRouter(prefix="/block", tags=['Blocks'])

@router.get("/", response_model=list[schemas.BlockResponse])
def get_blocks(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    blocks = db.query(models.Block).filter(models.Block.owner_id == current_user.id).all()
    return blocks

@router.get("/public", response_model=list[schemas.BlockResponse])
def get_public_blocks(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    blocks = db.query(models.Block).filter(models.Block.is_private == False).all()
    return blocks

# Only works for admin account, fetches public and private simulations
@router.get("/all", response_model=list[schemas.BlockResponse])
def get_all_blocks(db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    if (current_user.id != 1):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorised access, please contact admin/owner for further detail if access is needed.")
    blocks = db.query(models.Block).filter(models.Block.owner_id == 1).all()
    return blocks

@router.get("/{id}", response_model=schemas.BlockResponse)
def get_block(block: models.Block = Depends(middleware.get_current_block)):
    return block

@router.post("/", response_model=schemas.BlockResponse)
def create_block(block: schemas.BlockCreation ,db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    created_block = models.Block(**block.model_dump())
    created_block.owner_id = current_user.id
    db.add(created_block)
    db.commit()
    db.refresh()
    return created_block

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_block(block: models.Block = Depends(middleware.get_current_block), db: Session = Depends(get_db)):
    db.delete(block)
    db.commit()

@router.put("/{id}", response_model=schemas.BlockResponse)
def update_block(block: schemas.BlockCreation, old_block: models.Block = Depends(middleware.get_current_block), db: Session = Depends(get_db)):
    query = db.query(models.Block).filter(models.Block.id == old_block.id)
    query.update(block.model_dump(), synchronize_session=False)
    db.commit()

    updated_block = query.first()
    return updated_block

@router.patch("/{id}", response_model=schemas.BlockResponse)
def patch_block(id: int, block_data: schemas.BlockUpdate, db: Session = Depends(get_db), current_user: schemas.UserResponse = Depends(middleware.get_current_user)):
    query = db.query(models.Block).filter(models.Block.id == id)
    old_block = query.first()

    if not old_block:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Block was not found.")

    if old_block.owner_id != current_user.id:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "No corresponding block were found.")
    
    updated_data = block_data.model_dump(exclude_unset=True)
    if not updated_data:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No fields provided.")

    query.update(updated_data, synchronize_session=False)
    db.commit()

    updated_block = query.first()
    return updated_block
