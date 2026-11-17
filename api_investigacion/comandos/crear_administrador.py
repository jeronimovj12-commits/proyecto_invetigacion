# Ejecuta la instruccion indicada dentro del flujo actual.
"""Ejecutar desde /app: python -m comandos.crear_administrador."""
# Carga el modulo o los modulos asyncio.
import asyncio
# Carga el modulo o los modulos sys.
import sys
# Importa getpass desde getpass para usar esas definiciones.
from getpass import getpass

# Importa ConflictoInicializacion desde seguridad.errores para usar esas definiciones.
from seguridad.errores import ConflictoInicializacion
# Importa crear_servicio_autenticacion desde servicios.ensamblador_autenticacion para usar esas definiciones.
from servicios.ensamblador_autenticacion import crear_servicio_autenticacion


# Define la funcion main con los parametros declarados; su bloque realiza esta operacion.
def main():
    # Inicia un bloque cuya excepcion se manejara en los except siguientes.
    try:
        # Ejecuta el bloque siguiente solo cuando se cumple: not sys.stdin.isatty().
        if not sys.stdin.isatty():
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('Se requiere una terminal interactiva con entrada oculta; no se admiten contraseñas por tubería.')
        # Asigna a nombre el valor calculado a la derecha.
        nombre = input('Nombre de usuario del primer administrador: ').strip()
        # Asigna a correo el valor calculado a la derecha.
        correo = input('Correo: ').strip()
        # Asigna a clave el valor calculado a la derecha.
        clave = getpass('Contraseña (mínimo 12 caracteres): ')
        # Ejecuta el bloque siguiente solo cuando se cumple: clave != getpass('Repite la contraseña: ').
        if clave != getpass('Repite la contraseña: '):
            # Lanza la excepcion indicada y detiene el flujo normal.
            raise ValueError('Las contraseñas no coinciden.')
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        asyncio.run(crear_servicio_autenticacion().crear_primero(nombre, correo, clave))
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except (ValueError, ConflictoInicializacion) as error:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        print(str(error))
        # Devuelve al llamador el resultado de la expresion indicada.
        return 1
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except (EOFError, KeyboardInterrupt):
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        print('Inicialización cancelada sin completar.')
        # Devuelve al llamador el resultado de la expresion indicada.
        return 1
    # Captura la excepcion indicada para manejarla sin dejarla propagarse.
    except Exception:
        # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
        print('No se pudo inicializar: revisa configuración, migración y disponibilidad. No se muestran datos sensibles.')
        # Devuelve al llamador el resultado de la expresion indicada.
        return 1
    # Ejecuta la instruccion o llamada indicada dentro del bloque actual.
    print('Primer administrador creado. No se muestran credenciales.')
    # Devuelve al llamador el resultado de la expresion indicada.
    return 0


# Ejecuta el bloque siguiente solo cuando se cumple: __name__ == '__main__'.
if __name__ == '__main__':
    # Lanza la excepcion indicada y detiene el flujo normal.
    raise SystemExit(main())
