# LT Challenge

Este proyecto analiza datos de tweets para resolver tres problemas específicos utilizando dos enfoques diferentes: uno optimizado para tiempo de ejecución y otro para uso de memoria.

## Estructura del Proyecto

```bash
├── docker # Recursos CI/CD para github actions y gcp
│   ├── Dockerfile.deploy
│   ├── Dockerfile.dev
│   ├── requirements_deploy.txt
│   ├── requirements_dev.txt
│   ├── requirements_stage.txt
│   └── service.py
├── __init__.py
├── README.md
├── src
│   ├── challenge.ipynb
│   ├── __init__.py
│   ├── q1_memory.py
│   ├── q1_time.py
│   ├── q2_memory.py
│   ├── q2_time.py
│   ├── q3_memory.py
│   ├── q3_time.py
│   └── stats.py # Mediciones de optimizacion (acceptance tests)
└── test # Unit tests para unit tests
    ├── __init__.py
    ├── q1_tests.py
    ├── q2_tests.py
    ├── q3_tests.py
    └── resources
        └── twitter_test.json # Datos ligeros para los unit tests
└── .github/
    └── workflows/
        ├── pr_deploy.yml
        └── pr_staging.yml
```

## Problemas Resueltos

1. **Top 10 fechas con más tweets con usuario más recurrente**
   - Funciones: `q1_time()` y `q1_memory()`
   - Resultado: Lista de tuplas con fecha y usuario con más publicaciones ese día

2. **Top 10 emojis más usados**
   - Funciones: `q2_time()` y `q2_memory()`
   - Resultado: Lista de tuplas con emoji y su conteo

3. **Top 10 usuarios más influyentes**
   - Funciones: `q3_time()` y `q3_memory()`
   - Resultado: Lista de tuplas con username y conteo de menciones

## Cómo Ejecutar Local

1. Instalar docker y ejecutar su daemon
2. Contruir imagen del contenedor:
```
  docker build -f docker/Dockerfile.dev -t ltchallenge_env .
```
3. Ejecutar imagen ltchallenge_env, asegurate de tener libre el puerto 8080
```
  docker run --name ltchallenge -it -p 8080:8080 -v $(pwd):/app ltchallenge_env
```

## Análisis Detallado

Para un análisis más profundo y visualización de resultados, consulta el notebook Jupyter `challenge.ipynb` en la carpeta `src/`.

## CI/CD Workflow

Este proyecto implementa un workflow de CI/CD utilizando GitHub Actions. El proceso se divide en dos etapas principales:
![cicd image](/img/ltchallenge_cicd.drawio.png "CI/CD")

### Pull Requests a la rama `stage`
Pruebas estandar para verificacion de funcionalidad. Estas mismas se ejecutan en el runner de github actions.

- Se ejecutan pruebas unitarias para verificar funcionalidad básica de cada función.
- Archivo de configuración: `.github/workflows/pr_staging.yml`

### Pull Requests a la rama `main`
Introducción de pruebas de aceptación: Una vez superadas las pruebas de código, la evaluación de métricas de reducción de tiempos y optimización de memoria permite la mejora continua del repositorio subyacente, haciéndolo más eficiente.

- Se comparan las métricas de rendimiento con la versión anterior del código.
- Los PRs son rechazados automáticamente si las métricas de tiempo o memoria se reducen.
- Archivo de configuración: `.github/workflows/pr_deploy.yml`

**Diseño:** Escoger cloud run para acceptance tests permite un estandar para que todos los desarrolladores tengan un estandar donde no haya variaciones de hardware que puedan afectar tiempos de procesamiento y memoria. Asi mismo, permite si se desea escalar datos asi mismo el sistema pueda escalar. 

## Autor

[Gabriel Preciado]
[gtm144@hotmail.com]
