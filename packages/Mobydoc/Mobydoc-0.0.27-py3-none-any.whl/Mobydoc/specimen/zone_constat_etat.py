import uuid

from sqlalchemy import (BIGINT, DATETIME, INTEGER, TIMESTAMP, VARBINARY, Float,
                        Column, DateTime, ForeignKey, String, text)
from sqlalchemy.orm import relationship

from ..base import UUID, Base, indent, json_loop

class SpecimenZoneConstatEtat(Base):
    __tablename__ = "SpecimenZoneConstatEtat"

    id = Column("SpecimenZoneConstatEtat_Id", UUID, primary_key=True, nullable=False, default=uuid.uuid4)

    id_specimen = Column("SpecimenZoneConstatEtat_Specimen_Id", UUID, ForeignKey("Specimen.Specimen_Id"), nullable=True)

    # Prévu / Actuel / Antérieur
    statut = Column("SpecimenZoneConstatEtat_Statut", INTEGER, nullable=True)
    # pas présent dans le formulaire
    id_motif_constat_etat = Column("SpecimenZoneConstatEtat_MotifConstatEtat_Id", UUID, nullable=True) #ForeignKey [dbo].[MotifConstatEtat]
    # pas présent dans le formulaire
    id_campagne_recolement = Column("SpecimenZoneConstatEtat_CampagneRecolement_Id", UUID, nullable=True) # ForeignKey [dbo].[CampagneRecolement]
    from ..reference.etat import Etat as t_etat
    id_etat = Column("SpecimenZoneConstatEtat_Etat_Id", UUID, ForeignKey(t_etat.id), nullable=True)
    # ChampSpecimenConstatEtatIntegrite
    # ChampSpecimenConstatEtatVerificateur
    from ..moby.champ.date import MobyChampDate as t_champ_date
    id_date_constat = Column("SpecimenZoneConstatEtat_DateConstat_Id", UUID, ForeignKey(t_champ_date.id), nullable=True)  
    # n'est pas affiché dans le formulaire
    id_degre_urgence = Column("SpecimenZoneConstatEtat_DegreUrgence_Id", UUID, nullable=True) #ForeignKey [dbo].[DegreUrgence]
    # NOTE:
    # une table ChampSpecimenZoneConstatEtatMultimedia existe, mais n'est pas utilisé à Grenoble
    notes = Column("SpecimenZoneConstatEtat_Notes", String, nullable=True)
    ordre = Column("SpecimenZoneConstatEtat_Ordre", INTEGER, nullable=True, default=1)

    t_write = Column("_trackLastWriteTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_creation = Column("_trackCreationTime", DateTime, nullable=False, server_default=text("(getdate())"))
    t_write_user = Column("_trackLastWriteUser", String(64), nullable=False)
    t_creation_user = Column("_trackCreationUser", String(64), nullable=False)
    t_version = Column("_rowVersion", TIMESTAMP, nullable=False)

    # liaisons

    specimen = relationship("Specimen", foreign_keys=[id_specimen], post_update=True)
    # non présent : motif_constat_etat
    # non présent : campagne_recollement
    # etat (un seul)
    etat = relationship(t_etat, foreign_keys=[id_etat])
    # intégrités (plusieurs)
    # vérificateurs (plusieurs)

    date_constat = relationship(t_champ_date, foreign_keys=[id_date_constat])
    # non présent : degre_urgence
    # multimedias






