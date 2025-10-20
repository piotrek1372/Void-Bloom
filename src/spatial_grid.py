"""
Spatial Grid - system optymalizacji kolizji.
Dzieli ekran na siatką komórek do szybszego wyszukiwania kolizji.
"""


class SpatialGrid:
    """
    Siatka przestrzenna do optymalizacji kolizji.
    Dzieli ekran na komórki i przechowuje obiekty w odpowiednich komórkach.
    """

    def __init__(self, screen_width, screen_height, cell_size=100):
        """
        Inicjalizuje SpatialGrid.

        Args:
            screen_width: Szerokość ekranu
            screen_height: Wysokość ekranu
            cell_size: Rozmiar komórki siatki (domyślnie 100)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.cell_size = cell_size

        # Oblicz wymiary siatki
        self.grid_width = (screen_width // cell_size) + 1
        self.grid_height = (screen_height // cell_size) + 1

        # Inicjalizuj siatkę
        self.grid = {}

        # Śledzenie pozycji obiektów dla optymalizacji
        # Słownik: id(obj) -> (cell_x, cell_y)
        self.object_positions = {}

        self.clear()

    def clear(self):
        """Czyści siatkę i śledzenie pozycji."""
        self.grid = {}
        self.object_positions = {}
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.grid[(x, y)] = []

    def _get_cell_coords(self, obj):
        """
        Oblicza współrzędne komórki dla obiektu.

        Args:
            obj: Obiekt z atrybutem rect

        Returns:
            Krotka (cell_x, cell_y)
        """
        cell_x = int(obj.rect.centerx // self.cell_size)
        cell_y = int(obj.rect.centery // self.cell_size)

        # Upewnij się, że komórka jest w granicach
        cell_x = max(0, min(cell_x, self.grid_width - 1))
        cell_y = max(0, min(cell_y, self.grid_height - 1))

        return (cell_x, cell_y)

    def add_object(self, obj):
        """
        Dodaje obiekt do siatki.

        Args:
            obj: Obiekt z atrybutem rect (pygame.Rect)
        """
        cell_coords = self._get_cell_coords(obj)
        obj_id = id(obj)

        self.grid[cell_coords].append(obj)
        self.object_positions[obj_id] = cell_coords

    def update_object(self, obj):
        """
        Aktualizuje pozycję obiektu w siatce.
        Jeśli obiekt przesunął się do innej komórki, przesuwa go.
        Jeśli pozostał w tej samej komórce, nic nie robi (optymalizacja).

        Args:
            obj: Obiekt z atrybutem rect (pygame.Rect)
        """
        obj_id = id(obj)
        new_cell_coords = self._get_cell_coords(obj)
        old_cell_coords = self.object_positions.get(obj_id)

        # Jeśli obiekt nie zmienił komórki, nic nie rób
        if old_cell_coords == new_cell_coords:
            return

        # Usuń obiekt ze starej komórki
        if old_cell_coords is not None and old_cell_coords in self.grid:
            try:
                self.grid[old_cell_coords].remove(obj)
            except ValueError:
                pass  # Obiekt nie był w starej komórce

        # Dodaj obiekt do nowej komórki
        self.grid[new_cell_coords].append(obj)
        self.object_positions[obj_id] = new_cell_coords

    def remove_object(self, obj):
        """
        Usuwa obiekt z siatki.

        Args:
            obj: Obiekt do usunięcia
        """
        obj_id = id(obj)
        cell_coords = self.object_positions.get(obj_id)

        if cell_coords is not None and cell_coords in self.grid:
            try:
                self.grid[cell_coords].remove(obj)
            except ValueError:
                pass  # Obiekt nie był w komórce

        # Usuń z śledzenia pozycji
        if obj_id in self.object_positions:
            del self.object_positions[obj_id]

    def get_nearby_objects(self, obj, radius=1):
        """
        Zwraca obiekty w pobliżu danego obiektu.

        Args:
            obj: Obiekt referencyjny
            radius: Promień wyszukiwania w komórkach (domyślnie 1)

        Returns:
            Lista pobliskich obiektów
        """
        cell_x = int(obj.rect.centerx // self.cell_size)
        cell_y = int(obj.rect.centery // self.cell_size)
        
        nearby = []
        
        # Sprawdź komórki w promieniu
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                check_x = cell_x + dx
                check_y = cell_y + dy
                
                # Sprawdź granice
                if 0 <= check_x < self.grid_width and 0 <= check_y < self.grid_height:
                    nearby.extend(self.grid[(check_x, check_y)])
        
        return nearby

    def get_objects_in_cell(self, cell_x, cell_y):
        """
        Zwraca obiekty w danej komórce.

        Args:
            cell_x: Współrzędna X komórki
            cell_y: Współrzędna Y komórki

        Returns:
            Lista obiektów w komórce
        """
        if 0 <= cell_x < self.grid_width and 0 <= cell_y < self.grid_height:
            return self.grid[(cell_x, cell_y)]
        return []

    def rebuild(self, objects):
        """
        Przebudowuje siatkę z nową listą obiektów.

        Args:
            objects: Lista wszystkich obiektów
        """
        self.clear()
        for obj in objects:
            self.add_object(obj)

