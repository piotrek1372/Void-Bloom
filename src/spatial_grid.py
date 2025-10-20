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
        self.clear()

    def clear(self):
        """Czyści siatkę."""
        self.grid = {}
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                self.grid[(x, y)] = []

    def add_object(self, obj):
        """
        Dodaje obiekt do siatki.

        Args:
            obj: Obiekt z atrybutem rect (pygame.Rect)
        """
        cell_x = int(obj.rect.centerx // self.cell_size)
        cell_y = int(obj.rect.centery // self.cell_size)
        
        # Upewnij się, że komórka jest w granicach
        cell_x = max(0, min(cell_x, self.grid_width - 1))
        cell_y = max(0, min(cell_y, self.grid_height - 1))
        
        self.grid[(cell_x, cell_y)].append(obj)

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

