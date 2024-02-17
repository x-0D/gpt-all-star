from __future__ import annotations

import os.path
from pathlib import Path

from gpt_all_star.core.agents.agents import Agents
from gpt_all_star.core.agents.architect import Architect
from gpt_all_star.core.agents.copilot import Copilot
from gpt_all_star.core.agents.designer import Designer
from gpt_all_star.core.agents.engineer import Engineer
from gpt_all_star.core.agents.product_owner import ProductOwner
from gpt_all_star.core.agents.project_manager import ProjectManager
from gpt_all_star.core.agents.qa_engineer import QAEngineer
from gpt_all_star.core.steps.steps import STEPS, StepType
from gpt_all_star.core.storage import Storage, Storages


class Project:
    def __init__(
        self,
        step: StepType = StepType.DEFAULT,
        project_name: str = None,
        japanese_mode: bool = False,
        review_mode: bool = False,
        debug_mode: bool = False,
    ) -> None:
        self.set_modes(japanese_mode, review_mode, debug_mode)
        self.set_project_name(project_name)
        self.set_storages()
        self.set_agents()
        self.set_step_type(step)

    def set_modes(
        self, japanese_mode: bool, review_mode: bool, debug_mode: bool
    ) -> None:
        self.japanese_mode = japanese_mode
        self.review_mode = review_mode
        self.debug_mode = debug_mode

    def set_project_name(self, project_name: str) -> None:
        self.project_name = project_name or Copilot().ask_project_name()

    def set_storages(self) -> None:
        project_path = Path(os.path.abspath(f"projects/{self.project_name}")).absolute()
        self.storages = Storages(
            root=Storage(project_path),
            app=Storage(project_path / "app"),
            docs=Storage(project_path / "docs"),
            archive=Storage(project_path / ".archive"),
        )

    def set_agents(self) -> None:
        self.agents = Agents(
            copilot=Copilot(storages=self.storages, debug_mode=self.debug_mode),
            product_owner=ProductOwner(
                storages=self.storages, debug_mode=self.debug_mode
            ),
            engineer=Engineer(storages=self.storages, debug_mode=self.debug_mode),
            architect=Architect(storages=self.storages, debug_mode=self.debug_mode),
            designer=Designer(storages=self.storages, debug_mode=self.debug_mode),
            qa_engineer=QAEngineer(storages=self.storages, debug_mode=self.debug_mode),
            project_manager=ProjectManager(
                storages=self.storages, debug_mode=self.debug_mode
            ),
        )

    def set_step_type(self, step: StepType) -> None:
        self.step_type = step or StepType.DEFAULT
        if self.step_type is StepType.DEFAULT:
            self.agents.copilot.state("Archiving previous storages...")
            Storages.archive_storage(self.storages)

    def start(self) -> None:
        self.agents.copilot.start(self.project_name)
        self.execute_steps()

    def execute_steps(self) -> None:
        try:
            for step in STEPS[self.step_type]:
                self.execute_step(step)
        except KeyboardInterrupt:
            self.agents.copilot.state("Interrupt received! Stopping...")

    def execute_step(self, step) -> None:
        try:
            step(
                self.agents,
                self.japanese_mode,
                self.review_mode,
                self.debug_mode,
            ).run()
        except Exception as e:
            self.agents.copilot.state(
                f"Failed to execute step {step}. Reason: {str(e)}"
            )
            raise e

    def finish(self) -> None:
        self.agents.copilot.finish()
