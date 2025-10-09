import json
from pathlib import Path

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

        Args:
            mode: Modo de juego a cargar

        Returns:
            GameConfig con la configuración cargada

        Raises:
            GameConfigLoaderError: Si hay errores en la carga o validación
        """
        config_path = self.base_path / mode.value / "config.json"

        # Validar que el archivo existe
        if not config_path.exists():
            raise GameConfigLoaderError(
                f"Archivo de configuración no encontrado: {config_path}"
            )

        try:
            # Leer archivo JSON
            with open(config_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Validar estructura
            self._validate_config_structure(data, config_path)

            # Construir GameConfig
            return GameConfig(
                mode=mode,
                map_path=data['map_path'],
                initial_position=tuple(data['initial_position']),
                goal_position=tuple(data['goal_position']),
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

    def _validate_config_structure(self, data: dict, config_path: Path) -> None:
        """
        Valida que la estructura del JSON sea correcta.

        Args:
            data: Diccionario con los datos del JSON
            config_path: Ruta del archivo (para mensajes de error)

        Raises:
            GameConfigLoaderError: Si la estructura es inválida
        """
        required_fields = [
            'mode', 'map_path', 'initial_position',
            'goal_position', 'entity_type'
        ]

        # Verificar campos requeridos
        for field in required_fields:
            if field not in data:
                raise GameConfigLoaderError(
                    f"Campo requerido '{field}' faltante en {config_path}"
                )

        # Validar tipos
        if not isinstance(data['initial_position'], list) or len(data['initial_position']) != 2:
            raise GameConfigLoaderError(
                f"'initial_position' debe ser una lista de 2 elementos en {config_path}"
            )

        if not isinstance(data['goal_position'], list) or len(data['goal_position']) != 2:
            raise GameConfigLoaderError(
                f"'goal_position' debe ser una lista de 2 elementos en {config_path}"
            )

        # Validar que el archivo de mapa existe
        map_path = Path(data['map_path'])
        if not map_path.exists():
            raise GameConfigLoaderError(
                f"Archivo de mapa no encontrado: {map_path} (especificado en {config_path})"
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
