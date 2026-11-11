# Respuestas — Taller 1

1. Sin `table=True`, `Cancion` sería solo una clase de Python (como `CancionBase`): no se crearía la tabla.
2. El `id` es `int | None` porque antes de guardar todavía no existe; la base de datos lo genera.
3. **404**: el recurso no existe (`GET /canciones/99`). **422**: los datos enviados no son válidos (un `POST` sin `titulo` o con `duracion_segundos: 0`).
4. `index=True` acelera las búsquedas por ese campo. No está en `duracion_segundos` porque no la usamos para buscar, y cada índice ocupa espacio y hace más lentas las escrituras.
5. Agregar `album` al modelo, borrar `database.db` y reiniciar, porque `create_all` no modifica tablas que ya existen.
6. `commit()` guarda, pero el `id` lo asigna la base de datos; `refresh()` vuelve a leer la fila para traerlo y devolver la canción completa.
7. `PUT` reemplaza todos los campos; `PATCH` cambia solo los que se envían.
