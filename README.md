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
docker compose run --name z36_server --build --rm -e MAX_CLIENTS=10 server
```
- należy ustawić wartość parametru `MAX_CLIENTS`

### Uruchomienie klienta
```
docker compose run --name z36_client --build --rm client
```
- każdy kolejny uruchamiany kontener z klientem musi mieć inną nazwę np.
`z36_client_2`

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

## Przeprowadzenie testów i uzyskanie danych sieciowych

Uruchom serwer tak jak wspomniane wyżej, następnie w osobnych terminalu wejdź w tryb interaktywny z kontenerem serwera z terminalem sh

`docker exec -it z36_server sh`

Uruchom zbieranie danych sieciowych

`tcpdump -i eth0 -w /tmp/z36.pcap`

Przejdź do nowego terminala i uruchom klienta, prześlij wiadomości wedle uznania. Następnie w terminalu z `tcpdump` zatrzymaj jego wykonywanie `Ctrl+C`, opuść kontener `exit`. Skopiuj uzyskane pliki do folderu `tests` za pomocą polecenia `docker cp z35_server:{ścieżka do pliku} {ścieżka docelowa}`.

W programie Wireshark pobierz dane z wybranej wiadomości zaszyfrowanej do pliku, który umieść także w folderze `tests`, przejdź do tego folderu, zaktualizuj ten plik o nazwy plików z danymi i uruchom program odszyfrowujący wiadomość `python test.py`.
