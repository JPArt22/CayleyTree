"""
Vista para encriptación y desencriptación directa.
Permite usar funciones para cifrar/descifrar textos sin construir árboles.
"""

import customtkinter as ctk
from logic import CryptoEngine
from gui.function_view import generate_random_function


class CryptoView(ctk.CTkFrame):
    """Vista para encriptación/desencriptación directa."""
    
    def __init__(self, parent, n=9, on_back=None):
        super().__init__(parent, fg_color="#11111b")
        
        self.n = n
        self.crypto_engine = CryptoEngine(n)
        self.on_back = on_back
        self.funcion = [None] * n
        self.result_text = ""
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Configura la interfaz de usuario."""
        # Header
        header = ctk.CTkFrame(self, fg_color="#1e1e2e", height=60)
        header.pack(fill="x", padx=20, pady=(20, 10))
        
        btn_back = ctk.CTkButton(
            header,
            text="← Volver",
            width=100,
            height=35,
            fg_color="#313244",
            hover_color="#45475a",
            font=("Segoe UI", 13),
            command=self._on_back_clicked
        )
        btn_back.pack(side="left", padx=10, pady=10)
        
        title = ctk.CTkLabel(
            header,
            text="Encriptación y Desencriptación",
            font=("Segoe UI", 22, "bold"),
            text_color="#cdd6f4"
        )
        title.pack(side="left", padx=20)
        
        # Contenedor principal con scroll
        main = ctk.CTkScrollableFrame(self, fg_color="#11111b")
        main.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Panel central
        center = ctk.CTkFrame(main, fg_color="#1e1e2e")
        center.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Instrucciones
        instr_frame = ctk.CTkFrame(center, fg_color="#313244")
        instr_frame.pack(padx=30, pady=(20, 10), fill="x")
        
        lbl_instr = ctk.CTkLabel(
            instr_frame,
            text=f"INSTRUCCIONES\n\n"
                 f"1. Ingrese una función f(1)...f({self.n}) separada por comas\n"
                 f"2. La función se usará como clave de encriptación\n"
                 f"3. Escriba el texto que desea encriptar o desencriptar\n"
                 f"4. Use los botones correspondientes para procesar\n\n"
                 f"Alfabeto: A-Z, Ñ, espacio, coma, punto (30 caracteres)",
            font=("Segoe UI", 12),
            text_color="#a6adc8",
            justify="left"
        )
        lbl_instr.pack(pady=15, padx=15)
        
        # Función
        func_frame = ctk.CTkFrame(center, fg_color="#313244")
        func_frame.pack(padx=30, pady=10, fill="x")
        
        lbl_func = ctk.CTkLabel(
            func_frame,
            text="Función (clave de cifrado):",
            font=("Segoe UI", 14, "bold"),
            text_color="#cdd6f4"
        )
        lbl_func.pack(pady=(15, 5), padx=15, anchor="w")
        
        self.entry_funcion = ctk.CTkEntry(
            func_frame,
            placeholder_text=f"Ejemplo: {','.join(map(str, range(1, min(self.n+1, 10))))}",
            height=40,
            font=("Segoe UI", 13)
        )
        self.entry_funcion.pack(padx=15, pady=(0, 10), fill="x")
        
        btn_set_func = ctk.CTkButton(
            func_frame,
            text="Establecer Función como Clave",
            fg_color="#89b4fa",
            hover_color="#b4befe",
            text_color="#1e1e2e",
            font=("Segoe UI", 13, "bold"),
            height=40,
            command=self._set_function
        )
        btn_set_func.pack(padx=15, pady=(0, 15))

        btn_random = ctk.CTkButton(
            func_frame,
            text="🎲 Generar Función Aleatoria",
            fg_color="#89b4fa",
            hover_color="#b4befe",
            text_color="#1e1e2e",
            font=("Segoe UI", 13, "bold"),
            height=40,
            command=self._generar_funcion_aleatoria
        )
        btn_random.pack(padx=15, pady=(0, 15), fill="x")
        
        self.lbl_func_status = ctk.CTkLabel(
            func_frame,
            text="",
            font=("Segoe UI", 11),
            text_color="#f38ba8"
        )
        self.lbl_func_status.pack(pady=(0, 10))
        
        # Texto
        text_frame = ctk.CTkFrame(center, fg_color="#313244")
        text_frame.pack(padx=30, pady=10, fill="x")
        
        lbl_text = ctk.CTkLabel(
            text_frame,
            text="Texto a encriptar/desencriptar:",
            font=("Segoe UI", 14, "bold"),
            text_color="#cdd6f4"
        )
        lbl_text.pack(pady=(15, 5), padx=15, anchor="w")
        
        self.entry_text = ctk.CTkTextbox(
            text_frame,
            height=120,
            font=("Segoe UI", 13),
            wrap="word"
        )
        self.entry_text.pack(padx=15, pady=(0, 10), fill="x")
        
        # Botones de acción
        btn_frame = ctk.CTkFrame(text_frame, fg_color="transparent")
        btn_frame.pack(pady=10)
        
        btn_encrypt = ctk.CTkButton(
            btn_frame,
            text="🔒 Encriptar",
            fg_color="#a6e3a1",
            hover_color="#94e2d5",
            text_color="#1e1e2e",
            font=("Segoe UI", 13, "bold"),
            width=200,
            height=45,
            command=self._encrypt
        )
        btn_encrypt.pack(side="left", padx=10)
        
        btn_decrypt = ctk.CTkButton(
            btn_frame,
            text="🔓 Desencriptar",
            fg_color="#cba6f7",
            hover_color="#b4befe",
            text_color="#1e1e2e",
            font=("Segoe UI", 13, "bold"),
            width=200,
            height=45,
            command=self._decrypt
        )
        btn_decrypt.pack(side="left", padx=10)
        
        btn_clear = ctk.CTkButton(
            btn_frame,
            text="Limpiar",
            fg_color="#585b70",
            hover_color="#6c7086",
            text_color="#cdd6f4",
            font=("Segoe UI", 13, "bold"),
            width=150,
            height=45,
            command=self._clear
        )
        btn_clear.pack(side="left", padx=10)
        
        # Resultado
        result_frame = ctk.CTkFrame(center, fg_color="#313244")
        result_frame.pack(padx=30, pady=(10, 20), fill="x")
        
        lbl_result = ctk.CTkLabel(
            result_frame,
            text="Resultado:",
            font=("Segoe UI", 14, "bold"),
            text_color="#cdd6f4"
        )
        lbl_result.pack(pady=(15, 5), padx=15, anchor="w")
        
        self.lbl_resultado = ctk.CTkLabel(
            result_frame,
            text="El resultado aparecerá aquí",
            font=("Segoe UI", 13),
            text_color="#a6adc8",
            justify="left",
            anchor="w"
        )
        self.lbl_resultado.pack(pady=(0, 15), padx=15, fill="x")

        btn_copy = ctk.CTkButton(
            result_frame,
            text="Copiar Resultado",
            fg_color="#f9e2af",
            hover_color="#f5c2e7",
            text_color="#1e1e2e",
            font=("Segoe UI", 13, "bold"),
            height=40,
            command=self._copy_result
        )
        btn_copy.pack(padx=15, pady=(0, 15), fill="x")
    
    def _set_function(self):
        """Establece la función como clave de cifrado."""
        texto = self.entry_funcion.get().strip()
        
        if not texto:
            self.lbl_func_status.configure(
                text="⚠ Por favor ingrese una función",
                text_color="#f38ba8"
            )
            return
        
        try:
            valores = [int(x.strip()) for x in texto.split(',')]
            
            if len(valores) != self.n:
                self.lbl_func_status.configure(
                    text=f"⚠ Debe ingresar exactamente {self.n} valores",
                    text_color="#f38ba8"
                )
                return
            
            if not all(1 <= x <= self.n for x in valores):
                self.lbl_func_status.configure(
                    text=f"⚠ Los valores deben estar entre 1 y {self.n}",
                    text_color="#f38ba8"
                )
                return
            
            # Convertir a índices 0-(n-1)
            self.funcion = [v - 1 for v in valores]
            
            # Configurar clave
            self.crypto_engine.set_key_from_function(self.funcion)
            
            self.lbl_func_status.configure(
                text="✓ Función establecida correctamente como clave de cifrado",
                text_color="#a6e3a1"
            )
            
        except ValueError:
            self.lbl_func_status.configure(
                text=f"⚠ Formato inválido. Use números del 1 al {self.n} separados por comas",
                text_color="#f38ba8"
            )
    
    def _encrypt(self):
        """Encripta el texto."""
        self.result_text = ""
        if None in self.funcion:
            self.lbl_resultado.configure(
                text="⚠ Primero debe establecer una función como clave",
                text_color="#f38ba8"
            )
            return
        
        texto = self.entry_text.get("1.0", "end-1c").strip()
        
        if not texto:
            self.lbl_resultado.configure(
                text="⚠ Por favor ingrese un texto para encriptar",
                text_color="#f38ba8"
            )
            return
        
        try:
            resultado = self.crypto_engine.encrypt(texto)
            self.result_text = resultado
            self.lbl_resultado.configure(
                text=f"✓ Texto encriptado:\n\n{resultado}",
                text_color="#a6e3a1"
            )
        except Exception as e:
            self.lbl_resultado.configure(
                text=f"⚠ Error al encriptar: {str(e)}",
                text_color="#f38ba8"
            )
    
    def _decrypt(self):
        """Desencripta el texto."""
        self.result_text = ""
        if None in self.funcion:
            self.lbl_resultado.configure(
                text="⚠ Primero debe establecer una función como clave",
                text_color="#f38ba8"
            )
            return
        
        texto = self.entry_text.get("1.0", "end-1c").strip()
        
        if not texto:
            self.lbl_resultado.configure(
                text="⚠ Por favor ingrese un texto para desencriptar",
                text_color="#f38ba8"
            )
            return
        
        try:
            resultado = self.crypto_engine.decrypt(texto)
            self.result_text = resultado
            self.lbl_resultado.configure(
                text=f"✓ Texto desencriptado:\n\n{resultado}",
                text_color="#a6e3a1"
            )
        except Exception as e:
            self.lbl_resultado.configure(
                text=f"⚠ Error al desencriptar: {str(e)}",
                text_color="#f38ba8"
            )
    
    def _clear(self):
        """Limpia los campos."""
        self.entry_text.delete("1.0", "end")
        self.result_text = ""
        self.lbl_resultado.configure(
            text="El resultado aparecerá aquí",
            text_color="#a6adc8"
        )

    def _generar_funcion_aleatoria(self):
        """Genera una función aleatoria y la establece como clave."""
        funcion_aleatoria = generate_random_function(self.n)
        self.entry_funcion.delete(0, "end")
        self.entry_funcion.insert(0, ",".join(map(str, funcion_aleatoria)))
        self._set_function()

    def _copy_result(self):
        """Copia el resultado actual al portapapeles."""
        if not self.result_text:
            self.lbl_resultado.configure(
                text="⚠ No hay un resultado para copiar",
                text_color="#f38ba8"
            )
            return

        self.clipboard_clear()
        self.clipboard_append(self.result_text)
        self.update_idletasks()
        self.lbl_resultado.configure(
            text="✓ Resultado copiado al portapapeles",
            text_color="#a6e3a1"
        )
    
    def _on_back_clicked(self):
        """Maneja el botón de volver."""
        if self.on_back:
            self.on_back()
