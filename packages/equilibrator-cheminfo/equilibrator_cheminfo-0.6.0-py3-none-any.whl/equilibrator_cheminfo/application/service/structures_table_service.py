# Copyright (c) 2021, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide a service that coordinates the transformation of structures."""


import logging
import multiprocessing
from pathlib import Path
from typing import Type

import pandas as pd
from tqdm import tqdm

# Import needed for activating the pandas.DataFrame accessor definition.
from equilibrator_cheminfo.domain.model import StructuresTable  # noqa: F401
from equilibrator_cheminfo.infrastructure.service.orm import (
    ORMManagementService,
    ORMMolecularEntityRepository,
)

from .abstract_molecular_entity_service import AbstractMolecularEntityService
from .create_molecular_entities_from_table_command import (
    CheminformaticsBackend,
    CreateMolecularEntitiesFromTableCommand,
)


logger = logging.getLogger(__name__)


class StructuresTableService:
    """Define a service that coordinates the transformation of structures."""

    @classmethod
    def transform(cls, command: CreateMolecularEntitiesFromTableCommand) -> None:
        """Transform a structures table into a database of molecular entities."""
        assert command.cheminformatics_backend == CheminformaticsBackend.ChemAxon, (
            "Currently, pKa and major microspecies estimation is only provided by "
            "ChemAxon Marvin."
        )
        assert command.structures_table.is_file(), (
            f"The TSV file '{command.structures_table}' defining the chemical "
            f"structures was not found."
        )
        from equilibrator_cheminfo.application.service.chemaxon import (
            ChemAxonMolecularEntityService,
        )

        repo = ORMMolecularEntityRepository(
            session=ORMManagementService.create_session(command.database_url)
        )
        structures = cls._create_structures_table(command.structures_table)
        if command.processes > 1:
            cls._concurrently(structures, ChemAxonMolecularEntityService, repo, command)
        else:
            cls._sequentially(structures, ChemAxonMolecularEntityService, repo, command)
        repo.log_summary()

    @classmethod
    def _sequentially(
        cls,
        structures: pd.DataFrame,
        service: Type[AbstractMolecularEntityService],
        repo: ORMMolecularEntityRepository,
        command: CreateMolecularEntitiesFromTableCommand,
    ) -> None:
        """Coordinate predictions on all structures sequentially and load results."""
        service.setup(
            command.minimum_ph,
            command.maximum_ph,
            command.fixed_ph,
        )
        for structure in tqdm(
            structures.cheminfo.iter_structures(),
            total=len(structures),
            desc="Molecular Entity",
            unit_scale=True,
        ):
            if (entity := service.run(structure)) is not None:
                repo.add(entity)

    @classmethod
    def _concurrently(
        cls,
        structures: pd.DataFrame,
        service: Type[AbstractMolecularEntityService],
        repo: ORMMolecularEntityRepository,
        command: CreateMolecularEntitiesFromTableCommand,
        batch_size: int = 10_000,
    ) -> None:
        """Coordinate predictions on all structures concurrently and load results."""
        args = list(structures.cheminfo.iter_structures())
        chunk_size = min(max(len(args) // command.processes, 1), batch_size)
        with multiprocessing.get_context("spawn").Pool(
            processes=command.processes,
            initializer=service.setup,
            initargs=(
                command.minimum_ph,
                command.maximum_ph,
                command.fixed_ph,
            ),
        ) as pool:
            result_iter = pool.imap_unordered(
                service.run,
                args,
                chunksize=chunk_size,
            )
            for molecular_entity in (
                result
                for result in tqdm(
                    result_iter,
                    total=len(args),
                    desc="Molecular Entity",
                    unit_scale=True,
                )
                if result is not None
            ):
                repo.add(molecular_entity)

    @classmethod
    def _create_structures_table(cls, molecules: Path) -> pd.DataFrame:
        """Extract and transform chemical structures from the given TSV file."""
        logger.info("Extract chemical structures.")
        raw = pd.read_csv(molecules, sep="\t")
        logger.info(f"Found {len(raw):n} entries.")
        logger.info("Transform chemical structures.")
        logger.debug("Ignore rows with missing InChIs.")
        result = raw.loc[raw["inchi"].notnull(), :].cheminfo.neutralize_protonation()
        logger.info(f"Maintained {len(result):n} entries.")
        assert len(result["inchikey"].unique()) == len(
            result
        ), "InChIKeys are not unique even though they *should* be."
        return result
