# 🧠 Habit Tracker — Guía de estructura del proyecto
> Jose Manuel · FastAPI + PostgreSQL + Ollama

---

## 1. Vista general

```
habit_tracker/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   ├── api.py
│   │   │   └── predictor.py       ← ejemplo del template, lo adaptaremos
│   │   └── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── errors.py
│   │   ├── events.py
│   │   ├── logging.py
│   │   └── paginator.py
│   ├── models/
│   │   ├── log.py
│   │   └── prediction.py          ← ejemplo del template, lo eliminaremos
│   ├── services/
│   │   ├── __init__.py
│   │   └── predict.py             ← ejemplo del template, lo reemplazaremos
│   ├── __init__.py
│   ├── db.py
│   └── main.py
├── ml/
├── notebooks/
├── tests/
├── .env.example
├── .gitignore
├── Dockerfile
├── Makefile
├── pyproject.toml
└── requirements.txt
```

---

## 2. La carpeta `app/` — el corazón

Todo lo que hace tu aplicación vive aquí. Cuando el servidor arranca, lo primero que ejecuta es `main.py`, y desde ahí se conecta todo lo demás.

### `app/main.py`
El punto de entrada de la aplicación. Aquí se crea la instancia de FastAPI y se registran todas las rutas.

> 💡 **Analogía:** Es como la recepción de un edificio. Toda petición HTTP pasa por aquí primero.

### `app/db.py`
Contiene la configuración de la conexión a PostgreSQL. Lee las credenciales del `.env` y crea la sesión de base de datos que usan todos los demás módulos.

> 💡 **Analogía:** Es el puente entre tu código Python y la bodega de datos (PostgreSQL).

---

## 3. `app/api/` — las rutas

Aquí viven los endpoints de tu API. Un endpoint es una URL específica que hace una acción cuando alguien la llama.

| Archivo | Contiene |
|---|---|
| `routes/__init__.py` | Archivo vacío que convierte la carpeta en módulo Python |
| `routes/api.py` | Registra y agrupa todas las rutas de la app |
| `routes/predictor.py` | Ruta de ejemplo del template (la adaptaremos) |
| `__init__.py` | Convierte `app/api/` en módulo importable |

Para nuestro proyecto crearemos rutas como:
```
routes/habits.py    → GET /habits, POST /habits, DELETE /habits/{id}
routes/logs.py      → POST /habits/{id}/check, GET /habits/{id}/history
```

---

## 4. `app/core/` — la columna vertebral

Contiene todo lo que no es lógica de negocio pero que la app necesita para funcionar bien.

| Archivo | Para qué sirve |
|---|---|
| `config.py` | Lee las variables del `.env` y las expone como objetos Python |
| `errors.py` | Define errores personalizados (ej: `HabitNotFound`, `Unauthorized`) |
| `events.py` | Acciones al iniciar o apagar el servidor (conectar BD, etc.) |
| `logging.py` | Configura cómo y dónde se guardan los registros de la app |
| `paginator.py` | Lógica para devolver listas en páginas (ej: 20 hábitos por página) |

> 💡 `config.py` es uno de los archivos más importantes. Lo editarás pronto para configurar la conexión a PostgreSQL.

---

## 5. `app/models/` — las tablas

Aquí defines cómo se ven tus datos en la base de datos. SQLAlchemy lee estas definiciones y crea las tablas reales en PostgreSQL automáticamente. Nunca tienes que escribir `CREATE TABLE` manualmente.

| Archivo actual | Contenido |
|---|---|
| `log.py` | Modelo de ejemplo (lo adaptaremos para `habit_logs`) |
| `prediction.py` | Modelo del template (lo eliminaremos) |

Para nuestro proyecto crearemos:
```
models/habit.py      → tabla habits (id, nombre, frecuencia, fecha_creación)
models/habit_log.py  → tabla habit_logs (id, habit_id, fecha, cumplido)
```

> 💡 **Analogía:** Un modelo es el plano de una tabla. El ORM construye la tabla real a partir del plano.

---

## 6. `app/services/` — la lógica

La capa más importante para el negocio. Aquí va toda la lógica que no es solo guardar o traer datos.

Ejemplos de lo que irá aquí:
- Calcular la racha (streak) de un hábito
- Verificar que un usuario solo pueda editar sus propios hábitos
- Calcular el porcentaje de cumplimiento del mes
- Llamar a Ollama para generar sugerencias con IA

| Archivo actual | Contenido |
|---|---|
| `predict.py` | Servicio de ejemplo del template (lo reemplazaremos) |
| `__init__.py` | Convierte la carpeta en módulo importable |

> 💡 **Regla de oro:** Si la lógica tiene más de 2 pasos o condiciones, va en `services/`, no en el router.

---

## 7. Archivos en la raíz

### `.env.example`
Plantilla del archivo `.env`. Muestra qué variables necesita la app sin revelar valores reales. Este **SÍ** se sube a GitHub.

Tú crearás un `.env` con tus contraseñas reales. Ese **NUNCA** se sube a GitHub.

### `.gitignore`
Le dice a Git qué archivos ignorar. Ya viene configurado para ignorar `.env`, `venv`, caché de Python, etc.

> ⚠️ Verifica que `.env` esté en este archivo. Es crítico para no subir contraseñas a GitHub.

### `pyproject.toml`
Configuración moderna del proyecto Python. Define nombre, versión, dependencias y herramientas como el linter.

### `Dockerfile`
Permite empaquetar la app en un contenedor Docker para desplegarla en cualquier servidor. No lo tocaremos por ahora.

### `Makefile`
Define comandos cortos para tareas repetitivas. En lugar de escribir `uvicorn app.main:app --reload`, puedes definir `make run`.

---

## 8. El flujo completo de una petición

Cuando el frontend dice *"dame mis hábitos"*, esto pasa internamente:

```
Request HTTP
     │
     ▼
main.py          → recibe la petición
     │
     ▼
api/routes/      → identifica el endpoint correcto
     │
     ▼
services/        → aplica la lógica de negocio
     │
     ▼
models/          → consulta PostgreSQL
     │
     ▼
core/            → maneja errores si algo falla
     │
     ▼
Response JSON    → regresa al frontend
```

> 💡 Cada capa hace **una sola cosa**. Si una capa empieza a hacer el trabajo de otra, es señal de que algo está mal organizado.

---

## 9. ¿Qué vamos a adaptar del template?

| Acción | Archivo(s) |
|---|---|
| ❌ Eliminar o reemplazar | `models/prediction.py`, `services/predict.py`, `routes/predictor.py` |
| 🔧 Adaptar | `models/log.py` → lo convertimos en `habit_log.py` |
| ✅ Crear desde cero | `models/habit.py`, `services/habit_service.py`, `routes/habits.py` |
| ⚙️ Configurar | `core/config.py` → conexión a PostgreSQL y variables de entorno |

> ⚠️ No borres nada todavía. Primero entiende cómo funciona el template y luego lo adaptamos juntos.

---

## 10. Próximos pasos

- [ ] Instalar dependencias con `pip install -r requirements.txt`
- [ ] Configurar el archivo `.env` con las credenciales de PostgreSQL
- [ ] Adaptar `core/config.py` para conectar con `habit_tracker`
- [ ] Crear el primer modelo: `Habit` en `models/habit.py`
- [ ] Arrancar el servidor y ver la documentación automática de FastAPI

---

> 🚀 **¡Vamos con todo!**