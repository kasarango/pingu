# -*- encoding: utf-8 -*-
import pilasengine

pilas = pilasengine.iniciar()        
puntaje = 0
#Crear clase para el menu       
class EscenaMenu(pilasengine.escenas.Escena): 
    
    def iniciar(self): #Abrimos un método llamado iniciar para fondos e imagenes para el menu
        self.pilas.fondos.FondoMozaico('portada.png')
        actor_texto = self.pilas.actores.Actor()
        actor_texto.imagen = "letras.png"
        self._aplicar_animacion(actor_texto)
        self.pilas.eventos.click_de_mouse.conectar(self._iniciar_juego)

    def _aplicar_animacion(self, texto): #Creamos un método para aplicar la animación al menú
        texto.y = -500
        texto.escala = 4        #Tamaño del texto
        texto.escala = [1.4], 1.5
        texto.y = [5], 1
        texto.x = -170
        texto.rotacion = 5      #La rotación del texto

    def _iniciar_juego(self, evento): #Método para iniciar el juego
        self.pilas.escenas.EscenaJuego()

class BotonVolver(pilasengine.actores.Actor): #Creamos una clase para el boton volver

    def iniciar(self):      
        self.imagen = "boton_volver.png"        # Insertar imagen del botón volver
        self.cuando_hace_click = self._volver_a_iniciar
        self.y = 300
        self.y = [200]
        self.x = -200

    def _volver_a_iniciar(self, evento):
        self.pilas.escenas.EscenaMenu()
        # Insertar sonido de inicio
        sonido_de_cancion = pilas.sonidos.cargar('editada.wav')    
        sonido_de_cancion.reproducir()

class EscenaJuego(pilasengine.escenas.Escena):
    #Agregar sonido cuando se regresa al menú
    sonido_de_cancion = pilas.sonidos.cargar('editada.wav')
    sonido_de_cancion.reproducir()
        
    def iniciar(self):
        global puntaje
        fondo = pilas.fondos.DesplazamientoHorizontal()
        fondo.agregar('cielo2.jpg') # Insertamos la imagen cielo
        self._crear_fondo()
        self._crear_boton_volver()
        pingu = self.pilas.actores.Pingu(y=-180, x=-800)
        pingu.aprender(pilas.habilidades.PuedeExplotar)
        self.pilas.eventos.click_de_mouse.conectar(self._cuando_hace_click)
        puntos = pilas.actores.Puntaje(290, 200, color="blanco")
        #Le permite al autor moverse para todos los lados de forma retangular
        figura = pilas.fisica.Rectangulo(-280,-160,10,10, sensor=True, friccion=0, restitucion=0)
        pingu.aprender(pilas.habilidades.Imitar, figura)
        pingu.aprender(pilas.habilidades.MoverseConElTeclado)
        puntaje = 0
        pilas.avisar("Para moverme utilizar las teclas de direccion")
            
        # Crear una clase para obtener las moneds y el puntaje del jugador
        class MonedasPuntaje(pilasengine.actores.Actor):
            
            def iniciar(self):
                self.imagen = "data/manual/imagenes/actores/moneda.png"
                self.grilla = pilas.imagenes.cargar_grilla("data/moneda.png", 8)
                self.animacion = pilas.actores.Animacion(self.grilla, ciclica=True, velocidad=5)
                self.escala = 1
                self.x = 600 + pingu.x
                self.y = pilas.azar(-180, -50)
                self.velocidad = 1.5
                
                
            def actualizar(self):
                self.x -= self.velocidad
                
                if self.x < -400:
                    self.eliminar()
                if self.y > -50:
                    self.x = -50
        
        class PiedrasEnemigas(pilasengine.actores.Piedra):
            
            def iniciar(self):
                self.imagen = "piedra_grande.png"
                self.escala = 1
                self.x = 600 + pingu.x
                self.y = pilas.azar(-180, -40)
                self.velocidad = 2
                
            def actualizar(self):
                self.rotacion += 5
                self.x -= self.velocidad
                
                if self.x < -400:
                    self.eliminar()
        
        moneda = pilas.actores.Grupo()
        piedras = pilas.actores.Grupo()
        
        def crear_monedas():
            actor = MonedasPuntaje(pilas)
            moneda.agregar(actor)
        
        def crear_Piedras():
            actor = PiedrasEnemigas(pilas)
            piedras.agregar(actor)
        
        pilas.tareas.siempre(1.5, crear_monedas)
        pilas.tareas.siempre(2, crear_Piedras) 
        piedras.aprender(pilas.habilidades.PuedeExplotarConHumo)
        
        def coger_moneda(pingu, moneda):
            moneda.eliminar()
            global puntaje
            puntos.aumentar(cantidad = 2)    # La moneda tendrá un valor de 2
            puntaje += 2    # Cuando el pingüino coge una moneda, éste suma 2
            if puntaje == 20:
               pilas.actores.Texto("GANO EL JUEGO")    # Muestra msj en pantalla al usuario
                     
            sonido_de_cancion = pilas.sonidos.cargar('saltar.wav')
            sonido_de_cancion.reproducir()
    
        def cuando_toca_piedra(pingu, piedras):
            pingu.eliminar()
            piedras.eliminar()
            self.fondo_alejado = pilas.fondos.DesplazamientoHorizontal()
            self.fondo_alejado.agregar('isla.png',  y=-15, velocidad=0)
            self.fondo_alejado.z = 97

            self.fondo_agua = pilas.fondos.DesplazamientoHorizontal()
            self.fondo_agua.agregar('mar.png',  0, 200, 1)
            self.fondo_agua.z = 100
            pilas.actores.Texto("PERDIO EL JUEGO")
        #Ayuda a mantener al actor dentro de la pantalla a la vista
        def cuando_toca_barra(protagonista, barra):
            protagonista.eliminar()
        
        pingu.aprender("LimitadoABordesDePantalla")
        pingu.etiquetas.agregar('protagonista')
        rectangulo = pilas.fisica.Rectangulo(-319, 0, 1300, 5, sensor=True)
        rectangulo.etiquetas.agregar('bloque')
        pilas.colisiones.agregar(pingu, moneda, coger_moneda)
        pilas.colisiones.agregar(pingu, piedras, cuando_toca_piedra)
        pilas.colisiones.agregar('protagonista', 'bloque', cuando_toca_barra)
        
    def _crear_boton_volver(self):
        pilas.actores.BotonVolver()

    def _crear_fondo(self):
         
        self.fondo_alejado = pilas.fondos.DesplazamientoHorizontal()
        self.fondo_alejado.agregar('isla.png',  y=-15, velocidad=0.3)
        self.fondo_alejado.z = 97

        self.fondo_agua = pilas.fondos.DesplazamientoHorizontal()
        self.fondo_agua.agregar('mar.png',  y=200, velocidad=0.3)
        self.fondo_agua.z = 100
        
    def actualizar(self):
        self.fondo_agua.desplazar(1)
        self.fondo_alejado.desplazar(1)

    def _cuando_hace_click(self, evento):
        actor = (evento.x, evento.y)
        
## Vinculamos todas las escenas.
pilas.escenas.vincular(EscenaMenu)
pilas.escenas.vincular(EscenaJuego)

## Vinculamos los actores Personalizados
pilas.actores.vincular(BotonVolver)

# Se inicia la escena principal
pilas.escenas.EscenaMenu()

pilas.ejecutar()