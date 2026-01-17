# PSI_pro_Z36

Git repository for project from PSI (Network programming) course in Warsaw University of Technology.

## Team members:

- Małgorzata Grzanka
- Aleksandra Szczypawka
- Radosława Żukowska

## ToDo

- server wielowątkowy
- typy wiadomości
- obsługa typów wiadomości
- Diffie-Helman

## Uruchomienie z interaktywnym terminalem

Program pobiera input użytkownika z terminala. Parametry konfiuracyjne pochodzą z `docker-compose.yaml`.

```
docker compose run --name server --build --rm server
docker compose run --name client --build --rm client
```

- `run` zamiast up aby można było sie komunikować przez `stdin`
- `rm` - automatycznie się sprzątnie nie trzeba usuwać
- kiedy buduję z `run` to muszę wcześniej mieć sieć
  - `docker network create tcp_network`
- dodaję --name server, ponieważ łączę się z klienta na hostname server, a ez tego kontener jest inaczej nazywany
  - możnaby przekazywać adres jako parametr a nie hardcoded "server"

## Uruchomienie - Oba równocześnie

```
docker-compose -f docker-compose.yaml up --build
```

## Usunięcie

```
docker-compose -f docker-compose.yaml down
```

## Wielowątkowość

- `daemon=True` - jakby uruchomienie w tle, jeśli główny proces zostanie zakończony to ten też
