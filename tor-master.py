import os
import subprocess
from termcolor import colored
import shutil

def create_userjs(socksport, controlport, dest):
    user_js_content = f"""
user_pref("extensions.torlauncher.control_port", {controlport});
user_pref("extensions.torbutton.custom.socks_port", {socksport});
user_pref("extensions.torbutton.custom.socks_host", "127.0.0.1");
user_pref("extensions.torbutton.proxies_applied", false);
user_pref("extensions.torbutton.use_privoxy", false);
user_pref("network.proxy.socks_port", {socksport});
"""
    with open(dest, "w") as file:
        file.write(user_js_content.strip())

def count_identities_and_running():
    identities = [name for name in os.listdir('.') if os.path.isdir(name) and name.startswith('TOR-IDENTITY_')]
    running_identities = []
    try:
        for identity in identities:
            process = subprocess.Popen(['pgrep', '-f', identity], stdout=subprocess.PIPE)
            output, _ = process.communicate()
            if output:
                running_identities.append(identity)
    except Exception as e:
        print(colored(f"Error al contar las identidades ejecutándose: {e}", 'red'))
    return identities, running_identities

def create_identity(identities_count):
    identity_name = f"TOR-IDENTITY_{identities_count + 1}"
    original_path = "./tor-browser"
    destination_path = identity_name

    shutil.copytree(original_path, destination_path, symlinks=True)
    # Asegurarse de comenzar los puertos por encima de los reservados para la instancia original de Tor
    base_port = 9150 + identities_count * 2 + 100  # Empieza desde un puerto superior para evitar conflictos
    control_port = base_port + 1
    socks_port = base_port

    user_js_path = os.path.join(destination_path, "Browser", "TorBrowser", "Data", "Browser", "profile.default", "user.js")
    create_userjs(socks_port, control_port, user_js_path)

    print(colored(f"Identidad {identity_name} creada con SocksPort {socks_port} y ControlPort {control_port}.", 'green'))

def start_identity(identities, running_identities):
    for identity in identities:
        if identity not in running_identities:
            identity_path = os.path.join(identity, "Browser", "start-tor-browser")
            subprocess.Popen(['nohup', identity_path, '&'])
            print(colored(f"Iniciando {identity}...", 'green'))
            break
    else:
        print(colored("Todas las identidades ya están en ejecución.", 'yellow'))

def restart_identities(identities):
    for identity in identities:
        subprocess.call(['pkill', '-f', identity])
        shutil.rmtree(identity)
    print(colored("Todas las identidades han sido reiniciadas.", 'yellow'))

def print_menu():
    identities, running_identities = count_identities_and_running()
    print(colored("Menú:", 'cyan'))
    print(colored(f"Identidades en el directorio: {len(identities)}", 'yellow'), end='')
    if running_identities:
        print(colored(f" (Ejecutándose: {', '.join(running_identities)})", 'green'))
    else:
        print()
    print("1. Crear una identidad adicional")
    print("2. Iniciar una identidad")
    print("3. Reiniciar todas las identidades")
    print("4. Salir")

def main():
    while True:
        print_menu()
        choice = input("Seleccione una opción: ")
        identities, running_identities = count_identities_and_running()
        if choice == '1':
            create_identity(len(identities))
        elif choice == '2':
            start_identity(identities, running_identities)
        elif choice == '3':
            restart_identities(identities)
        elif choice == '4':
            break
        else:
            print(colored("Opción inválida. Intente de nuevo.", 'red'))

if __name__ == "__main__":
    main()
