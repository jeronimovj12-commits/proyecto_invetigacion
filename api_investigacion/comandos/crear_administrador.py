"""Ejecutar desde /app: python -m comandos.crear_administrador."""
import asyncio
import sys
from getpass import getpass

from seguridad.errores import ConflictoInicializacion
from servicios.ensamblador_autenticacion import crear_servicio_autenticacion


def main():
    try:
        if not sys.stdin.isatty():
            raise ValueError('Se requiere una terminal interactiva con entrada oculta; no se admiten contraseñas por tubería.')
        nombre = input('Nombre de usuario del primer administrador: ').strip()
        correo = input('Correo: ').strip()
        clave = getpass('Contraseña (mínimo 12 caracteres): ')
        if clave != getpass('Repite la contraseña: '):
            raise ValueError('Las contraseñas no coinciden.')
        asyncio.run(crear_servicio_autenticacion().crear_primero(nombre, correo, clave))
    except (ValueError, ConflictoInicializacion) as error:
        print(str(error))
        return 1
    except (EOFError, KeyboardInterrupt):
        print('Inicialización cancelada sin completar.')
        return 1
    except Exception:
        print('No se pudo inicializar: revisa configuración, migración y disponibilidad. No se muestran datos sensibles.')
        return 1
    print('Primer administrador creado. No se muestran credenciales.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
