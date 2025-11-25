# Sumario de Patrones de Diseño, Orientación a Objetos y Principios SOLID

---

## Patrones de Diseño

Los patrones de diseño son soluciones reutilizables a problemas comunes en el diseño de software. Se dividen principalmente en tres categorías:

### 1. Patrones Creacionales

- **Singleton:** Garantiza que una clase tenga una única instancia y proporciona un punto de acceso global.
  - *Ejemplo:* Un controlador de conexión a base de datos único en la aplicación.
  
- **Factory Method:** Define una interfaz para crear un objeto, pero permite que las subclases decidan qué clase instanciar.
  - *Ejemplo:* Un sistema de notificaciones que crea diferentes tipos de mensajes (email, SMS) según configuración.

- **Abstract Factory:** Permite crear familias de objetos relacionados sin especificar sus clases concretas.
  - *Ejemplo:* Una aplicación que crea componentes UI para diferentes plataformas (Windows, macOS) usando fábricas abstractas.

- **Builder:** Separa la construcción de un objeto complejo de su representación para que el mismo proceso pueda crear varias representaciones.
  - *Ejemplo:* Construcción paso a paso de un informe con diferentes formatos (HTML, PDF).

- **Prototype:** Permite copiar objetos existentes sin hacer el código dependiente de sus clases.
  - *Ejemplo:* Clonar configuraciones de usuario para crear nuevas sesiones rápidamente.

### 2. Patrones Estructurales

- **Adapter:** Permite que interfaces incompatibles trabajen juntas convirtiendo la interfaz de una clase en otra esperada.
  - *Ejemplo:* Adaptar una API antigua para que encaje con la nueva interfaz del sistema.

- **Decorator:** Añade responsabilidades a objetos de forma dinámica.
  - *Ejemplo:* Agregar funcionalidad de logging a un servicio sin modificar su código.

- **Facade:** Proporciona una interfaz simplificada a un conjunto de interfaces de un subsistema.
  - *Ejemplo:* Un punto único de acceso para operaciones complejas sobre subsistemas de pagos.

- **Composite:** Permite tratar objetos individuales y composiciones de objetos de la misma manera.
  - *Ejemplo:* Representar una estructura de carpetas y archivos de forma unificada.

- **Proxy:** Proporciona un sustituto o representante que controla el acceso a otro objeto.
  - *Ejemplo:* Proxy de acceso a una imagen que carga la imagen solo cuando es necesario.

### 3. Patrones de Comportamiento

- **Observer:** Define una dependencia uno-a-muchos para que cuando un objeto cambie su estado, todos sus dependientes sean notificados.
  - *Ejemplo:* Sistema de notificaciones donde múltiples componentes reaccionan a cambios de estado.

- **Strategy:** Define una familia de algoritmos, encapsula cada uno y los hace intercambiables.
  - *Ejemplo:* Diferentes métodos de ordenamiento que se pueden cambiar en tiempo de ejecución.

- **Command:** Encapsula una solicitud como un objeto, permitiendo parametrizar clientes y soportar operaciones deshacer.
  - *Ejemplo:* Sistema de controles de interfaz (botones) con funcionalidad de undo/redo.

- **State:** Permite a un objeto alterar su comportamiento cuando su estado interno cambia.
  - *Ejemplo:* Máquina expendedora que cambia de estado tras insertar moneda o seleccionar producto.

- **Template Method:** Define el esqueleto de un algoritmo en una operación, dejando algunos pasos para que las subclases los implementen.
  - *Ejemplo:* Proceso de generación de reportes donde la estructura es fija pero ciertos detalles cambian.

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

---

## Principios SOLID

Principios para diseño y mantenimiento de software orientado a objetos robusto y flexible:

- **S - Single Responsibility Principle (SRP):** Una clase debe tener una única responsabilidad.
  - *Ejemplo:* Separar la lógica de negocio y la interfaz de usuario en clases distintas.

- **O - Open/Closed Principle (OCP):** Las entidades deben estar abiertas para extensión pero cerradas para modificación.
  - *Ejemplo:* Añadir nuevos tipos de pago sin modificar el código existente.

- **L - Liskov Substitution Principle (LSP):** Las subclases deben poder sustituir a sus superclases sin alterar el comportamiento correcto.
  - *Ejemplo:* Un método que funcione con la clase `Animal` debe funcionar igual con `Perro`.

- **I - Interface Segregation Principle (ISP):** Muchas interfaces específicas son mejor que una única interfaz general.
  - *Ejemplo:* Interfaces separadas para `Imprimible` y `Escaneable` en lugar de una interfaz única.

- **D - Dependency Inversion Principle (DIP):** Depender de abstracciones, no de concreciones.
  - *Ejemplo:* Inyección de dependencias usando interfaces en lugar de clases concretas.

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

