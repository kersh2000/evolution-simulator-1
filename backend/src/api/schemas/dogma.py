import datetime
from typing import Dict, Optional
from pydantic import BaseModel

class DogmaBase(BaseModel):
    name: str
    is_private: bool
    genome_length: Optional[int]
    genomic_base_num: Optional[int] = None
    codon_length: Optional[int] = None
    proteomic_base_num: Optional[int] = None
    food_chemical_structure: Optional[str] = None
    chemical_base_num: Optional[int] = None
    protein_codon_factor: Optional[int] = None
    codon_mapping_method: Optional[str] = None
    codon_map: Optional[Dict] = None
    binding_exponent: Optional[int] = None
    upper_binding_prob: Optional[float] = None
    lower_binding_prob: Optional[float] = None
    num_of_binding_intervals: Optional[int] = None
    binding_map: Optional[Dict] = None
    energy_conversion_rate: Optional[float] = None
    mitosis_base_cost: Optional[float] = None
    mitosis_base_mutation_rate: Optional[float] = None
    moving_base_cost: Optional[float] = None
    protein_synthesis_base_cost: Optional[float] = None
    step_base_cost: Optional[float] = None

    class Config:
        from_attributes: True

class DogmaResponse(DogmaBase):
    created_at: datetime.datetime
    edited_at: datetime.datetime

class DogmaCreation(DogmaBase):
    owner_id: int