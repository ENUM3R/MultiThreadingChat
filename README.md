# Projekt nr.2 z przedmiotu systemy operacyjne 2:
# Wielowątkowy serwer chatu, wykonany w Pythonie z użyciem biblioteki threading, Autor: Cyprian Kozubek 
---
## Instrukcje uruchomienia projektu:
* Program należy sklonować do używanego IDE (master branch ), sprawdzić kompletność bibliotek w plikach. 
Uruchomić w terminalu plik server.py, komendą python server.py, następnie w nowych terminalach otworzyć plik clients.py, komendą python clients.py.
Po wykonaniu tych kroków powinna być możliwość konwersacji serwera z klientami.
---
## Działanie programu:
* Z poziomu serwera standardowo wysyłamy wiadomość do wszystkich klientów (broadcast), dodatkowo możemy wysłać
wiadomość do wybranego klienta z użyciem 'choose', podając jego adres portu, który widoczny jest w terminalu, oraz wiadomość,
aby zakończyć działanie serwera należy wpisać 'exit'. Z poziomu klienta wysyłamy wiadomość do wszystkich, aby zakończyć rozmowę
należy wpisać "exit". Każdy klient widzi wszystkie wiadomości, oprócz wiadomości prywatnych z serwera do innych klientów.
Serwer widzi wszystkie wiadomości klientów, także wiadomości prywatne.
---
## Opis problemu:
* W projekcie należało wykonać wielowątkowy serwer chatu, 
który umożliwia prowadzenie rozmowy z wieloma klientami jednocześnie.
Serwer umożliwia zarówno wysyłanie wiadomości bezpośrednio do wybranego klienta, jak i nadawanie wiadomości do 
wszystkich połączonych klientów (broadcasting). Klient widzi swoje wiadomości do serwera, jego odpowiedź
oraz wiadomości innych użytkowników. W projekcie dodatkowo zastosowano kolorowanie konsoli z wykorzystaniem kodów ANSI
(plik consoleColors.py). Każdy typ wiadomości (klient, serwer, błąd) ma przypisany inny kolor, 
co znacząco poprawia czytelność i estetykę komunikatów wyświetlanych w terminalu.
---
## Wątki i co reprezentują: 
1. `Dla serwera (plik server.py)`

Każdy nowy klient, który się łączy, uruchamia nowy wątek w funkcji manage_chat().
Dzięki temu serwer może obsługiwać wielu klientów jednocześnie. 
Serwer zarządza komunikacją poprzez iteracyjne odbieranie wiadomości od klientów i ich przekazywanie do wybranych odbiorców.

Dodatkowo uruchamiany jest wątek server_input_thread, który umożliwia operatorowi serwera ręczne wprowadzanie wiadomości na żywo,
które następnie są przesyłane do wszystkich połączonych klientów (broadcast) lub do wybranego klienta.

2. `Dla klienta (plik clients.py)`
Każdy klient tworzy dwa wątki:
* receive_thread – odbiera wiadomości od serwera i wyświetla je na ekranie.
* send_thread – wysyła wiadomości do serwera.
Dzięki temu klient może jednocześnie wysyłać i odbierać wiadomości, zapewniając płynną komunikację.
---
## Sekcje krytyczne i ich rozwiązanie: 
1. `Obsługa listy klientów na serwerze`
   
Problem: Wielu klientów jednocześnie wysyła wiadomości do serwera. Serwer musi obsługiwać każde połączenie osobno i przesyłać wiadomości do odpowiednich klientów.

Rozwiązanie: Serwer uruchamia nowy wątek dla każdego połączonego klienta. 
Blokada (lock) zapewnia, że tylko jeden wątek naraz może modyfikować clients_list, co zapobiega błędom związanym z równoczesnym zapisem.

2. `Wysyłanie wiadomości przez serwer do klientów`

Problem: Serwer może odpowiadać wybranemu klientowi, a w tym czasie inny klient może się połączyć lub rozłączyć.

Rozwiązanie: Serwer używa blokady (lock) przed wysłaniem wiadomości. Zapewnia to, że tylko jeden wątek naraz może modyfikować listę klientów i wysyłać wiadomości.

3. `Usuwanie klientów z listy`
   
Problem: Gdy klient się rozłącza, jego gniazdo powinno zostać poprawnie usunięte z clients_list, aby uniknąć błędów i prób wysyłania wiadomości do nieistniejącego połączenia.

Rozwiązanie: Usunięcie klienta odbywa się wewnątrz with lock, co zabezpiecza przed równoczesnym dostępem innych wątków.

---

