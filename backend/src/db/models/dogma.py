from sqlalchemy import JSON, Column, ForeignKey, Integer, String, Boolean, TIMESTAMP, Enum, Float
from ..db import Base
from sqlalchemy.sql import func

class Dogma(Base):
    __tablename__ = "dogmas"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    is_private = Column(Boolean, nullable=False, default=True)
    # The default length of the blocks' genomes
    genome_length = Column(Integer, nullable=False, default=200)
    # The number of unique bases for storing genomic information within the genome, starting from '0' to '9' (numbers)
    genomic_base_num = Column(Integer, nullable=False, default=3)
    # The length of the codon at which the 'universal polymerase' will use to transcript (and translate) the genome into proteins
    codon_length = Column(Integer, nullable=False, default=3)
    # The number of unique bases for storing proteomic information within the proteome, starting from 'aa' to 'zz' (double lower-case letters)
    proteomic_base_num = Column(Integer, nullable=False, default=10)
    # The chemical formula of the linear small food
    food_chemical_structure = Column(String, nullable=False, default="ABA")
    # The number of unique bases for storing chemical information within the substrates, starting from 'A' to 'Z' (single upper-case letter)
    chemical_base_num = Column(Integer, nullable=False, default=3)
    # The number of different genomic codons which can code for a single protein base (cannot be larger than: (((genomic_base_num ^ codon_length) / 2) - 2) / proteomic_base_num)
    protein_codon_factor = Column(Integer, default=2)
    # The method for generating protein-codon maps, with a protein_codon_factor of higher than 1. 
    # > Linear - next to eachother in sequence (aa1, aa2, bb1, bb2, cc1, cc2)
    # > Non-Linear - in order of generation (aa1, bb1, cc1, aa2, bb2, cc2)
    # > Mirror - on opposite sides of the codon spectrum (aa1, bb1, cc1, cc2, bb2, aa2)
    # > Random - random assignment to any available codon (bb2, cc1, cc2, aa2, bb1, aa1)
    # > Custom - determined by the user on the frontend
    codon_mapping_method = Column(Enum("linear", "non-linear", "mirror", "random", "custom", name="mapping_method_type"), default="linear")
    # The codon map
    codon_map = Column(JSON)
    # The exponent of the binding formula (sum of binding probabilities / length of substrate) to determine the activation or deactivation of an event or cascade of events by the protein
    binding_exponent = Column(Integer, nullable=False, default=3)
    # The upper binding probability
    upper_binding_prob = Column(Float, nullable=False, default=0.9)
    # The lower binding probability
    lower_binding_prob = Column(Float, nullable=False, default=0.1)
    # The number of binding intervals, given a probability between the upper and lower limits set (cannot be larger then proteomic_base_num - 2)
    num_of_binding_intervals = Column(Integer, nullable=False, default=3)
    # The binding map, containing the probability each protein interaction has at successfully binding
    binding_map = Column(JSON)
    # The rate of converting chemicals into energy
    energy_conversion_rate = Column(Float, nullable=False, default=10)
    # The base energy cost for asexual reproduction (mitosis)
    mitosis_base_cost = Column(Float, nullable=False, default=10000)
    # The base mutation rate for asexual reproduction (mitosis)
    mitosis_base_mutation_rate = Column(Float, nullable=False, default=10000)
    # The base energy cost for moving a block
    moving_base_cost = Column(Float, nullable=False, default=1000)
    # The base energy cost for one round of protein sysnthesis
    protein_synthesis_base_cost = Column(Float, nullable=False, default=1000)
    # The base energy cost for living in one step (unit of time)
    step_base_cost = Column(Float, nullable=False, default=100)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    edited_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())