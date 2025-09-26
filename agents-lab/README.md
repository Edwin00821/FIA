# Práctica 1 – Búsqueda en Mapas

## Objetivo

Desarrollar los elementos básicos para definir y manipular entornos discretos representados en matrices (laberintos, tableros o mapas), que posteriormente permitirán la interacción con agentes capaces de explorar, descubrir y tomar decisiones dentro de estos espacios.

## Descripción

En esta práctica se trabajará con representaciones de ambientes utilizando **matrices de R filas y C columnas**, donde las filas están numeradas y las columnas identificadas con letras.

Los ambientes pueden representar:

- **Laberintos**: caminos y muros.
- **Mapas de terreno**: distintos tipos de superficies (tierra, agua, montaña, arena, bosque, etc.).
- **Tableros de juego**: como ajedrez u otros.

Cada celda de la matriz se codifica con un valor que representa su tipo (ej. `0 = muro`, `1 = camino`, `2 = agua`, `3 = arena`, `4 = bosque`), lo cual facilita el procesamiento y reduce la complejidad computacional.

Los mapas se cargarán desde archivos de texto en formato CSV o similar, y se desplegarán gráficamente para permitir interacción.

## Actividades

### 1. Carga y manejo de mapas

- [x] **1.1 Cargar mapa**: Importar un archivo (`.txt` o `.csv`) con el mapa codificado y mostrarlo en una interfaz gráfica.
- [x] **1.2 Consultar celda**: Obtener el valor de una coordenada y mostrar su significado (ej. “(7,A) es muro”).
- [x] **1.3 Modificar celda**: Cambiar el valor de una coordenada específica en el mapa.
- [x] **1.4 Marcar posiciones**: Permitir anotaciones como:
  - `I`: Punto inicial
  - `X`: Posición actual
  - `V`: Visitado
  - `O`: Punto de decisión

### 2. Enmascaramiento de mapas

Diferenciar entre:

- **Mapa completo**: creado por el diseñador.
- **Conocimiento del agente**: construido de manera progresiva mientras explora.

Se debe permitir:

1. [x] Enmascarar todo el mapa (desconocido).
2. [x] Descubrir una posición al visitarla.
3. [x] Volver a enmascarar posiciones.

### 3. Creación de agentes

Diseñar agentes con diferentes **habilidades de percepción y acción**:

#### 3.1 Sensores

- [] **Agente con 1 sensor**: percibe solo en una dirección (ej. frente).
- [] **Agente con 4 sensores**: percibe en todas las direcciones (arriba, abajo, izquierda, derecha).

#### 3.2 Acciones

- [] Ejemplo **Agente 1**: girar izquierda, avanzar.
- [] Ejemplo **Agente 2**: girar izquierda, girar derecha, avanzar.
- [] Ejemplo **Agente 3**: moverse libremente en las 4 direcciones.

#### 3.3 Costos de movimiento

Cada tipo de terreno tiene un **costo diferente** dependiendo del agente (humano, mono, pulpo, sasquatch, etc.).  
Por ejemplo:

- [] **Agua**: Humano (2), Pulpo (1), Mono (4).
- [] **Montaña**: solo accesible para Sasquatch (15).

### 4. Control de un agente por el usuario

Implementar una modalidad donde el **usuario controla al agente**:

1. [] Seleccionar tipo de ser (Humano, Mono, etc.).
2. [] Establecer punto inicial y final.
3. [] Mover al agente con teclado o mouse.
4. [] Marcar casillas visitadas (`V`) y puntos de decisión (`O`).
5. [] Contabilizar:
   - Número de movimientos realizados.
   - Costo total acumulado según el terreno.

## Recomendaciones

- Usar archivos de texto (`.txt` o `.csv`) para definir mapas.
- Diseñar la interfaz de manera modular para poder reutilizar componentes en prácticas posteriores.
- Considerar la extensibilidad: en el futuro se implementarán algoritmos de búsqueda sobre estos ambientes.

## Resultados esperados

- [] Sistema que **cargue, visualice y modifique mapas**.
- [] Interfaz para **consultar y editar celdas**.
- [] Simulación de un agente que **descubra progresivamente** su entorno.
- [] Opción de **control manual de un agente**, con marcadores y cálculo de costos.
