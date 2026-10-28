
```md
# Changelog

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
