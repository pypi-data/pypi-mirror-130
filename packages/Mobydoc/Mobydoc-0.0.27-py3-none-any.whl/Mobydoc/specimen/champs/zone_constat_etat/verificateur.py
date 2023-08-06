# CREATE TABLE [dbo].[ChampSpecimenConstatEtatVerificateur](
# 	[ChampSpecimenConstatEtatVerificateur_Id] [uniqueidentifier] ROWGUIDCOL  NOT NULL,
# 	[ChampSpecimenConstatEtatVerificateur_SpecimenZoneConstatEtat_Id] [uniqueidentifier] NULL,
# 	[ChampSpecimenConstatEtatVerificateur_Verificateur_Id] [uniqueidentifier] NULL,
# 	[ChampSpecimenConstatEtatVerificateur_FonctionRole_Id] [uniqueidentifier] NULL,
# 	[ChampSpecimenConstatEtatVerificateur_Ordre] [int] NULL,
# 	[_trackLastWriteTime] [datetime] NOT NULL,
# 	[_trackCreationTime] [datetime] NOT NULL,
# 	[_trackLastWriteUser] [nvarchar](64) NOT NULL,
# 	[_trackCreationUser] [nvarchar](64) NOT NULL,
#  CONSTRAINT [PK_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificateu] PRIMARY KEY NONCLUSTERED 
# (
# 	[ChampSpecimenConstatEtatVerificateur_Id] ASC
# )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 99, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
# ) ON [PRIMARY]
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur] ADD  CONSTRAINT [DF_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificater]  DEFAULT ((1)) FOR [ChampSpecimenConstatEtatVerificateur_Ordre]
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur] ADD  CONSTRAINT [DF_ChampSpecimenConstatEtatVerificateu__trackLastWriteTime]  DEFAULT (getdate()) FOR [_trackLastWriteTime]
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur] ADD  CONSTRAINT [DF_ChampSpecimenConstatEtatVerificateu__trackCreationTime]  DEFAULT (getdate()) FOR [_trackCreationTime]
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur]  WITH NOCHECK ADD  CONSTRAINT [FK_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificate__SpecimenZoneConstatEtat_Id_SpecimenZoneConstatEtat] FOREIGN KEY([ChampSpecimenConstatEtatVerificateur_SpecimenZoneConstatEtat_Id])
# REFERENCES [dbo].[SpecimenZoneConstatEtat] ([SpecimenZoneConstatEtat_Id])
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur] NOCHECK CONSTRAINT [FK_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificate__SpecimenZoneConstatEtat_Id_SpecimenZoneConstatEtat]
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur]  WITH NOCHECK ADD  CONSTRAINT [FK_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificateF_Reference_Id_FonctionRole] FOREIGN KEY([ChampSpecimenConstatEtatVerificateur_FonctionRole_Id])
# REFERENCES [dbo].[FonctionRole] ([Reference_Id])
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur] NOCHECK CONSTRAINT [FK_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificateF_Reference_Id_FonctionRole]
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur]  WITH NOCHECK ADD  CONSTRAINT [FK_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificateF_Reference_Id_Reference] FOREIGN KEY([ChampSpecimenConstatEtatVerificateur_FonctionRole_Id])
# REFERENCES [dbo].[Reference] ([Reference_Id])
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur] NOCHECK CONSTRAINT [FK_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificateF_Reference_Id_Reference]
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur]  WITH NOCHECK ADD  CONSTRAINT [FK_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificateV_Personne_Id_Personne] FOREIGN KEY([ChampSpecimenConstatEtatVerificateur_Verificateur_Id])
# REFERENCES [dbo].[Personne] ([Personne_Id])
# ALTER TABLE [dbo].[ChampSpecimenConstatEtatVerificateur] NOCHECK CONSTRAINT [FK_ChampSpecimenConstatEtatVerificateu_ChampSpecimenConstatEtatVerificateV_Personne_Id_Personne]
