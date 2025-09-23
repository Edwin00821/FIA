import csv
from pathlib import Path
from typing import List, Dict
from abc import ABC, abstractmethod

from src.core.cell import Cell, TerrainType
from src.core.map import Map


class MapLoaderError(Exception):
    """Excepción personalizada para errores en la carga de mapas."""
    pass


class BaseMapLoader(ABC):
    """Clase base abstracta para cargadores de mapas."""

    @abstractmethod
    def load(self, file_path: str) -> Map:
        pass

    def _validate_file_exists(self, file_path: str) -> None:
        if not Path(file_path).exists():
            raise MapLoaderError(f"El archivo {file_path} no existe")

    def _parse_terrain_value(self, value: str) -> TerrainType:
        try:
            terrain_value = int(value.strip())
            return TerrainType.from_value(terrain_value)
        except ValueError as e:
            if "Valor de terreno desconocido" in str(e):
                raise MapLoaderError(
                    f"Valor de terreno inválido: '{value.strip()}'")
            else:
                raise MapLoaderError(
                    f"'{value.strip()}' no es un número válido")

    def _build_grid_from_rows(self, rows: List[List[str]]) -> Map:
        grid = []
        for line_num, row_values in enumerate(rows, 1):
            if not row_values or all(not val.strip() for val in row_values):
                continue  # Ignorar filas vacías

            row = []
            for col_num, value in enumerate(row_values):
                try:
                    terrain = self._parse_terrain_value(value)
                    row.append(Cell(terrain))
                except MapLoaderError as e:
                    raise MapLoaderError(
                        f"Fila {line_num}, columna {col_num + 1}: {e}"
                    )
            grid.append(row)

        if not grid:
            raise MapLoaderError(
                "El archivo está vacío o no contiene datos válidos"
            )

        return Map(grid)


class TxtMapLoader(BaseMapLoader):
    def load(self, file_path: str) -> Map:
        self._validate_file_exists(file_path)

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                rows = [line.strip().split(",")
                        for line in file if line.strip()]
        except IOError as e:
            raise MapLoaderError(f"Error al leer el archivo {file_path}: {e}")

        return self._build_grid_from_rows(rows)


class CsvMapLoader(BaseMapLoader):
    def load(self, file_path: str) -> Map:
        self._validate_file_exists(file_path)

        try:
            with open(file_path, "r", encoding="utf-8", newline="") as file:
                csv_reader = csv.reader(file)
                rows = [row for row in csv_reader]
        except IOError as e:
            raise MapLoaderError(f"Error al leer el archivo {file_path}: {e}")

        return self._build_grid_from_rows(rows)


class MapLoader:
    """Gestor principal de carga de mapas."""

    def __init__(self):
        self._loaders: Dict[str, BaseMapLoader] = {
            ".txt": TxtMapLoader(),
            ".csv": CsvMapLoader(),
        }

    def load_map(self, file_path: str) -> Map:
        """Carga un mapa detectando automáticamente el formato del archivo."""
        file_extension = Path(file_path).suffix.lower()

        if file_extension not in self._loaders:
            supported_formats = ", ".join(self._loaders.keys())
            raise MapLoaderError(
                f"Formato de archivo no soportado: {file_extension}. "
                f"Formatos soportados: {supported_formats}"
            )

        loader = self._loaders[file_extension]
        return loader.load(file_path)

    def get_supported_formats(self) -> List[str]:
        """Retorna la lista de formatos soportados."""
        return list(self._loaders.keys())
