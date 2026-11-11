# Justificación técnica — [nombres del grupo]

## 1. Qué construimos
API de playlist (tabla `canciones`) con los 5 endpoints del Taller 1. Fuera del material base solo agregamos lo necesario para publicarla en Vercel.

## 2. Elementos fuera del material
| # | Elemento | Dónde se usa | ¿Para qué? |
|---|---|---|---|
| 1 | Deploy en Vercel | Todo el proyecto | Publicar la API en internet |
| 2 | Variable de entorno `VERCEL` (`os.environ`) | `database.py` | Detectar que corremos en Vercel |
| 3 | SQLite en `/tmp` y `create_all` al importar | `database.py` | Poder escribir la base en Vercel |

## 3. Detalle de cada elemento
### Elemento 1: Deploy en Vercel
- ¿Qué es? Una plataforma que ejecuta la API como funciones sin servidor y le da una URL pública.
- ¿Qué necesidad resuelve? Que la API pueda probarse desde `/docs` sin instalar nada.
- ¿Qué pasaría si no lo usáramos? Solo funcionaría en `127.0.0.1`.
- ¿Riesgo o costo? Dependemos de un servicio externo y de su configuración.
- Fuente: https://vercel.com/docs/functions/runtimes/python

### Elementos 2 y 3: variable `VERCEL`, SQLite en `/tmp` y `create_all` al importar
- ¿Qué es? Vercel define la variable `VERCEL`; si existe, guardamos la base en `/tmp`, la única carpeta escribible, y creamos la tabla al cargar el módulo porque cada instancia nueva empieza con `/tmp` vacío.
- ¿Qué necesidad resuelve? Evitar errores al escribir en un disco de solo lectura y `no such table`.
- ¿Qué pasaría si no lo usáramos? La API fallaría al crear canciones en Vercel.
- ¿Riesgo o costo? Los datos se pierden al reiniciarse la instancia; para persistencia real hay que usar una base externa (p. ej. PostgreSQL), con más configuración y secretos que proteger.
- Fuente: https://vercel.com/docs/functions/runtimes/python

## 4. Conclusión
Con pocas líneas el proyecto funciona en la nube, pero aprendimos que SQLite en un entorno sin servidor solo sirve para demos.
