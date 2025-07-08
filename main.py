import tkinter
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random
from typing import List, Tuple

from quadtree import Ponto, Circulo, Retangulo, QuadTree

# Define a aparência padrão da aplicação
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    """
    Classe principal da aplicação que gerencia a interface gráfica e o estado da simulação.
    """
    def __init__(self) -> None:
        super().__init__()
        self.title("Simulador de Cobertura Quadtree")
        self.geometry("1100x720")

        self._carregar_dados_fixos()
        self._inicializar_estado_simulacao()

        # Configura o layout principal da janela
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_sidebar()
        self._criar_area_principal()

        # Conecta o evento de clique do mouse no canvas à nossa função de callback
        self.canvas.mpl_connect('button_press_event', self._on_map_click)

        # Inicia a primeira simulação
        self._rodar_nova_simulacao()

    def _carregar_dados_fixos(self) -> None:
        """Carrega recursos que não mudam, como a imagem de fundo e as construções."""
        self.construcoes = [
            Retangulo(29, 148, 10, 8), Retangulo(77, 137, 30, 17),
            Retangulo(152, 137, 30, 17), Retangulo(145, 62, 23, 12),
            Retangulo(113, 4, 72, 4)
        ]
        try:
            self.imagem_fundo = plt.imread('mapa_exemplo.png')
        except FileNotFoundError:
            self.imagem_fundo = None

    def _inicializar_estado_simulacao(self) -> None:
        """Inicializa as variáveis que guardarão o estado atual da simulação."""
        self.cameras: List[Circulo] = []
        self.pontos_aleatorios: List[Ponto] = []
        self.pontos_manuais: List[Ponto] = []
        
        # Variáveis de controle para os modos de edição da interface
        self.modo_adicao_ponto = tkinter.BooleanVar(value=False)
        self.modo_adicao_camera = tkinter.BooleanVar(value=False)
        self.raio_camera_var = tkinter.IntVar(value=25)

    def _criar_sidebar(self) -> None:
        """Cria e posiciona todos os widgets da barra de controle lateral."""
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)

        ctk.CTkLabel(self.sidebar_frame, text="Controles", font=ctk.CTkFont(size=20, weight="bold")).grid(row=0, column=0, padx=20, pady=(20, 10))
        ctk.CTkButton(self.sidebar_frame, text="Nova Simulação Aleatória", command=self._rodar_nova_simulacao).grid(row=1, column=0, padx=20, pady=10)
        
        ctk.CTkLabel(self.sidebar_frame, text="Modo de Edição Manual:", anchor="w").grid(row=2, column=0, padx=20, pady=(10, 0))
        ctk.CTkSwitch(self.sidebar_frame, text="Adicionar Ponto", variable=self.modo_adicao_ponto, command=self._toggle_modo_ponto).grid(row=3, column=0, padx=20, pady=10, sticky="w")
        ctk.CTkSwitch(self.sidebar_frame, text="Adicionar Câmera", variable=self.modo_adicao_camera, command=self._toggle_modo_camera).grid(row=4, column=0, padx=20, pady=10, sticky="w")
        
        ctk.CTkLabel(self.sidebar_frame, text="Raio da Câmera Manual:", anchor="w").grid(row=5, column=0, padx=20, pady=(10,0))
        
        ctk.CTkSlider(self.sidebar_frame, from_=0, to=25, number_of_steps=25, variable=self.raio_camera_var, command=self._atualizar_label_raio).grid(row=6, column=0, padx=20, pady=(0,0), sticky="ew")
        
        self.label_valor_raio = ctk.CTkLabel(self.sidebar_frame, text="")
        self.label_valor_raio.grid(row=7, column=0, padx=20, pady=(0,10))
        self._atualizar_label_raio(self.raio_camera_var.get())

        ctk.CTkButton(self.sidebar_frame, text="Limpar Tudo", fg_color="#D2042D", hover_color="#AA0000", command=self._limpar_tudo).grid(row=8, column=0, padx=20, pady=10)
        ctk.CTkButton(self.sidebar_frame, text="Sair", fg_color="transparent", border_width=2, command=self.quit).grid(row=9, column=0, padx=20, pady=20, sticky="s")

    def _criar_area_principal(self) -> None:
        """Cria o container para o gráfico e o canvas do Matplotlib."""
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.bind("<Configure>", self._on_resize) # Mantém a proporção do gráfico
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.main_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
    
    # --- Métodos de Lógica e Eventos ---

    def _on_resize(self, event: tkinter.Event) -> None:
        """Mantém o gráfico quadrado e centralizado ao redimensionar a janela."""
        new_size = min(event.width, event.height)
        pad_x = (event.width - new_size) / 2
        pad_y = (event.height - new_size) / 2
        self.canvas_widget.place(x=pad_x, y=pad_y, width=new_size, height=new_size)

    def _toggle_modo_ponto(self) -> None:
        """Garante que apenas um modo de adição esteja ativo por vez."""
        if self.modo_adicao_ponto.get():
            self.modo_adicao_camera.set(False)

    def _toggle_modo_camera(self) -> None:
        """Garante que apenas um modo de adição esteja ativo por vez."""
        if self.modo_adicao_camera.get():
            self.modo_adicao_ponto.set(False)
            
    def _atualizar_label_raio(self, valor: float) -> None:
        """Atualiza o texto do label do raio conforme o slider é movido."""
        raio = int(valor)
        text = "Raio: Aleatório (10-25)" if raio == 0 else f"Raio: {raio}"
        self.label_valor_raio.configure(text=text)
    
    def _on_map_click(self, event) -> None:
        """Callback para cliques do mouse no mapa."""
        if event.inaxes != self.ax or event.xdata is None:
            return

        x, y = event.xdata, event.ydata
        if self.modo_adicao_ponto.get():
            self.pontos_manuais.append(Ponto(x, y))
            self._atualizar_plot()
        elif self.modo_adicao_camera.get():
            self._adicionar_camera_manual(Ponto(x, y))

    # --- Métodos de Controle da Simulação ---

    def _rodar_nova_simulacao(self) -> None:
        """Inicia uma simulação com novas câmeras e pontos aleatórios."""
        self.cameras = self._gerar_cameras_aleatorias()
        self.pontos_aleatorios = [Ponto(random.randint(0, 200), random.randint(0, 200)) for _ in range(7)]
        self.pontos_manuais.clear()
        self._atualizar_plot()
        
    def _limpar_tudo(self) -> None:
        """Limpa todas as câmeras e pontos, resetando o cenário."""
        self.cameras.clear()
        self.pontos_aleatorios.clear()
        self.pontos_manuais.clear()
        self._atualizar_plot()

    def _gerar_cameras_aleatorias(self, quantidade: int = 5) -> List[Circulo]:
        """Gera uma lista de câmeras em posições válidas."""
        cameras_geradas = []
        for _ in range(quantidade):
            raio = random.randint(10, 25)
            while True:
                ponto_central = Ponto(random.randint(raio, 200 - raio), random.randint(raio, 200 - raio))
                if not any(c.contem_ponto(ponto_central) for c in self.construcoes):
                    cameras_geradas.append(Circulo(ponto_central.x, ponto_central.y, raio))
                    break
        return cameras_geradas

    def _adicionar_camera_manual(self, centro: Ponto) -> None:
        """Adiciona uma câmera manual no local clicado, se for válido."""
        valor_raio = self.raio_camera_var.get()
        raio = random.randint(10, 25) if valor_raio == 0 else valor_raio
        
        # Validação da posição da câmera
        em_predio = any(c.contem_ponto(centro) for c in self.construcoes)
        fora_da_borda = not (raio <= centro.x <= 200 - raio and raio <= centro.y <= 200 - raio)
        
        if not em_predio and not fora_da_borda:
            self.cameras.append(Circulo(centro.x, centro.y, raio))
            self._atualizar_plot()

    # --- Métodos de Desenho e Lógica Final ---

    def _atualizar_plot(self) -> None:
        """Função central que redesenha o estado atual da simulação no canvas."""
        self.ax.clear()
        
        arvore_quad = QuadTree(Retangulo(100, 100, 100, 100), profundidade_maxima=7)
        if self.cameras or self.construcoes:
            arvore_quad.refinar(self.cameras + self.construcoes)
        
        todos_os_pontos = self.pontos_aleatorios + self.pontos_manuais
        cobertos, bloqueados, descobertos = self._classificar_pontos(todos_os_pontos, self.cameras)
        
        self._desenhar_elementos_base()
        self._desenhar_elementos_simulacao(arvore_quad.obter_nos_folha(), self.cameras, cobertos, bloqueados, descobertos)
        
        self.canvas.draw()

    def _classificar_pontos(self, pontos: List[Ponto], cameras: List[Circulo]) -> Tuple[List, List, List]:
        """Separa uma lista de pontos em três categorias: coberto, bloqueado ou descoberto."""
        cobertos, bloqueados, descobertos = [], [], []
        for ponto in pontos:
            if any(c.contem_ponto(ponto) for c in self.construcoes):
                bloqueados.append(ponto)
            elif any(c.contem_ponto(ponto) for c in cameras):
                cobertos.append(ponto)
            else:
                descobertos.append(ponto)
        return cobertos, bloqueados, descobertos
    
    def _desenhar_elementos_base(self) -> None:
        """Configura o estilo e desenha os elementos estáticos do gráfico."""
        colors = {"bg": "#2B2B2B", "text": "#DCE4EE", "grid": "#565B5E"}
        self.fig.patch.set_facecolor(colors["bg"])
        self.ax.set_facecolor(colors["bg"])
        self.ax.tick_params(colors=colors["text"])
        for spine in self.ax.spines.values():
            spine.set_color(colors["grid"])
        self.ax.title.set_color(colors["text"])
        self.ax.set_aspect('equal', adjustable='box')
        self.ax.set_xlim(0, 200)
        self.ax.set_ylim(0, 200)
        self.ax.set_title("QuadCams")
        if self.imagem_fundo is not None:
            self.ax.imshow(self.imagem_fundo, extent=[0, 200, 0, 200], aspect='auto')

    def _desenhar_elementos_simulacao(self, nos_folha: List, cameras: List, cobertos: List, bloqueados: List, descobertos: List) -> None:
        """Desenha os elementos dinâmicos da simulação (quadtree, câmeras, pontos)."""
        colors = {"bg": "#2B2B2B", "text": "#DCE4EE", "grid": "#565B5E"}
        for no in nos_folha:
            f = no.fronteira
            self.ax.add_patch(plt.Rectangle((f.x-f.w, f.y-f.h), f.w*2, f.h*2, fc='none', ec=colors["grid"], lw=0.4, alpha=0.7))
        for c in self.construcoes:
            self.ax.add_patch(plt.Rectangle((c.x-c.w, c.y-c.h), c.w*2, c.h*2, fc='dimgray', ec='black', lw=1.5, alpha=0.8))
        for c in cameras:
            self.ax.add_patch(plt.Circle((c.x, c.y), c.raio, fc='cornflowerblue', ec='darkblue', lw=1.5, alpha=0.4))
        
        if bloqueados:
            px, py = zip(*[(p.x, p.y) for p in bloqueados]); self.ax.plot(px, py, 'x', c='red', ms=10, mew=2.5, label='Bloqueado')
        if cobertos:
            px, py = zip(*[(p.x, p.y) for p in cobertos]); self.ax.plot(px, py, 'o', c='lime', ms=10, mec='darkgreen', mew=1.5, label='Coberto')
        if descobertos:
            px, py = zip(*[(p.x, p.y) for p in descobertos]); self.ax.plot(px, py, '.', c='blue', ms=12, label='Descoberto')
        
        if any([cobertos, bloqueados, descobertos]):
            legend = self.ax.legend(loc='upper right', facecolor=colors["bg"], edgecolor=colors["grid"])
            plt.setp(legend.get_texts(), color=colors["text"])


if __name__ == '__main__':
    app = App()
    app.mainloop()