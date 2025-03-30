Projekt nr.2 z przedmiotu systemy operacyjne 2: Wielowątkowy serwer chatu, wykonany w Pythonie z użyciem biblioteki threading, Autor: Cyprian Kozubek 272959

Instrukcje uruchomienia projektu: Program należy sklonować do używanego IDE (branch master), sprawdzić kompletność bibliotek w plikach. Uruchomić w terminalu plik server.py, komendą python server.py, następnie w nowych terminalach otworzyć plik clients.py, komendą python clients.py. Po wykonaniu tych kroków powinna być możliwość konwersacji serwera z klientami, aby skończyć rozmowę z poziomu klienta, należy wpisać "exit".

Opis problemu: W projekcie należało wykonać wielowątkowy serwer chatu, podobny do chatbota. Wielu klientów naraz może pisać wiadomości do serwera, który odpowiada każdemu klientowi. Klient widzi tylko swoje wiadomości oraz informację zwrotną z serwera, z poziomu serwera widzimy konwersację ze wszystkimi klientami, którzy wysłali wiadomość.

Wątki i co reprezentują: 
1. Dla serwera (plik server.py)
Każdy nowy klient, który się łączy, uruchamia nowy wątek w funkcji manage_chat(). Dzięki temu serwer może obsługiwać wielu klientów jednocześnie. Serwer zarządza komunikacją poprzez iteracyjne odbieranie wiadomości od klientów i ich przekazywanie do wybranych odbiorców.
2. Dla klienta (plik clients.py)
Każdy klient tworzy dwa wątki:
* receive_thread – odbiera wiadomości od serwera i wyświetla je na ekranie.
* send_thread – wysyła wiadomości do serwera.
Dzięki temu klient może jednocześnie wysyłać i odbierać wiadomości, zapewniając płynną komunikację.

Sekcje krytyczne i ich rozwiązanie: 
1. Sekcja krytyczna – obsługa wielu klientów przez serwer
   
Problem: Wielu klientów jednocześnie wysyła wiadomości do serwera. Serwer musi obsługiwać każde połączenie osobno i przesyłać wiadomości do odpowiednich klientów.
Rozwiązanie: Serwer uruchamia nowy wątek dla każdego połączonego klienta (thread = threading.Thread(target=manage_chat, args=(client_socket,client_address))).

Do ochrony dostępu do listy klientów (clients_list) użyto blokady (lock):
with lock:
    clients_list[client_address] = client_socket
    
Dzięki temu tylko jeden wątek może modyfikować clients_list w danym momencie, co zapobiega błędom związanym z równoczesnym zapisem.

2.Sekcja krytyczna – wysyłanie wiadomości do klientów

Problem: Wiele wątków serwera może jednocześnie próbować wysyłać wiadomości do różnych klientów.

Rozwiązanie: Przy wysyłaniu wiadomości do wszystkich klientów również stosowane jest lock:
with lock:
    for client_addr, client_sock in clients_list.items():
        if client_sock != client_socket:
            try:
                client_sock.send(msg.encode())
            except Exception as e:
                print(f"Error sending message to {client_addr}: {e}")
Zapobiega to sytuacji, w której dwóch wątków jednocześnie próbuje iterować po clients_list i wysyłać wiadomości, co mogłoby prowadzić do błędów.

3. Sekcja krytyczna – usuwanie klientów z listy
   
Problem: Gdy klient się rozłącza, jego gniazdo powinno zostać poprawnie usunięte z clients_list, aby uniknąć błędów i prób wysyłania wiadomości do nieistniejącego połączenia.

Rozwiązanie: Usunięcie klienta odbywa się wewnątrz with lock, aby uniknąć problemów wynikających z dostępu do clients_list przez inne wątki:
with lock:
    del clients_list[client_address]
