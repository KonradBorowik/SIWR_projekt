# SIWR_projekt

W visualizer.py wczytywane są zdjęcia i towrzona jest lista z obiektami klasy Image. W image.py znajduje się klasa Image, a w niej metody wykorzystujące informacje zawarte na zdjęciach.
Do porównania bboxów wykorzystuję porównanie histogramów zwężonych górnych połówek bboxów. Porównuję histogramy każdego bboxa z aktualnego zdjęcia z każdym histogramem bboxa z poprzedniego zdjęcia. To ma miejsce w histograms.py.
Kolejnym krokiem jest utworzenie funkcji f_b dla połączeń w grafie pomiędzy obiektami (f_b ogranicza możliwość wystąpienia sytuacji, w której dwa obiekty zostaną sklasyfikowane jako ten sam obiekt z poprzedniego zdjęcia) oraz f_u, w których zawarte są wartości podobieństw danego obiektu, do któregoś z obiektów z poprzedniego zdjęcia.
Te macierze podawane są do create_graph(), w którym tworzę graf. Najpierw tworzę połączenia obiekt->f_u, później obiekt->f_b->obiekt. Ostatecznie wyniki otrzymuję po utworzeniu BeliefPropagation na podstawie utworzonego grafu.

![graf (3)](https://user-images.githubusercontent.com/28296861/189764953-52854e38-e92e-4f3f-b0e9-aa551f685113.jpg)
