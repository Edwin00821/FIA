import json
from pathlib import Path

from typing import Tuple

from src.core.game_mode import GameMode, GameConfig


class GameConfigLoaderError(Exception):
    """Excepción personalizada para errores en la carga de configuración."""
    pass


class GameConfigLoader:
    """
    Cargador de configuración específica de modos de juego.

    Se encarga de leer archivos config.json y validar su estructura.
    """

    def __init__(self, base_path: str = "data"):
        """
        Inicializa el cargador de configuración.

        Args:
            base_path: Ruta base donde se encuentran las carpetas de configuración
        """
        self.base_path = Path(base_path)

    def load_config(self, mode: GameMode) -> GameConfig:
        """
        Carga la configuración para un modo de juego específico.
        """
        config_path = self.base_path / mode.value / "config.json"

        if not config_path.exists():
            raise GameConfigLoaderError(
                f"Archivo de configuración no encontrado: {config_path}"
            )

        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            self._validate_config_structure(data, config_path)

            # Convertir posiciones a tuplas si son strings
            initial_pos = data['initial_position']
            goal_pos = data['goal_position']

            if isinstance(initial_pos, str):
                initial_pos = self._parse_human_coordinate(initial_pos)
            else:
                initial_pos = tuple(initial_pos)

            if isinstance(goal_pos, str):
                goal_pos = self._parse_human_coordinate(goal_pos)
            else:
                goal_pos = tuple(goal_pos)

            return GameConfig(
                mode=mode,
                map_path=data['map_path'],
                initial_position=initial_pos,
                goal_position=goal_pos,
                entity_type=data['entity_type'],
                entity_config=data.get('entity_config', {})
            )

        except json.JSONDecodeError as e:
            raise GameConfigLoaderError(
                f"Error parseando JSON en {config_path}: {e}"
            )
        except KeyError as e:
            raise GameConfigLoaderError(
                f"Campo requerido faltante en {config_path}: {e}"
            )
        except Exception as e:
            raise GameConfigLoaderError(
                f"Error inesperado cargando configuración: {e}"
            )

    def get_available_modes(self) -> list[GameMode]:
        """
        Obtiene la lista de modos disponibles (que tienen carpeta de configuración).

        Returns:
            Lista de GameMode disponibles
        """
        available = []
        for mode in GameMode:
            config_path = self.base_path / mode.value / "config.json"
            if config_path.exists():
                available.append(mode)
        return available

    def _validate_config_structure(self, data: dict, config_path: Path) -> None:
        """
        Valida que la estructura del JSON sea correcta.
        """
        required_fields = [
            'mode', 'map_path', 'initial_position',
            'goal_position', 'entity_type'
        ]

        for field in required_fields:
            if field not in data:
                raise GameConfigLoaderError(
                    f"Campo requerido '{field}' faltante en {config_path}"
                )

        # Validar tipos - ahora soporta string o lista
        if not (isinstance(data['initial_position'], (list, str))):
            raise GameConfigLoaderError(
                f"'initial_position' debe ser una lista de 2 elementos o string en formato humano en {config_path}"
            )

        if not (isinstance(data['goal_position'], (list, str))):
            raise GameConfigLoaderError(
                f"'goal_position' debe ser una lista de 2 elementos o string en formato humano en {config_path}"
            )

        # Si es lista, validar longitud
        if isinstance(data['initial_position'], list) and len(data['initial_position']) != 2:
            raise GameConfigLoaderError(
                f"'initial_position' como lista debe tener 2 elementos en {config_path}"
            )

        if isinstance(data['goal_position'], list) and len(data['goal_position']) != 2:
            raise GameConfigLoaderError(
                f"'goal_position' como lista debe tener 2 elementos en {config_path}"
            )

        # Validar que el archivo de mapa existe
        map_path = Path(data['map_path'])
        if not map_path.exists():
            raise GameConfigLoaderError(
                f"Archivo de mapa no encontrado: {map_path} (especificado en {config_path})"
            )

        if 'entity_config' in data:
            if not isinstance(data['entity_config'], dict):
                raise GameConfigLoaderError(
                    f"'entity_config' debe ser un diccionario en {config_path}"
                )

    def _parse_human_coordinate(self, coord: str) -> Tuple[int, int]:
        """
        Convierte una coordenada en formato humano a índices (row, col).

        Args:
            coord: Coordenada en formato "10A" o "2E"

        Returns:
            Tupla (row, col) con índices 0-indexados

        Raises:
            GameConfigLoaderError: Si el formato es inválido
        """
        coord = coord.strip().upper()

        # Separar número y letra
        row_str = ""
        col_str = ""

        for char in coord:
            if char.isdigit():
                row_str += char
            elif char.isalpha():
                col_str += char

        if not row_str or not col_str:
            raise GameConfigLoaderError(
                f"Formato de coordenada inválido: '{coord}'. Use formato como '10A' o '2E'"
            )

        try:
            row = int(row_str) - 1  # Convertir de 1-indexado a 0-indexado
            col = ord(col_str[0]) - ord('A')  # Convertir letra a índice
            return (row, col)
        except (ValueError, IndexError) as e:
            raise GameConfigLoaderError(
                f"Error convirtiendo coordenada '{coord}': {e}"
            )
