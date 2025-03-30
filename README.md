Projekt nr.2 z przedmiotu systemy operacyjne 2: Wielowątkowy serwer chatu, wykonany w Pythonie z użyciem biblioteki threading, Autor: Cyprian Kozubek 272959

Instrukcje uruchomienia projektu: Program należy sklonować do używanego IDE (branch master), sprawdzić kompletność bibliotek w plikach. 
Uruchomić w terminalu plik server.py, komendą python server.py, następnie w nowych terminalach otworzyć plik clients.py, komendą python clients.py.
Po wykonaniu tych kroków powinna być możliwość konwersacji serwera z klientami, aby skończyć rozmowę z poziomu klienta, należy wpisać 'exit'.
Z poziomu serwera można wybrać klienta do odpowiedzi z użyciem 'change', zakończyć działanie serwera z użyciem 'end' i wysłać odpowiedź do klienta.

Opis problemu: W projekcie należało wykonać wielowątkowy serwer chatu, podobny do chatbota, który obsłuży rozmowę z wieloma klientami naraz. 
Wielu klientów naraz może pisać wiadomości do serwera, który odpowiada każdemu klientowi. 
Klient widzi tylko swoje wiadomości oraz informację zwrotną z serwera, z poziomu serwera widzimy konwersację ze wszystkimi klientami, którzy wysłali wiadomość.

Wątki i co reprezentują: 
1. Dla serwera (plik server.py)

Każdy nowy klient, który się łączy, uruchamia nowy wątek w funkcji manage_chat().
Dzięki temu serwer może obsługiwać wielu klientów jednocześnie. 
Serwer zarządza komunikacją poprzez iteracyjne odbieranie wiadomości od klientów i ich przekazywanie do wybranych odbiorców.

2. Dla klienta (plik clients.py)
Każdy klient tworzy dwa wątki:
* receive_thread – odbiera wiadomości od serwera i wyświetla je na ekranie.
* send_thread – wysyła wiadomości do serwera.

Dzięki temu klient może jednocześnie wysyłać i odbierać wiadomości, zapewniając płynną komunikację.

Sekcje krytyczne i ich rozwiązanie: 
1. Obsługa listy klientów na serwerze
   
Problem: Wielu klientów jednocześnie wysyła wiadomości do serwera. Serwer musi obsługiwać każde połączenie osobno i przesyłać wiadomości do odpowiednich klientów.

Rozwiązanie: Serwer uruchamia nowy wątek dla każdego połączonego klienta. 
Blokada (lock) zapewnia, że tylko jeden wątek naraz może modyfikować clients_list, co zapobiega błędom związanym z równoczesnym zapisem.

2. Wysyłanie wiadomości przez serwer do klientów

Problem: Serwer może odpowiadać wybranemu klientowi, a w tym czasie inny klient może się połączyć lub rozłączyć.

Rozwiązanie: Serwer używa blokady (lock) przed wysłaniem wiadomości. Zapewnia to, że tylko jeden wątek naraz może modyfikować listę klientów i wysyłać wiadomości.

3. Usuwanie klientów z listy
   
Problem: Gdy klient się rozłącza, jego gniazdo powinno zostać poprawnie usunięte z clients_list, aby uniknąć błędów i prób wysyłania wiadomości do nieistniejącego połączenia.

Rozwiązanie: Usunięcie klienta odbywa się wewnątrz with lock, co zabezpiecza przed równoczesnym dostępem innych wątków:
