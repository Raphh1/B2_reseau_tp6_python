import asyncio

# Dictionnaire global pour stocker les informations des clients
CLIENTS = {}

async def send_to_all(message, sender_addr):
    # Envoyer le message à tous les clients, sauf à l'émetteur
    for addr, client_info in CLIENTS.items():
        if addr != sender_addr:
            writer = client_info["w"]
            writer.write(message.encode())
            await writer.drain()

async def handle_client(reader, writer):
    # Récupérer l'adresse du client
    addr = writer.get_extra_info('peername')
    
    # Attendre le pseudo du client
    data = await reader.read(100)
    pseudo = data.decode().split('|')[1]
    CLIENTS[addr] = {"r": reader, "w": writer, "pseudo": pseudo}

    # Annoncer l'arrivée du client à tout le monde
    announcement = f"Annonce : {pseudo} a rejoint la chatroom\n"
    await send_to_all(announcement, addr)

    try:
        while True:
            data = await reader.read(100)
            message = data.decode()
            
            if not message:
                # Le client s'est déconnecté
                break

            # redistribuer le message à tout le monde
            sender_pseudo = CLIENTS[addr]["pseudo"]
            redistributed_message = f"{sender_pseudo} a dit : {message}"
            await send_to_all(redistributed_message, addr)

    except asyncio.CancelledError:
        pass

    finally:
        # Le client s'est déconnecté
        writer.close()
        await writer.wait_closed()

        # Retirer le client du dictionnaire
        del CLIENTS[addr]

        # Annoncer le départ du client à tout le monde
        departure_announcement = f"Annonce : {pseudo} a quitté la chatroom\n"
        await send_to_all(departure_announcement, addr)

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 12345)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
