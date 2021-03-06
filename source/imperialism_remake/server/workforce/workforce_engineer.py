# Imperialism remake
# Copyright (C) 2020 amtyurin
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

from imperialism_remake.server.models.technology_type import TechnologyType
from imperialism_remake.server.models.terrain_type import TerrainType
from imperialism_remake.server.models.turn_planned import TurnPlanned
from imperialism_remake.server.models.workforce_action import WorkforceAction
from imperialism_remake.server.server_scenario import ServerScenario
from imperialism_remake.server.workforce.workforce_common import WorkforceCommon


class WorkforceEngineer(WorkforceCommon):
    def __init__(self, server_scenario: ServerScenario, turn_planned: TurnPlanned, workforce):
        super().__init__(server_scenario, turn_planned, workforce, {})

        self._tech_to_terrain_type = {
            TerrainType.SWAMP.value: TechnologyType.ROAD_THROUGH_SWAMP,
            TerrainType.HILLS.value: TechnologyType.ROAD_THROUGH_HILLS,
            TerrainType.MOUNTAINS.value: TechnologyType.ROAD_THROUGH_MOUNTAINS,
            TerrainType.DESERT.value: TechnologyType.ROAD_THROUGH_DESERT,
            TerrainType.TUNDRA.value: TechnologyType.ROAD_THROUGH_TUNDRA,
            TerrainType.PLAIN.value: TechnologyType.ROAD_THROUGH_PLAINS
        }

    def is_action_allowed(self, new_row: int, new_column: int, workforce_action: WorkforceAction) -> bool:
        is_action_allowed = super().is_action_allowed(new_row, new_column, workforce_action)
        if not is_action_allowed:
            return False

        if workforce_action == WorkforceAction.DUTY_ACTION:
            row, column = self.get_current_position()
            # TODO check if can do duty action where i am standing now (build port or extend city, etc.)
            if new_column == column and new_row == row:
                return True

            if [new_column, new_row] not in self._server_scenario.neighbored_tiles(column, row):
                return False

            neighbour_terrain_type = self._server_scenario.terrain_at(new_column, new_row)
            neighbour_tile_action_allowed = self._can_build(neighbour_terrain_type)

            current_terrain_type = self._server_scenario.terrain_at(column, row)
            current_tile_action_allowed = self._can_build(current_terrain_type)

            return neighbour_tile_action_allowed and current_tile_action_allowed

        return True

    def _can_build(self, terrain_type):
        return self._is_tech_allowed_on_map(self._tech_to_terrain_type[terrain_type])
