
```md
# Changelog

## [Unreleased]
### Changed
- Los cambios hechos desde la UI (agregar, editar, eliminar) se aplican sin reiniciar
- Reconexión automática al broker MQTT y mensajes claros de conexión/desconexión
- El simulador arranca aunque el broker no esté disponible
- Un error en un dispositivo ya no detiene su hilo
- Validación de ID duplicado, intervalo mínimo y tipo de dispositivo
- La lista de tipos de la UI se genera desde `DEVICE_TYPES`
- Rutas absolutas: se puede ejecutar desde cualquier carpeta
- `logging` en lugar de `print`
- Versiones fijas en `requirements.txt`
- Migración a la API de callbacks v2 de paho-mqtt

## [1.1.0] - 2026-10-28
### Added
- Nuevos dispositivos: Machine Monitor, Site Monitor CCH, Site Monitor INZ, IPC Monitor
- `config.example.yaml` con broker público para pruebas
- Creación automática de `config.yaml` si no existe

### Changed
- `config.yaml` ya no se versiona (configuración local)
- NRGY Monitor usa `ts` en lugar de `timestamp`
- Dockerfile expone el puerto 9876

## [1.0.0] - 2026-02-10
### Added
- Simulación de Site Monitor
- Simulación de NRGY Monitor
- Envío MQTT configurable
- Interfaz web para gestión de dispositivos
- Edición y eliminación de dispositivos
- Confirmación modal al eliminar
- Soporte para imágenes estáticas
- Dockerización del proyecto
