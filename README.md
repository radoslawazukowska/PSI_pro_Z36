# PSI_pro_Z36

Git repository for project from PSI (Network programming) course in Warsaw University of Technology.

## Team members:

- Małgorzata Grzanka
- Aleksandra Szczypawka
- Radosława Żukowska

## Uruchomienie z interaktywnym terminalem

Program pobiera input użytkownika z terminala. Parametry konfiuracyjne pochodzą z `docker-compose.yaml`.

```
docker-compose run server
docker-compose run client
```

## Uruchomienie

### Oba równocześnie

```
docker-compose -f docker-compose.yaml up --build
```

## Usunięcie

```
docker-compose -f docker-compose.yaml down
```
