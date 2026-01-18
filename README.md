# PSI_pro_Z36

Git repository for project from PSI (Network programming) course in Warsaw University of Technology.

## Team members:

- Małgorzata Grzanka
- Aleksandra Szczypawka
- Radosława Żukowska


## Uruchomienie

Program pobiera input użytkownika dlatego należy uruchomić w osobnych terminalach. Parametry konfiuracyjne pochodzą z `docker-compose.yaml`.

```
git clone https://github.com/radoslawazukowska/PSI_pro_Z36.git
cd PSI_pro_Z36
```

### Uruchomienie serwera
```
docker compose run --name z36_server --build --rm server
```

### Uruchomienie klienta
```
docker compose run --name z36_client --build --rm client
```

## Obsługa
Programy `klienta` oraz `serwera` obsługujemy z wiersza poleceń.
### Server
Obsługiwane polecenia:
- `LIST` - wyświetla listę połączonych klientów (format: id, adres)
- `DELETE <ID>` - kończy połączenie dla klienta o wskazanych id

### Klient
Obsługiwane polecenia:
- `CONNECT` - nawiązuje połączenie z serwerem
- `MSG` - wysyła wiadamość do serwera
- `END` - kończy połączenie z serwerem
