# Sumario de Patrones de Diseño, Orientación a Objetos y Principios SOLID

---

## Patrones de Diseño

Los patrones de diseño son soluciones reutilizables a problemas comunes en el diseño de software. Se dividen principalmente en tres categorías:

### 1. Patrones Creacionales

- **Singleton:** Garantiza que una clase tenga una única instancia y proporciona un punto de acceso global.
  - *Ejemplo:* Un controlador de conexión a base de datos único en la aplicación.
    
    ```
    class DatabaseConnection:
      _instance = None

      def __new__(cls, connection_string: str):
        # Ignoramos el connection_string después de la primera vez
        if cls._instance is None:
          print("Creando nueva conexión a la BD...")
          cls._instance = super().__new__(cls)
          cls._instance.connection_string = connection_string
        return cls._instance

      def query(self, sql: str):
        print(f"[{self.connection_string}] Ejecutando SQL: {sql}")

    db1 = DatabaseConnection("postgres://prod")
    db2 = DatabaseConnection("postgres://otro")  # Se ignora el nuevo string

    print(db1 is db2)  # True, misma instancia
    db1.query("SELECT * FROM usuarios")
    ```
  
- **Factory Method:** Define una interfaz para crear un objeto, pero permite que las subclases decidan qué clase instanciar.
  - *Ejemplo:* Un sistema de notificaciones que crea diferentes tipos de mensajes (email, SMS) según configuración.

    ```
    from abc import ABC, abstractmethod

    class Notificador(ABC):
      @abstractmethod
      def enviar(self, mensaje: str):
        pass

    class NotificadorEmail(Notificador):
      def enviar(self, mensaje: str):
        print(f"[EMAIL] Enviando: {mensaje}")

    class NotificadorSMS(Notificador):
      def enviar(self, mensaje: str):
        print(f"[SMS] Enviando: {mensaje}")

    class NotificadorFactory:
      @staticmethod
      def crear_notificador(tipo: str) -> Notificador:
        if tipo == "email":
          return NotificadorEmail()
        elif tipo == "sms":
          return NotificadorSMS()
        raise ValueError(f"Tipo de notificación no soportado: {tipo}")
    
    # Uso
    config_tipo = "email"
    notificador = NotificadorFactory.crear_notificador(config_tipo)
    notificador.enviar("Tu pedido ha sido despachado.")
    ```

- **Abstract Factory:** Permite crear familias de objetos relacionados sin especificar sus clases concretas.
  - *Ejemplo:* Una aplicación que crea componentes UI para diferentes plataformas (Windows, macOS) usando fábricas abstractas.
 
    ```
    from abc import ABC, abstractmethod

    # Productos abstractos
    class Boton(ABC):
      @abstractmethod
      def dibujar(self):
        pass

    class CheckBox(ABC):
      @abstractmethod
      def dibujar(self):
        pass

    # Productos concretos
    class BotonWindows(Boton):
      def dibujar(self):
        print("Dibujando Botón estilo Windows")

    class CheckBoxWindows(CheckBox):
      def dibujar(self):
        print("Dibujando CheckBox estilo Windows")

    class BotonMac(Boton):
      def dibujar(self):
        print("Dibujando Botón estilo macOS")

    class CheckBoxMac(CheckBox):
      def dibujar(self):
        print("Dibujando CheckBox estilo macOS")
    
    # Fábrica abstracta
    class UIFactory(ABC):
      @abstractmethod
      def crear_boton(self) -> Boton:
        pass
    
      @abstractmethod
      def crear_checkbox(self) -> CheckBox:
        pass

    # Fábricas concretas
    class WindowsFactory(UIFactory):
      def crear_boton(self) -> Boton:
        return BotonWindows()

      def crear_checkbox(self) -> CheckBox:
        return CheckBoxWindows()

    class MacFactory(UIFactory):
      def crear_boton(self) -> Boton:
        return BotonMac()

      def crear_checkbox(self) -> CheckBox:
        return CheckBoxMac()
    
    # Cliente
    def construir_pantalla(factory: UIFactory):  
      boton = factory.crear_boton()
      checkbox = factory.crear_checkbox()
      boton.dibujar()
      checkbox.dibujar()

    factory = WindowsFactory()
    construir_pantalla(factory)
    ```

- **Builder:** Separa la construcción de un objeto complejo de su representación para que el mismo proceso pueda crear varias representaciones.
  - *Ejemplo:* Construcción paso a paso de un informe con diferentes formatos (HTML, PDF).

    ```
    class Reporte:
      def __init__(self):
        self.titulo = ""
        self.contenido = ""
        self.footer = ""

      def __str__(self):
        return f"{self.titulo}\n\n{self.contenido}\n\n{self.footer}"

    class ReporteBuilder:
      def __init__(self):
        self.reporte = Reporte()

      def con_titulo(self, titulo: str):
        self.reporte.titulo = titulo
        return self

      def con_contenido(self, contenido: str):
        self.reporte.contenido = contenido
        return self

      def con_footer(self, footer: str):
        self.reporte.footer = footer
        return self

      def build(self) -> Reporte:
        return self.reporte

    # Uso
    builder = ReporteBuilder()
    reporte = (
      builder
        .con_titulo("Informe de Ventas Q1")
        .con_contenido("Contenido detallado de ventas...")
        .con_footer("Generado automáticamente por el sistema.")
        .build()
    )

    print(reporte)
    ```

- **Prototype:** Permite copiar objetos existentes sin hacer el código dependiente de sus clases.
  - *Ejemplo:* Clonar configuraciones de usuario para crear nuevas sesiones rápidamente.

    ```
    import copy

    class ConfigUsuario:
      def __init__(self, tema: str, idioma: str, notificaciones: bool):
        self.tema = tema
        self.idioma = idioma
        self.notificaciones = notificaciones

      def clonar(self) -> "ConfigUsuario":
        # Devuelve una copia superficial
        return copy.copy(self)

      def __repr__(self):
        return f"ConfigUsuario(tema={self.tema}, idioma={self.idioma}, notificaciones={self.notificaciones})"

    config_base = ConfigUsuario("oscuro", "es", True)
    config_nueva_sesion = config_base.clonar()
    config_nueva_sesion.idioma = "en"  # Cambiamos algo específico

    print(config_base)
    print(config_nueva_sesion)
    ```

### 2. Patrones Estructurales

- **Adapter:** Permite que interfaces incompatibles trabajen juntas convirtiendo la interfaz de una clase en otra esperada.
  - *Ejemplo:* Adaptar una API antigua para que encaje con la nueva interfaz del sistema.

    ```
    class LegacyPaymentGateway:
      def hacer_pago(self, cantidad: float):
        print(f"[LEGACY] Pago realizado por {cantidad}")

    class PaymentProcessor:
      def pagar(self, monto: float):
        raise NotImplementedError
   
    class LegacyPaymentAdapter(PaymentProcessor):
      def __init__(self, legacy_gateway: LegacyPaymentGateway):
        self.legacy_gateway = legacy_gateway

      def pagar(self, monto: float):
        # Adaptamos el método antiguo al nuevo nombre
        self.legacy_gateway.hacer_pago(monto)

    # Uso
    legacy = LegacyPaymentGateway()  
    processor = LegacyPaymentAdapter(legacy)
    processor.pagar(100.0)
    ```
  

- **Decorator:** Añade responsabilidades a objetos de forma dinámica.
  - *Ejemplo:* Agregar funcionalidad de logging a un servicio sin modificar su código.

    ```
    from abc import ABC, abstractmethod
    
    class Servicio(ABC):
      @abstractmethod
      def ejecutar(self):
        pass

    class ServicioPago(Servicio):
      def ejecutar(self):
        print("Procesando pago...")

    class ServicioConLogging(Servicio):
      def __init__(self, servicio: Servicio):
        self._servicio = servicio

    def ejecutar(self):
        print("[LOG] Antes de ejecutar servicio")
        self._servicio.ejecutar()
        print("[LOG] Después de ejecutar servicio")

    # Uso
    servicio = ServicioPago()
    servicio_log = ServicioConLogging(servicio)
    servicio_log.ejecutar()
    ```

- **Facade:** Proporciona una interfaz simplificada a un conjunto de interfaces de un subsistema.
  - *Ejemplo:* Un punto único de acceso para operaciones complejas sobre subsistemas de pagos.

    ```
    class ValidadorFraude:
      def validar(self, pedido_id: int) -> bool:
        print(f"Validando fraude para pedido {pedido_id}")
        return True

    class PasarelaPago:
      def cobrar(self, monto: float) -> bool:
        print(f"Cobrando {monto} con pasarela de pago")
        return True

    class GeneradorFactura:
      def generar(self, pedido_id: int):
        print(f"Generando factura para pedido {pedido_id}")

    class PaymentFacade:
      def __init__(self):
        self._fraude = ValidadorFraude()
        self._pasarela = PasarelaPago()
        self._factura = GeneradorFactura()

      def procesar_pago(self, pedido_id: int, monto: float):
        if not self._fraude.validar(pedido_id):
          print("Pago rechazado por fraude")
          return
        if not self._pasarela.cobrar(monto):
            print("Error en la pasarela de pago")
            return
        self._factura.generar(pedido_id)
        print("Pago procesado correctamente")

    facade = PaymentFacade()
    facade.procesar_pago(pedido_id=123, monto=199.99)
    ```

- **Composite:** Permite tratar objetos individuales y composiciones de objetos de la misma manera.
  - *Ejemplo:* Representar una estructura de carpetas y archivos de forma unificada.

    ```
    from abc import ABC, abstractmethod

    class NodoArchivo(ABC):
      @abstractmethod
      def mostrar(self, indent: int = 0):
        pass

    class Archivo(NodoArchivo):
      def __init__(self, nombre: str):
        self.nombre = nombre

      def mostrar(self, indent: int = 0):
        print(" " * indent + f"- {self.nombre}")

    class Carpeta(NodoArchivo):
      def __init__(self, nombre: str):
        self.nombre = nombre
        self.hijos: list[NodoArchivo] = []

      def agregar(self, nodo: NodoArchivo):
        self.hijos.append(nodo)

      def mostrar(self, indent: int = 0):
        print(" " * indent + f"[{self.nombre}]")
        for hijo in self.hijos:
            hijo.mostrar(indent + 2)

    # Uso
    root = Carpeta("root")
    docs = Carpeta("docs")
    img = Carpeta("img")

    root.agregar(docs)
    root.agregar(img)
    docs.agregar(Archivo("README.md"))
    img.agregar(Archivo("logo.png"))

    root.mostrar()
    ```

- **Proxy:** Proporciona un sustituto o representante que controla el acceso a otro objeto.
  - *Ejemplo:* Proxy de acceso a una imagen que carga la imagen solo cuando es necesario.

    ```
    from abc import ABC, abstractmethod

    class Imagen(ABC):
      @abstractmethod
      def mostrar(self):
        pass

    class ImagenReal(Imagen):
      def __init__(self, ruta: str):
        self.ruta = ruta
        self._cargar_desde_disco()

      def _cargar_desde_disco(self):
        print(f"Cargando imagen pesada desde disco: {self.ruta}")

      def mostrar(self):
        print(f"Mostrando imagen: {self.ruta}")

    class ImagenProxy(Imagen):
      def __init__(self, ruta: str):
        self.ruta = ruta
        self._imagen_real: ImagenReal | None = None

      def mostrar(self):
        if self._imagen_real is None:
          self._imagen_real = ImagenReal(self.ruta)
        self._imagen_real.mostrar()

    # Uso
    imagen = ImagenProxy("foto_hd.png")
    print("La app sigue respondiendo...")
    imagen.mostrar()  # Aquí recién se carga de verdad
    ```

### 3. Patrones de Comportamiento

- **Observer:** Define una dependencia uno-a-muchos para que cuando un objeto cambie su estado, todos sus dependientes sean notificados.
  - *Ejemplo:* Sistema de notificaciones donde múltiples componentes reaccionan a cambios de estado.
 
    ```
    from abc import ABC, abstractmethod

    class Observador(ABC):
      @abstractmethod
      def actualizar(self, precio: float):
        pass

    class Stock(ABC):
      def __init__(self):
        self._observadores: list[Observador] = []

      def agregar_observador(self, obs: Observador):
        self._observadores.append(obs)

      def notificar(self, precio: float):
        for o in self._observadores:
          o.actualizar(precio)

    class Accion(Stock):
      def __init__(self, simbolo: str):
        super().__init__()
        self.simbolo = simbolo
        self._precio = 0.0

      def set_precio(self, precio: float):
        self._precio = precio
        self.notificar(precio)

    class DashboardInversionista(Observador):
      def __init__(self, nombre: str):
        self.nombre = nombre

      def actualizar(self, precio: float):
        print(f"[{self.nombre}] Nuevo precio: {precio}")

    # Uso
    accion = Accion("I4S")
    accion.agregar_observador(DashboardInversionista("Trader 1"))
    accion.agregar_observador(DashboardInversionista("Trader 2"))

    accion.set_precio(10.5)
    accion.set_precio(11.0)
    ```

- **Strategy:** Define una familia de algoritmos, encapsula cada uno y los hace intercambiables.
  - *Ejemplo:* Diferentes métodos de ordenamiento que se pueden cambiar en tiempo de ejecución.

    ```
    from abc import ABC, abstractmethod

    class EstrategiaDescuento(ABC):
      @abstractmethod
      def calcular(self, monto: float) -> float:
        pass

    class DescuentoBlackFriday(EstrategiaDescuento):
      def calcular(self, monto: float) -> float:
        return monto * 0.5  # 50%

    class DescuentoClienteVIP(EstrategiaDescuento):
      def calcular(self, monto: float) -> float:
        return monto * 0.8  # 20%

    class SinDescuento(EstrategiaDescuento):
      def calcular(self, monto: float) -> float:
        return monto

    class CarritoCompras:
      def __init__(self, estrategia: EstrategiaDescuento):
        self.estrategia = estrategia
        self.monto = 0.0

      def agregar_item(self, precio: float):
        self.monto += precio

      def total(self) -> float:
        return self.estrategia.calcular(self.monto)
    
    # Uso
    carrito = CarritoCompras(EstrategiaDescuento := DescuentoBlackFriday())
    carrito.agregar_item(100)
    carrito.agregar_item(50)

    print("Total con descuento:", carrito.total())
    ```

- **Command:** Encapsula una solicitud como un objeto, permitiendo parametrizar clientes y soportar operaciones deshacer.
  - *Ejemplo:* Sistema de controles de interfaz (botones) con funcionalidad de undo/redo.
 
    ```
    from abc import ABC, abstractmethod

    class Command(ABC):
      @abstractmethod
      def ejecutar(self):
        pass

      @abstractmethod
      def deshacer(self):
        pass

    class EditorTexto:
      def __init__(self):
        self.texto = ""

      def __str__(self):
        return self.texto

    class EscribirTextoCommand(Command):
      def __init__(self, editor: EditorTexto, texto: str):
        self.editor = editor
        self.texto = texto

      def ejecutar(self):
        self.editor.texto += self.texto

      def deshacer(self):
        self.editor.texto = self.editor.texto[:-len(self.texto)]

    class Invoker:
      def __init__(self):
        self.historial: list[Command] = []

      def ejecutar(self, cmd: Command):
        cmd.ejecutar()
        self.historial.append(cmd)

      def deshacer(self):
        if self.historial:
          cmd = self.historial.pop()
          cmd.deshacer()
    
    # Uso
    editor = EditorTexto()
    invoker = Invoker()

    cmd1 = EscribirTextoCommand(editor, "Hola ")
    cmd2 = EscribirTextoCommand(editor, "mundo")

    invoker.ejecutar(cmd1)
    invoker.ejecutar(cmd2)
    print(editor)  # Hola mundo

    invoker.deshacer()
    print(editor)  # Hola
    ```

- **State:** Permite a un objeto alterar su comportamiento cuando su estado interno cambia.
  - *Ejemplo:* Máquina expendedora que cambia de estado tras insertar moneda o seleccionar producto.

    ```
    from abc import ABC, abstractmethod

    class Estado(ABC):
      @abstractmethod
      def insertar_moneda(self, maquina: "MaquinaExpendedora"):
        pass

      @abstractmethod
      def seleccionar_producto(self, maquina: "MaquinaExpendedora"):
        pass

    class SinMonedaState(Estado):
      def insertar_moneda(self, maquina: "MaquinaExpendedora"):
        print("Moneda insertada.")
        maquina.estado = ConMonedaState()

      def seleccionar_producto(self, maquina: "MaquinaExpendedora"):
        print("Inserta una moneda primero.")

    class ConMonedaState(Estado):
      def insertar_moneda(self, maquina: "MaquinaExpendedora"):
        print("Ya hay una moneda, no puedes insertar otra.")

      def seleccionar_producto(self, maquina: "MaquinaExpendedora"):
        print("Producto dispensado.")
        maquina.estado = SinMonedaState()

    class MaquinaExpendedora:
      def __init__(self):
        self.estado: Estado = SinMonedaState()

      def insertar_moneda(self):
        self.estado.insertar_moneda(self)

      def seleccionar_producto(self):
        self.estado.seleccionar_producto(self)
    
    # Uso
    m = MaquinaExpendedora()
    m.seleccionar_producto()
    m.insertar_moneda()
    m.seleccionar_producto()
    ```

- **Template Method:** Define el esqueleto de un algoritmo en una operación, dejando algunos pasos para que las subclases los implementen.
  - *Ejemplo:* Proceso de generación de reportes donde la estructura es fija pero ciertos detalles cambian.

    ```
    from abc import ABC, abstractmethod

    class GeneradorReporte(ABC):
      def generar(self):
        self._abrir()
        self._escribir_cabecera()
        self._escribir_contenido()
        self._cerrar()

      def _abrir(self):
        print("Abriendo archivo de reporte...")

      def _cerrar(self):
        print("Cerrando archivo de reporte...")

      @abstractmethod
      def _escribir_cabecera(self):
        pass

      @abstractmethod
      def _escribir_contenido(self):
        pass
    
    class GeneradorReporteVentas(GeneradorReporte):
      def _escribir_cabecera(self):
        print("Cabecera: Reporte de Ventas")

      def _escribir_contenido(self):
        print("Contenido: Ventas por región, producto, etc.")

    class GeneradorReporteInventario(GeneradorReporte):
      def _escribir_cabecera(self):
        print("Cabecera: Reporte de Inventario")

      def _escribir_contenido(self):
        print("Contenido: Stock actual, reposiciones, etc.")

    # Uso
    reporte = GeneradorReporteVentas()
    reporte.generar()
    ```
---

## Orientación a Objetos (OO)

La programación orientada a objetos es un paradigma basado en el concepto de "objetos", que contienen datos y código para manipular esos datos.

### Conceptos principales:

- **Clase:** Plantilla o molde para crear objetos, define atributos y métodos.
  - *Ejemplo:* Clase `Persona` con atributos `nombre` y métodos `saludar()`.

- **Objeto:** Instancia de una clase.
  - *Ejemplo:* Objeto `juan` de la clase `Persona`.

- **Encapsulamiento:** Ocultar los detalles internos del objeto, exponiendo solo lo necesario.
  - *Ejemplo:* Variables privadas con métodos públicos para acceso.

- **Herencia:** Permite crear nuevas clases basadas en clases existentes.
  - *Ejemplo:* Clase `Estudiante` que hereda de `Persona`.

- **Polimorfismo:** Capacidad de usar una interfaz común para diferentes tipos de objetos.
  - *Ejemplo:* Método `dibujar()` que funciona para `Círculo`, `Cuadrado` y `Triángulo`.

- **Abstracción:** Enfocar en los aspectos esenciales sin mostrar detalles complejos.
  - *Ejemplo:* Interfaz `Vehículo` que define `mover()` sin implementarlo.

    ```
    class Persona:
      # Clase: define atributos y métodos
      def __init__(self, nombre: str, edad: int):
        # Encapsulamiento: atributos "privados" (convención con _)
        self._nombre = nombre
        self._edad = edad

      # Encapsulamiento: getters/setters
      @property
      def nombre(self):
        return self._nombre

      def saludar(self):
        print(f"Hola, soy {self._nombre} y tengo {self._edad} años.")

    # Herencia: Estudiante hereda de Persona
    class Estudiante(Persona):
      def __init__(self, nombre: str, edad: int, carrera: str):
        super().__init__(nombre, edad)
        self.carrera = carrera

      # Polimorfismo: redefinimos saludar
      def saludar(self):
        print(f"Hola, soy {self.nombre}, estudio {self.carrera}.")

    # Abstracción: interfaz de un "Vehículo"
    from abc import ABC, abstractmethod
    
    class Vehiculo(ABC):
      @abstractmethod
      def mover(self):
        pass

    class Auto(Vehiculo):
      def mover(self):
        print("El auto se mueve por la carretera.")
    
    class Bicicleta(Vehiculo):
      def mover(self):
        print("La bicicleta se mueve por la ciclovía.")

    # Uso de conceptos:
    persona = Persona("Ana", 30)  # Objeto (instancia de Persona)
    estudiante = Estudiante("Luis", 20, "Informática")  # Objeto Estudiante

    persona.saludar()
    estudiante.saludar()  # Polimorfismo

    vehiculos: list[Vehiculo] = [Auto(), Bicicleta()]
    for v in vehiculos:
      v.mover()  # Polimorfismo usando la abstracción Vehiculo
    ```
---

## Principios SOLID

Principios para diseño y mantenimiento de software orientado a objetos robusto y flexible:

- **S - Single Responsibility Principle (SRP):** Una clase debe tener una única responsabilidad.
  - *Ejemplo:* Separar la lógica de negocio y la interfaz de usuario en clases distintas.

    ```
    class Factura:
      # Solo conoce datos del invoice
      def __init__(self, monto: float, cliente: str):
        self.monto = monto
        self.cliente = cliente

    class CalculadoraImpuestos:
      # Responsable solo de lógica de impuestos
      def calcular_iva(self, factura: Factura) -> float:
        return factura.monto * 0.19

    class FacturaPrinter:
      # Responsable solo de presentar/imprimir
      def imprimir(self, factura: Factura, iva: float):
        total = factura.monto + iva
        print(f"Cliente: {factura.cliente}, Subtotal: {factura.monto}, IVA: {iva}, Total: {total}")

    # Uso
    factura = Factura(1000, "Empresa X")
    calc = CalculadoraImpuestos()
    iva = calc.calcular_iva(factura)

    printer = FacturaPrinter()
    printer.imprimir(factura, iva)
    ```

- **O - Open/Closed Principle (OCP):** Las entidades deben estar abiertas para extensión pero cerradas para modificación.
  - *Ejemplo:* Añadir nuevos tipos de pago sin modificar el código existente.
 
    ```
    from abc import ABC, abstractmethod

    class MetodoPago(ABC):
      @abstractmethod
      def pagar(self, monto: float):
        pass

    class PagoTarjeta(MetodoPago):
      def pagar(self, monto: float):
        print(f"Pagando {monto} con tarjeta de crédito")

    class PagoPayPal(MetodoPago):
      def pagar(self, monto: float):
        print(f"Pagando {monto} con PayPal")

    # Código cliente cerrado a cambios: solo depende de la abstracción
    class Checkout:
      def __init__(self, metodo_pago: MetodoPago):
        self.metodo_pago = metodo_pago

      def procesar(self, monto: float):
        self.metodo_pago.pagar(monto)

    # Si mañana agrego PagoCrypto, no toco Checkout
    class PagoCrypto(MetodoPago):
      def pagar(self, monto: float):
        print(f"Pagando {monto} con Criptomonedas")

    checkout = Checkout(PagoTarjeta())
    checkout.procesar(500)

    ```

- **L - Liskov Substitution Principle (LSP):** Las subclases deben poder sustituir a sus superclases sin alterar el comportamiento correcto.
  - *Ejemplo:* Un método que funcione con la clase `Animal` debe funcionar igual con `Perro`.

    ```
    class Animal:
      def hacer_sonido(self):
        print("Algún sonido genérico...")

    class Perro(Animal):
      def hacer_sonido(self):
        print("Guau!")

    class Gato(Animal):
      def hacer_sonido(self):
        print("Miau!")

    
    def hacer_hablar(animal: Animal):
      # Esta función debería funcionar bien con cualquier subclase de Animal
      animal.hacer_sonido()
    
    # Uso
    animales: list[Animal] = [Perro(), Gato(), Animal()]
    for a in animales:
      hacer_hablar(a)
    ```

- **I - Interface Segregation Principle (ISP):** Muchas interfaces específicas son mejor que una única interfaz general.
  - *Ejemplo:* Interfaces separadas para `Imprimible` y `Escaneable` en lugar de una interfaz única.

    ```
    from abc import ABC, abstractmethod

    class Imprimible(ABC):
      @abstractmethod
      def imprimir(self, documento: str):
        pass

    class Escaneable(ABC):
      @abstractmethod
      def escanear(self) -> str:
        pass

    class ImpresoraBasica(Imprimible):
      def imprimir(self, documento: str):
        print(f"Imprimiendo: {documento}")

    class Multifuncional(Imprimible, Escaneable):
      def imprimir(self, documento: str):
        print(f"[Multifuncional] Imprimiendo: {documento}")

      def escanear(self) -> str:
        print("[Multifuncional] Escaneando documento...")
        return "Contenido del escaneo"

    # Uso
    impresora = ImpresoraBasica()
    impresora.imprimir("Contrato")

    multi = Multifuncional()
    multi.imprimir("Reporte")
    multi.escanear()
    ```

- **D - Dependency Inversion Principle (DIP):** Depender de abstracciones, no de concreciones.
  - *Ejemplo:* Inyección de dependencias usando interfaces en lugar de clases concretas.

    ```
    from abc import ABC, abstractmethod

    class PasarelaPagoAbstraccion(ABC):
      @abstractmethod
      def cobrar(self, monto: float) -> bool:
        pass

    class StripeGateway(PasarelaPagoAbstraccion):
      def cobrar(self, monto: float) -> bool:
        print(f"[Stripe] cobrando {monto}")
        return True

    class FakeGateway(PasarelaPagoAbstraccion):
      # Para tests
      def __init__(self, debe_funcionar: bool = True):
        self.debe_funcionar = debe_funcionar

      def cobrar(self, monto: float) -> bool:
        print(f"[FakeGateway] monto {monto}, ok={self.debe_funcionar}")
        return self.debe_funcionar

    class PedidoService:
      # Depende de la abstracción, no de StripeGateway directamente
      def __init__(self, pasarela: PasarelaPagoAbstraccion):
        self.pasarela = pasarela

      def procesar_pedido(self, pedido_id: int, monto: float):
        if self.pasarela.cobrar(monto):
            print(f"Pedido {pedido_id} procesado correctamente")
        else:
            print(f"Fallo al procesar pedido {pedido_id}")

    # En producción
    service_prod = PedidoService(StripeGateway())
    service_prod.procesar_pedido(1, 99.99)

    # En tests
    service_test = PedidoService(FakeGateway(debe_funcionar=False))
    service_test.procesar_pedido(2, 50.0)

    ```

---

# Ejemplo Práctico Integrado

Supongamos una aplicación de gestión de pedidos:

- Se usa **Factory Method** para crear distintos tipos de pedidos (online, telefónico).
- Cada pedido es un objeto que implementa la interfaz `Pedido`.
- Se aplica **SRP** separando la lógica de procesamiento del pedido y la interfaz del usuario en clases diferentes.
- **OCP** permite agregar nuevos métodos de pago sin modificar la clase principal.
- La clase base `Pedido` es sustituible con subclases específicas respetando **LSP**.
- Se usan pequeñas interfaces para diferentes funcionalidades respetando **ISP**.
- Dependencias como procesadores de pago se inyectan mediante interfaces para seguir **DIP**.

---

Este sumario es útil como referencia rápida y guía para aplicar buenas prácticas en desarrollo de software orientado a objetos con patrones probados y principios que mejoran la mantenibilidad y escalabilidad.

