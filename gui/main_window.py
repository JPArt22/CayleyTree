"""
Ventana principal de la aplicación.
Gestiona la navegación entre vistas y el menú principal.
"""

import customtkinter as ctk
from gui.tree_view import TreeView
from gui.function_view import FunctionView
from gui.crypto_view import CryptoView


class MainWindow(ctk.CTk):
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("Proyecto MD II - CayleyTree")
        self.geometry("1600x900")
        
        # Maximizar ventana al iniciar
        self.state('zoomed')
        
        # Tema oscuro
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Color de fondo
        self.configure(fg_color="#11111b")
        
        # Centrar ventana
        self._center_window()
        
        # Vistas
        self.current_view = None
        self.menu_view = None
        self.tree_view = None
        self.function_view = None
        self.crypto_view = None
        self.n_vertices = 9  # Valor por defecto
        
        # Mostrar menú
        self._show_menu()
    
    def _center_window(self):
        """Centra la ventana en la pantalla."""
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')
    
    def _clear_view(self):
        """Limpia la vista actual."""
        if self.current_view:
            self.current_view.pack_forget()
            self.current_view = None
    
    def _show_menu(self):
        """Muestra el menú principal."""
        self._clear_view()
        
        if self.menu_view is None:
            self.menu_view = self._create_menu()
        
        self.current_view = self.menu_view
        self.current_view.pack(fill="both", expand=True)
    
    def _create_menu(self):
        """Crea el menú principal."""
        menu = ctk.CTkFrame(self, fg_color="#11111b")
        
        # Container central
        center = ctk.CTkFrame(menu, fg_color="transparent")
        center.place(relx=0.5, rely=0.5, anchor="center")
        
        # Logo / Título
        title_frame = ctk.CTkFrame(center, fg_color="#1e1e2e", corner_radius=15)
        title_frame.pack(pady=(0, 40), padx=40)
        
        title = ctk.CTkLabel(
            title_frame,
            text="Proyecto MD I",
            font=("Segoe UI", 48, "bold"),
            text_color="#cdd6f4"
        )
        title.pack(pady=(30, 10), padx=60)
        
        subtitle = ctk.CTkLabel(
            title_frame,
            text="Demostración de Joyal a la Fórmula de Cayley",
            font=("Segoe UI", 18),
            text_color="#a6adc8"
        )
        subtitle.pack(pady=(0, 30), padx=40)
        
        # Descripción
        desc = ctk.CTkLabel(
            center,
            text="Herramienta interactiva para explorar la relación entre árboles\ny funciones mediante la demostración de André Joyal",
            font=("Segoe UI", 13),
            text_color="#7f849c",
            justify="center"
        )
        desc.pack(pady=(0, 30))
        
        # Selector de número de vértices
        n_frame = ctk.CTkFrame(center, fg_color="#1e1e2e", corner_radius=10)
        n_frame.pack(pady=(0, 30))
        
        n_label = ctk.CTkLabel(
            n_frame,
            text="Número de vértices (n):",
            font=("Segoe UI", 14, "bold"),
            text_color="#cdd6f4"
        )
        n_label.pack(side="left", padx=(20, 10), pady=15)
        
        self.n_slider = ctk.CTkSlider(
            n_frame,
            from_=3,
            to=35,
            number_of_steps=32,
            width=200,
            command=self._on_n_changed
        )
        self.n_slider.set(9)
        self.n_slider.pack(side="left", padx=10, pady=15)
        
        self.n_value_label = ctk.CTkLabel(
            n_frame,
            text="9",
            font=("Segoe UI", 16, "bold"),
            text_color="#89b4fa",
            width=40
        )
        self.n_value_label.pack(side="left", padx=(10, 20), pady=15)
        
        n_info = ctk.CTkLabel(
            center,
            text=f"T(9) = 9⁷ = {9**7:,} árboles distintos",
            font=("Segoe UI", 11, "italic"),
            text_color="#7f849c"
        )
        n_info.pack(pady=(0, 20))
        self.n_info_label = n_info
        
        # Botones
        btn_frame = ctk.CTkFrame(center, fg_color="transparent")
        btn_frame.pack()
        
        btn_tree = ctk.CTkButton(
            btn_frame,
            text="Construir Función desde Árbol",
            width=350,
            height=60,
            font=("Segoe UI", 16, "bold"),
            fg_color="#89b4fa",
            hover_color="#b4befe",
            text_color="#1e1e2e",
            corner_radius=12,
            command=self._show_tree_view
        )
        btn_tree.pack(pady=10)
        
        btn_function = ctk.CTkButton(
            btn_frame,
            text="Construir Árbol desde Función",
            width=350,
            height=60,
            font=("Segoe UI", 16, "bold"),
            fg_color="#a6e3a1",
            hover_color="#94e2d5",
            text_color="#1e1e2e",
            corner_radius=12,
            command=self._show_function_view
        )
        btn_function.pack(pady=10)
        
        # NUEVO: Botón de Encriptación/Desencriptación
        btn_crypto = ctk.CTkButton(
            btn_frame,
            text="🔐 Encriptar/Desencriptar Texto",
            width=350,
            height=60,
            font=("Segoe UI", 16, "bold"),
            fg_color="#f9e2af",
            hover_color="#f5c2e7",
            text_color="#1e1e2e",
            corner_radius=12,
            command=self._show_crypto_view
        )
        btn_crypto.pack(pady=10)
        
        # Footer
        footer = ctk.CTkLabel(
            center,
            text="Matemáticas Discretas II • Universidad Nacional de Colombia\nAgradecimiento al profesor Arles Ernesto Rodriguez Portela\nJulio de 2026",
            font=("Segoe UI", 11),
            text_color="#585b70"
        )
        footer.pack(pady=(40, 0))
        
        return menu
    
    def _on_n_changed(self, value):
        """Callback cuando cambia el valor de n."""
        n = int(value)
        self.n_vertices = n
        self.n_value_label.configure(text=str(n))
        
        # Actualizar información de Cayley
        if n <= 15:  # Evitar números muy grandes
            cayley_result = n ** (n - 2)
            self.n_info_label.configure(text=f"T({n}) = {n}^{n-2} = {cayley_result:,} árboles distintos")
        else:
            self.n_info_label.configure(text=f"T({n}) = {n}^{n-2} árboles distintos")
    
    def _show_tree_view(self):
        """Muestra la vista de construcción desde árbol."""
        self._clear_view()
        
        # Recrear siempre la vista con el n actual
        self.tree_view = TreeView(self, n=self.n_vertices, on_back=self._show_menu)
        
        self.current_view = self.tree_view
        self.current_view.pack(fill="both", expand=True)
    
    def _show_function_view(self):
        """Muestra la vista de función."""
        self._clear_view()
        
        # Recrear siempre la vista con el n actual
        self.function_view = FunctionView(self, n=self.n_vertices, on_back=self._show_menu)
        
        self.current_view = self.function_view
        self.current_view.pack(fill="both", expand=True)
    
    def _show_crypto_view(self):
        """Muestra la vista de encriptación/desencriptación."""
        self._clear_view()
        
        # Recrear siempre la vista con el n actual
        self.crypto_view = CryptoView(self, n=self.n_vertices, on_back=self._show_menu)
        
        self.current_view = self.crypto_view
        self.current_view.pack(fill="both", expand=True)
    
    def run(self):
        """Inicia el loop de la aplicación."""
        self.mainloop()


def start_application():
    """Función de entrada para iniciar la aplicación."""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    start_application()
