Projekt nr.2 z przedmiotu systemy operacyjne 2: Wielowątkowy serwer chatu, wykonany w Pythonie z użyciem biblioteki threading, Autor: Cyprian Kozubek 272959

Instrukcje uruchomienia projektu: Program należy sklonować do używanego IDE (branch master), sprawdzić kompletność bibliotek w plikach. Uruchomić w terminalu plik server.py, komendą python server.py, następnie w nowych terminalach otworzyć plik clients.py, komendą python clients.py. Po wykonaniu tych kroków powinna być możliwość konwersacji serwera z klientami, aby skończyć rozmowę z poziomu klienta, należy wpisać "exit".

Opis problemu: W projekcie należało wykonać wielowątkowy serwer chatu, podobny do chatbota. Wielu klientów naraz może pisać wiadomości do serwera, który odpowiada każdemu klientowi. Klient widzi tylko swoje wiadomości oraz informację zwrotną z serwera, z poziomu serwera widzimy konwersację ze wszystkimi klientami, którzy wysłali wiadomość.

Wątki i co reprezentują: Wątkami w tym projekcie są klienci, którzy chcą komunikować się z serwerem

Sekcje krytyczne i ich rozwiązanie: 
1. Serwer, wielu klientów chce naraz pisać do jednego serwera i uzyskać odpowiedź. Serwer otrzymuje wiadomość i wysyła odpowiedź do klienta, następnie przechodzi do następnego klienta. 
