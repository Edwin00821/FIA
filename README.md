# FIA

Este repositorio contiene las diferentes **prácticas de laboratorio** de la materia de **Fundamentos de Inteligencia Artificial (FIA)**.  
El proyecto está organizado por carpetas, cada una corresponde a una práctica distinta (ejemplo: `agents-lab`).

## 📂 Estructura del Proyecto

```
FIA/
│── .devcontainer/ # Configuración de Dev Containers
│── agents-lab/ # Práctica 1: Agentes
│── README.md
```

Cada práctica tendrá:

- Su propio directorio (`*-lab`).
- Un archivo principal de ejecución.
- Archivos auxiliares (mapas, configuraciones, etc).

## 🐳 Entorno de Desarrollo

El proyecto está preparado para usarse con **Dev Containers** de VS Code.  
Esto permite que todos los colaboradores tengan el mismo entorno sin configurar nada manualmente.

### Requisitos

- [Docker](https://www.docker.com/)
- [VS Code](https://code.visualstudio.com/)
- Extensión **Dev Containers** de VS Code

### Configuración Automática

Al abrir este repositorio en VS Code, selecciona **"Reopen in Container"**.  
El contenedor incluye:

- Python 3.12
- Librerías para trabajar con interfaces gráficas y SDL
- Extensiones de VS Code para Python y herramientas de desarrollo

## ▶️ Ejecución de Prácticas

Para ejecutar una práctica:

1. Abre el contenedor (`Dev Container`) en VS Code.
2. Entra al directorio de la práctica:

   ```bash
   cd agents-lab
   ```

3. Ejecuta el archivo principal de la práctica:

   ```bash
   python main.py
   ```

_(el nombre puede variar según la práctica, se documentará en cada carpeta)._

## 📦 Dependencias Específicas

- El contenedor ya incluye dependencias básicas (Python + librerías de C/SDL).
- Si alguna práctica necesita librerías adicionales de Python, agrega un archivo `requirements.txt` dentro de esa práctica y ejecútalo con:

  ```bash
  pip install -r requirements.txt
  ```

> ⚠️ No es necesario crear un `.venv` en cada práctica, ya que el Dev Container gestiona el entorno global de desarrollo.

## 📘 Prácticas

- **agents-lab** (Práctica 1)
  Construcción de agentes en entornos discretos (laberintos, tableros, terrenos).
  Incluye:

  - [x] Carga y visualización de mapas
  - [] Interacción con el entorno
  - [] Creación de agentes con diferentes sensores y acciones

_(Más prácticas se irán agregando conforme avance el curso)._

---

## 🌳 Estrategia de Branches (Flujo de Trabajo en Git)

Este repositorio será desarrollado por **4 personas en equipo** y cada práctica evoluciona a partir de la anterior.  
Por ello, necesitamos un flujo de ramas que nos permita:

- Mantener un **historial claro de cada práctica**.
- Poder **volver a cualquier versión terminada** (útil para revisiones o entregas).
- Facilitar el **trabajo colaborativo sin conflictos**.

### 📂 Estructura de Ramas

1. **`main`**

   - Contiene únicamente las prácticas **terminadas y validadas**.
   - Siempre representa el estado **estable y entregable** del proyecto.
   - Se mergea aquí solo cuando una práctica ya está lista.

   > **Por qué**: Mantener `main` estable evita que se suba código incompleto o en desarrollo. Esto asegura que siempre tengamos una versión lista para revisión/entrega.

2. **`practice-N` (ejemplo: `practice-1`, `practice-2`, …)**

   - Cada práctica tiene su propia rama.
   - La **práctica N** se crea a partir de la práctica anterior (`practice-2` nace de `practice-1`).
   - En esta rama se desarrolla todo el trabajo conjunto de la práctica hasta completarla.

   > **Por qué**: Como las prácticas se construyen sobre las anteriores, tener una rama específica garantiza que cada versión se conserve en el historial y podamos revisitarla sin perder el contexto.

3. **Branches personales/feature**

   - Cada integrante trabaja en su propia rama derivada de la práctica actual.
   - Ejemplo para práctica 2:
     - `practice-2-bfs`
     - `practice-2-dfs`
     - `practice-2-ids`
     - `practice-2-ui`

   > **Por qué**: Permite que los 4 trabajen en paralelo sin pisarse el trabajo. Cada quien hace commits en su rama y luego se integran en la rama central de la práctica (`practice-2`) mediante Pull Requests.

### 🔀 Flujo de Trabajo Paso a Paso

1. **Crear la rama de práctica desde la anterior**
   ```bash
   git checkout -b practice-2 practice-1
   ```

> Se garantiza que la práctica 2 parte exactamente de la versión final de la práctica 1.

2. **Cada desarrollador crea su rama personal/feature desde la rama de práctica**

   ```bash
   git checkout -b practice-2-bfs practice-2
   ```

> Evita conflictos entre desarrolladores y permite trabajar de forma aislada en una parte específica.

3. **Trabajar y subir los cambios**

   ```bash
   git add .
   git commit -m "feat(bfs): implement breadth-first search"
   git push origin practice-2-bfs
   ```

> Usamos [Conventional Commits](https://www.conventionalcommits.org/) para que los mensajes sean claros y fáciles de leer en el historial.

4. **Pull Request (PR) hacia la rama de práctica**

   - Cuando el trabajo en la rama personal está listo → abrir un PR hacia `practice-2`.

   - Los demás revisan el código y, si todo está bien, se aprueba y se hace merge.

   > **Por qué**: Los PR permiten revisión entre compañeros, asegurando calidad y evitando errores.

---

5. **Finalización de la práctica**

   - Una vez que `practice-2` contiene todo el trabajo validado → se mergea a `main`.

   ```bash
   git checkout main
   git merge practice-2
   git push origin main
   ```

> **Por qué**: Así `main` siempre refleja la versión final y lista para entrega de cada práctica.

---

6. **Etiquetado de versiones (tags)**

   - Para marcar versiones importantes (fin de cada práctica), se crean tags:

   ```bash
   git tag v1.0-practice-1
   git tag v2.0-practice-2
   git push origin --tags
   ```

   > **Por qué**: Los tags permiten regresar fácilmente a cualquier práctica específica sin depender de ramas.

### 📊 Resumen Visual del Flujo

```
main
 │
 ├── practice-1
 │    ├── app
 │    └── core
 │
 ├── practice-2 (desde practice-1)
 │    ├── app
 │    └── core
 │
 └── practice-3 (desde practice-2)
      ├── ...
```

✅ Con este flujo logramos:

- Historial limpio y versionado por práctica.
- Colaboración en paralelo sin conflictos.
- Revisión de código entre compañeros.
- Entregables claros en `main` y accesibles mediante `tags`.

---

✍️ **Profesor**: Edgar A. Catalán Salgado
👨‍💻 **Integrantes**:

- Astudillo Pérez Edwin Uriel
