Zanim przedstawię nowy plan, przeprowadziłem **audyt poprzedniego**. 

**Wnioski z audytu:**
1. **Zbyt wysoki poziom ogólności:** "Implementacja Monte Carlo" to w rzeczywistości 3 dni pracy (teoria $\rightarrow$ kod $\rightarrow$ analiza $\rightarrow$ poprawki). 
2. **Brak pętli zwrotnej:** Poprzedni plan był liniowy. W prawdziwym researchu po testach statystycznych często trzeba wrócić do parametrów. 
3. **Ryzyko "pustego kodu":** Istniało ryzyko, że napiszesz funkcję, ale nie zrobisz analizy wyników. 
4. **Słaby punkt:** Przejście między miesiącem 2 (sygnały) a 3 (portfel) było zbyt gwałtowne. Brakuje etapu "wyboru najlepszych alf".

**Poprawki wprowadzone do nowego planu:**
*   **Atomizacja zadań:** Każdy dzień jest teraz podzielony na 3-5 konkretnych kroków (od teorii/projektowania, przez kod, po weryfikację).
*   **Wprowadzenie "Checkpointów":** Co tydzień pojawia się zadanie weryfikacyjne.
*   **Zwiększenie rygoru:** Dodano zadania dotyczące czyszczenia danych i obsługi błędów (exception handling), co jest kluczowe w systemach automatycznych.

Oto Twój nowy, zatomizowany plan **"Quant Lab to Mini Fund"** na 90 dni.

---

### 🟦 MIESIĄC 1: HARDENING & ROBUSTNESS (ODPORNOŚĆ)
*Cel: Budowa rygorystycznego procesu walidacji, który zabija złe pomysły.*

**Tydzień 1: Advanced Regime Integration**
*   **Dzień 1:** (1) Refaktoryzacja `get_indicators` do klasy `RegimeClassifier`, (2) Definicja parametrów regimów (Slope, Volatility), (3) Test jednostkowy klasyfikatora na jednym aktywie.
*   **Dzień 2:** (1) Kodowanie filtru "No-Trade Zone" (blokada wejść w Sideways), (2) Implementacja przełącznika regimów w `run_backtest`, (3) Porównanie Equity Curve z filtrem i bez.
*   **Dzień 3:** (1) Analiza korelacji: zwroty strategii vs aktualny regim, (2) Wyznaczenie "Worst Case Regime", (3) Optymalizacja parametrów wejścia specyficznie pod regime Bearish.
*   **Dzień 4:** (1) Projektowanie dynamicznych parametrów (SMA_fast zależny od Volatility), (2) Implementacja mapowania `Volatility` $\rightarrow$ `SMA_period`, (3) Testy porównawcze z parametrami stałymi.
*   **Dzień 5:** (1) Budowa modułu wizualizacji: nakładka kolorów regimów na wykres ceny, (2) Dodanie wskaźnika "Regime Duration" (ile dni trwa dany stan), (3) Weryfikacja wizualna zgodności sygnałów z regimem.
*   **Dzień 6:** (1) Testy na 3 różnych klasach aktywów (Krypto, Tech, Gold), (2) Analiza: czy ten sam klasyfikator regimów działa wszędzie?, (3) Korekta progów (thresholds) dla różnych aktywów.
*   **Dzień 7:** **CHECKPOINT:** (1) Podsumowanie Sharpe Ratio dla każdego regimu, (2) Decyzja: które regimy są profitowalne, (3) Sprzątanie kodu i dokumentacja modułu Regime.

**Tydzień 2: Optimization & Sensitivity (Walk-Away Test)**
*   **Dzień 8:** (1) Implementacja `GridSearch` dla 3 parametrów jednocześnie, (2) Zapisywanie wyników do ramki DataFrame, (3) Sortowanie wyników według Sharpe Ratio.
*   **Dzień 9:** (1) Budowa Heatmapy 2D dla dwóch głównych parametrów, (2) Analiza "wysp zysku" (szukanie obszarów stabilnych, nie szczytów), (3) Wybór parametrów z centrum stabilnego obszaru.
*   **Dzień 10:** (1) Kodowanie testu wrażliwości (Sensitivity Test): zmiana parametrów o $\pm 5\%$, (2) Obliczanie odchylenia standardowego wyniku przy zmianie parametrów, (3) Oznaczenie strategii jako "Fragile" lub "Robust".
*   **Dzień 11:** (1) Implementacja "Parameter Stability Score", (2) Porównanie wyników: najwyższy zysk vs najwyższa stabilność, (3) Wybór finalnego zestawu parametrów na bazie stabilności.
*   **Dzień 12:** (1) Budowa funkcji do automatycznego podziału danych na In-Sample (IS) i Out-of-Sample (OOS), (2) Optymalizacja na IS, (3) Pierwszy "ślepy" test na OOS.
*   **Dzień 13:** (1) Analiza degradacji wyników: $\frac{Sharpe_{OOS}}{Sharpe_{IS}}$, (2) Identyfikacja przyczyn overfittingu, (3) Uproszczenie strategii w celu poprawy wyników OOS.
*   **Dzień 14:** **CHECKPOINT:** (1) Raport z testu OOS, (2) Weryfikacja: czy strategia nadal ma edge?, (3) Finalizacja modułu `Optimizer`.

**Tydzień 3: Walk-Forward Validation (WFW) – CORE**
*   **Dzień 15:** (1) Projektowanie schematu okien (Train window vs Test window), (2) Implementacja funkcji `create_wf_splits`, (3) Wizualizacja okien na osi czasu.
*   **Dzień 16:** (1) Kodowanie pętli WFW: Optymalizacja w oknie $N$ $\rightarrow$ Test w oknie $N+1$, (2) Zapisywanie wyników z każdego okna testowego, (3) Obsługa błędów przy zbyt małej ilości danych w oknie.
*   **Dzień 17:** (1) Implementacja "WFW Equity Curve" (zszywanie wyników z okien testowych), (2) Porównanie krzywej WFW z krzywą z pełnego backtestu, (3) Obliczanie Max Drawdown dla krzywej WFW.
*   **Dzień 18:** (1) Analiza stabilności parametrów w czasie (czy w każdym oknie wygrywają te same parametry?), (2) Wykres zmian parametrów w czasie, (3) Wykrywanie "dryftu" strategii.
*   **Dzień 19:** (1) Obliczanie "WFW Efficiency Ratio", (2) Testowanie różnych rozmiarów okien treningowych, (3) Optymalizacja długości okna pod konkretny aktyw.
*   **Dzień 20:** (1) Implementacja mechanizmu "Early Exit" w WFW (zatrzymanie jeśli equity spada poniżej X), (2) Testowanie wpływu stop-lossu na wynik WFW, (3) Porównanie z Buy & Hold w każdym oknie.
*   **Dzień 21:** **CHECKPOINT:** (1) Finalna krzywa WFW dla SMA, (2) Weryfikacja: czy strategia jest "predictive" czy tylko "fitted"?, (3) Dokumentacja procesu WFW.

**Tydzień 4: Statistical Validation (The Truth)**
*   **Dzień 22:** (1) Teoria Monte Carlo dla trade'ów, (2) Implementacja funkcji losującego kolejność transakcji, (3) Generowanie 1000 alternatywnych ścieżek kapitału.
*   **Dzień 23:** (1) Budowa histogramu Max Drawdown z symulacji MC, (2) Obliczanie prawdopodobieństwa bankructwa (Risk of Ruin), (3) Wyznaczenie 95% przedziału ufności dla finalnego zwrotu.
*   **Dzień 24:** (1) Implementacja Bootstrapingu stóp zwrotu, (2) Tworzenie syntetycznych serii czasowych, (3) Analiza rozkładu zwrotów (czy jest "gruby ogon" - Fat Tails?).
*   **Dzień 25:** (1) Implementacja testu p-value (czy wynik jest istotny statystycznie?), (2) Budowa hipotezy zerowej (strategia = random), (3) Obliczanie prawdopodobieństwa, że wynik jest dziełem przypadku.
*   **Dzień 26:** (1) Implementacja "Equity Curve Permutation Test", (2) Porównanie rzeczywistej krzywej z tysiącem losowych krzywych, (3) Wizualizacja pozycji strategii na tle szumu.
*   **Dzień 27:** (1) Budowa zintegrowanego "Robustness Score" (Waga: WFW + MC + p-value), (2) Stworzenie tabeli rankingowej dla różnych wersji strategii, (3) Wybór finalnego "Zwycięzcy".
*   **Dzień 28:** **CHECKPOINT:** (1) Kompletny raport statystyczny dla SMA, (2) Decyzja: "Wdrażamy do biblioteki" lub "Odrzucamy pomysł", (3) Archiwizacja wyników.

---

### 🟨 MIESIĄC 2: ALPHA ENGINE (SZYBKI RESEARCH SYGNAŁÓW)
*Cel: Budowa biblioteki niezależnych sygnałów (Alf) i ich wzajemna kombinacja.*

**Tydzień 5: Mean Reversion Framework**
*   **Dzień 29:** (1) Implementacja RSI i Bollinger Bands, (2) Budowa sygnałów "Extreme Overbought/Oversold", (3) Testy wstępne na danych dziennych.
*   **Dzień 30:** (1) Implementacja Z-Score dla odchylenia od średniej, (2) Kodowanie wejść na poziomie $\pm 2\sigma$, (3) Analiza czasu przebywania w pozycji.
*   **Dzień 31:** (1) Budowa logiki wyjścia "Return to Mean" (zamknij gdy cena dotknie średniej), (2) Testowanie dynamicznego TP na bazie ATR, (3) Porównanie z TP stałym %.
*   **Dzień 32:** (1) Integracja z modułem Regime: Testowanie Mean Reversion tylko w Sideways, (2) Analiza: czy Mean Reversion naprawia straty SMA w konsolidacji?, (3) Optymalizacja parametrów pod regim Sideways.
*   **Dzień 33:** (1) Implementacja filtrów wolumenowych dla Mean Reversion (szukanie "wyczerpania" trendu), (2) Testowanie sygnałów na podstawie "Volume Spikes", (3) Weryfikacja win-rate.
*   **Dzień 34:** (1) Backtest Mean Reversion na 5 różnych aktywach, (2) Analiza: które aktywa są "mean-reverting", a które "trending"?, (3) Budowa mapy korelacji aktywów do tej strategii.
*   **Dzień 35:** **CHECKPOINT:** (1) Porównanie: SMA vs Mean Reversion, (2) Obliczenie korelacji między ich krzywymi kapitału, (3) Wybór parametrów "Alpha 1" (Mean Reversion).

**Tydzień 6: Momentum & Trend Following**
*   **Dzień 36:** (1) Implementacja MACD i ROC (Rate of Change), (2) Budowa sygnałów "Momentum Confirmation", (3) Testy na aktywach o wysokiej zmienności (BTC).
*   **Dzień 37:** (1) Implementacja strategii "Donchian Channel Breakout", (2) Kodowanie filtrów fałszywych wybić (False Breakouts), (3) Analiza Max Drawdown w trendach bocznych.
*   **Dzień 38:** (1) Implementacja "Multi-Timeframe Analysis" (Sygnał na D1 $\rightarrow$ Wejście na H1), (2) Kodowanie synchronizacji ram czasowych w Pandas, (3) Testowanie poprawy precyzji wejścia.
*   **Dzień 39:** (1) Implementacja "Momentum Ignition" (Cena $\uparrow$ + Wolumen $\uparrow$ + Volatility $\uparrow$), (2) Budowa logiki wejścia w "wybuchy" cenowe, (3) Testy na akcjach wzrostowych (Growth Stocks).
*   **Dzień 40:** (1) WFW dla strategii Momentum, (2) Optymalizacja długości okien trendowych, (3) Weryfikacja stabilności parametrów.
*   **Dzień 41:** (1) Budowa zestawienia "Regime vs Momentum", (2) Analiza: w którym momencie trend zamienia się w konsolidację?, (3) Implementacja sygnału wyjścia "Trend Exhaustion".
*   **Dzień 42:** **CHECKPOINT:** (1) Wybór parametrów "Alpha 2" (Momentum), (2) Porównanie: Alpha 1 vs Alpha 2, (3) Analiza korelacji między nimi (szukamy wartości < 0.3).

**Tydzień 7: Advanced Feature Engineering**
*   **Dzień 43:** (1) Implementacja Lagged Returns (opóźnione zwroty), (2) Budowa macierzy autokorelacji zwrotów, (3) Wybór optymalnych lagów dla różnych aktywów.
*   **Dzień 44:** (1) Implementacja wskaźników zmienności (Parkinson, Garman-Klass), (2) Budowa "Volatility Regime" (Low/Medium/High), (3) Testowanie wpływu zmienności na win-rate.
*   **Dzień 45:** (1) Kodowanie modułu skalowania: Z-Score Scaling i Robust Scaling, (2) Implementacja "Rolling Window Scaling" (uniknięcie look-ahead bias), (3) Testy na danych o różnych skalach (BTC vs AAPL).
*   **Dzień 46:** (1) Implementacja "Relative Strength" (Aktywo / S&P500), (2) Budowa rankingu siły aktywów, (3) Testowanie strategii "Buy Strongest, Sell Weakest".
*   **Dzień 47:** (1) Budowa klasy `FeatureGenerator`, (2) Automatyzacja tworzenia 30+ wskaźników jednym wywołaniem, (3) Optymalizacja pamięciowa (użycie `float32`).
*   **Dzień 48:** (1) Implementacja analizy korelacji między feature'ami, (2) Usuwanie redundantnych wskaźników (Multicollinearity check), (3) Wybór "Top 10" najważniejszych feature'ów.
*   **Dzień 49:** **CHECKPOINT:** (1) Audyt biblioteki feature'ów, (2) Weryfikacja: czy mamy dane do budowy sygnałów ML w przyszłości?, (3) Dokumentacja wejść i wyjść modułu `features()`.

**Tydzień 8: Signal Integration (The Voting System)**
*   **Dzień 50:** (1) Projekt architektury "Multi-Signal Ensemble", (2) Definicja interfejsu dla każdego sygnału (klasy `SignalBase`), (3) Implementacja modułu `SignalAggregator`.
*   **Dzień 51:** (1) Implementacja "Simple Voting" (Sygnał = $\text{mean}(\text{all signals})$), (2) Testowanie progów aktywacji (np. wejdź tylko gdy $\text{vote} > 0.7$), (3) Porównanie z pojedynczymi alfami.
*   **Dzień 52:** (1) Implementacja wagowania sygnałów (Weighted Average), (2) Przypisywanie wag na podstawie historycznego Sharpe Ratio każdego sygnału, (3) Testy stabilności wag.
*   **Dzień 53:** (1) Budowa "Regime-Based Switching" (W regimie A używaj Alfy 1, w regimie B Alfy 2), (2) Kodowanie logiki przełączania, (3) Analiza poprawy Equity Curve.
*   **Dzień 54:** (1) Analiza "Signal Diversification" (wykresy rozrzutu sygnałów), (2) Obliczanie korelacji błędów sygnałów, (3) Optymalizacja zestawu alf w celu minimalizacji korelacji.
*   **Dzień 55:** (1) Optymalizacja wag sygnałów za pomocą prostego algorytmu genetycznego lub GridSearch, (2) Walidacja wag na OOS, (3) Obliczanie "Ensemble Sharpe Ratio".
*   **Dzień 56:** **CHECKPOINT:** (1) Finalny wybór zestawu sygnałów do portfela, (2) Raport: "Dlaczego ten zestaw?", (3) Zamrożenie wersji "Alpha Engine v1".

---

### 🟥 MIESIĄC 3: MINI QUANT FUND (PORTFOLIO & AUTOMATION)
*Cel: Transformacja narzędzia researchowego w zautomatyzowany system zarządzania kapitałem.*

**Tydzień 9: Advanced Risk Management**
*   **Dzień 57:** (1) Implementacja "Equity-Based Sizing" (Risk per trade = 1% equity), (2) Budowa funkcji obliczania wielkości pozycji na bazie dystansu do SL, (3) Testowanie wpływu na Drawdown.
*   **Dzień 58:** (1) Implementacja "Volatility Adjusted Sizing" (Volatility Targeting), (2) Budowa mechanizmu redukcji pozycji przy wzrostach zmienności, (3) Porównanie z stałą wielkością pozycji.
*   **Dzień 59:** (1) Budowa systemu "Portfolio Heat" (Limit łącznej ekspozycji, np. max 300% lewaru), (2) Implementacja twardych limitów na jeden sektor/asset, (3) Kodowanie logiki odrzucania sygnałów przy pełnym "cieple".
*   **Dzień 60:** (1) Implementacja "Trailing Stop" (przesuwanie SL wraz z ceną), (2) Budowa "Time-based Stop" (zamknij po X dniach bez ruchu), (3) Analiza wpływu na Win-Rate vs Average Win.
*   **Dzień 61:** (1) Testowanie "Risk-Adjusted Returns" (Sortino Ratio), (2) Analiza "Ulcer Index" (miara stresu inwestora), (3) Optymalizacja parametrów Risk Managementu.
*   **Dzień 62:** (1) Implementacja "Kelly Criterion" (uproszczona wersja), (2) Testowanie "Fractional Kelly" (np. 0.25 Kelly) dla bezpieczeństwa, (3) Porównanie z Equal Weighting.
*   **Dzień 63:** **CHECKPOINT:** (1) Budowa modułu `risk_manager()`, (2) Testy: czy `risk_manager` poprawnie blokuje zbyt ryzykowne sygnały?, (3) Finalizacja logiki zarządzania kapitałem.

**Tydzień 10: Multi-Asset Portfolio Construction**
*   **Dzień 64:** (1) Budowa dynamicznej macierzy korelacji dla 10+ aktywów, (2) Implementacja alertów o zbyt wysokiej korelacji w portfelu, (3) Wizualizacja korelacji w formie mapy cieplnej.
*   **Dzień 65:** (1) Implementacja "Equal Risk Contribution" (ERC), (2) Kodowanie procesu wyrównywania wkładu do ryzyka (zmienność $\times$ waga), (3) Testy na portfelu mieszanym (S&P500, BTC, Gold).
*   **Dzień 66:** (1) Implementacja "Inverse Volatility Weighting", (2) Automatyzacja przydziału kapitału: stabilne aktywa $\rightarrow$ więcej kapitału, (3) Analiza stabilności Equity Curve portfela.
*   **Dzień 67:** (1) Budowa "Multi-Strategy Portfolio" (Sygnał A na BTC, Sygnał B na AAPL), (2) Implementacja wspólnego konta kapitałowego dla wszystkich strategii, (3) Testowanie interakcji między strategiami.
*   **Dzień 68:** (1) Obliczanie "Portfolio Sharpe Ratio", (2) Analiza "Contribution to Return" (która strategia/aktywo zarabia najwięcej?), (3) Analiza "Contribution to Risk".
*   **Dzień 69:** (1) Implementacja harmonogramu rebalansingu (np. każdy poniedziałek), (2) Kodowanie funkcji `rebalance_portfolio()`, (3) Testowanie wpływu częstotliwości rebalansingu na zysk.
*   **Dzień 70:** **CHECKPOINT:** (1) Analiza kosztów transakcyjnych przy rebalansingu, (2) Optymalizacja kosztów (rebalansuj tylko przy odchyleniu > X%), (3) Finalizacja modułu `portfolio_manager`.

**Tydzień 11: Automation Pipeline (The Robot)**
*   **Dzień 71:** (1) Budowa modułu `data_pipeline()` (automatyczne pobieranie danych z yfinance/API), (2) Implementacja obsługi błędów połączenia (retries), (3) Zapisywanie danych do lokalnej bazy/plików Parquet.
*   **Dzień 72:** (1) Implementacja "Daily Signal Generator" (skrypt uruchamiany raz dziennie), (2) Budowa pętli przechodzącej przez wszystkie aktywa i strategie, (3) Zapisywanie sygnałów do `daily_signals.csv`.
*   **Dzień 73:** (1) Implementacja "Signal Logger" z wersjonowaniem (kiedy sygnał powstał, jaka była wersja parametrów), (2) Budowa systemu logowania zdarzeń (INFO, WARNING, ERROR), (3) Testowanie stabilności skryptu przy braku danych.
*   **Dzień 74:** (1) Integracja całego łańcucha: `Data` $\rightarrow$ `Features` $\rightarrow$ `Signals` $\rightarrow$ `Risk` $\rightarrow$ `Position`, (2) Budowa głównego pliku `main.py`, (3) Testy "End-to-End" na danych historycznych.
*   **Dzień 75:** (1) Implementacja prostych powiadomień (np. print z podsumowaniem: "Today: 2 BUY, 1 SELL"), (2) Budowa funkcji `generate_daily_report()`, (3) Testowanie powiadomień na danych Live.
*   **Dzień 76:** (1) Budowa "Live Performance Tracker" (obliczanie PnL na podstawie rzeczywistych cen zamknięcia), (2) Implementacja śledzenia "Slippage" w rzeczywistym czasie, (3) Porównanie Live PnL vs Backtest PnL.
*   **Dzień 77:** **CHECKPOINT:** (1) Testy "Stress-test" automatyzacji (uruchomienie 10 razy pod rząd), (2) Naprawa błędów w pipeline, (3) Optymalizacja czasu wykonania skryptu.

**Tydzień 12: Final Integration & Audit**
*   **Dzień 78:** (1) Budowa finalnego generatora raportów PDF/HTML, (2) Dodanie wykresów Equity, Drawdown i Tabeli Trade'ów, (3) Automatyzacja wysyłki/zapisu raportu.
*   **Dzień 79:** (1) "Black Swan Stress Test" (symulacja spadku o 30% w jeden dzień), (2) Sprawdzenie, czy `risk_manager` uratuje kapitał, (3) Korekta limitów ryzyka.
*   **Dzień 80:** (1) Finalny audyt "Anti-Bias": ponowna weryfikacja wszystkich `shift(1)` i okien danych, (2) Szukanie wycieków danych w całym systemie, (3) Raport z audytu.
*   **Dzień 81:** (1) Optymalizacja wydajności: zamiana pętli `for` na operacje wektoryzowane w Pandas, (2) Profilowanie kodu (szukanie wąskich gardeł), (3) Optymalizacja zapisu danych.
*   **Dzień 82:** (1) Dokumentacja techniczna: "Jak dodać nową Alfę do systemu?", (2) Opis architektury systemu, (3) Instrukcja uruchamiania pipeline'u.
*   **Dzień 83:** (1) Start "Paper Trading" (testy na żywo bez pieniędzy), (2) Codzienne monitorowanie sygnałów, (3) Ręczna weryfikacja poprawności sygnałów.
*   **Dzień 84:** **FINAL CHECKPOINT:** (1) Podsumowanie całego projektu, (2) Prezentacja: "Mini Quant Fund v1.0", (3) Plan rozwoju na przyszłość (np. Machine Learning).

**Dni 85-90: Buffer & Polish**
*   Dni 85-90: Czas na nieprzewidziane błędy, dopracowanie wizualizacji, naukę nowych bibliotek lub powtórzenie etapów, które okazały się najtrudniejsze.