|image1| |image2|\ |image3|\ |image4| |image5|

.. _transformación-de-park--clarke:

Transformación de Park & Clarke
===============================

La librería de Park (dq0) & Clarke (α, *β* ) incluye los módulos
siguientes :

-  Transformación de componentes del tiempo, marco A, B, C a ejes nuevos
   ejes de referencia estacionario ortogonal α, *β*.

-  Inversa de Clarke, ejes de referencia estacionario ortogonal α, *β* a
   componentes del dominio del tiempo, marco A, B , C.

-  Transformación de componentes del tiempo, marco ABC hacia un sistema
   de referencia dq0 en régimen permanente.

-  Inversa de Park, ejes de referencia rotatorio dq0 a componentes del
   dominio del tiempo, marco A, B, C.

-  Transformación de referencia estacionario ortogonal α, *β* hacia un
   marco de referencia rotatorio dq0.

Instalación
-----------

La instalación del módulo se realiza con :

.. code:: python

   pip install ClarkePark

Transformación (a,b,c) - (α, *β*)
---------------------------------

El módulo tiene dependencias siendo necesario instalar ``numpy`` para
procesar la información. También será necesario instalar e importar
``matplotlib.pyplot`` para visualizar los resultados.

.. code:: tex

   alpha, beta, z = ClarkePark.abc_to_alphaBeta0(A,B,C)

Para poder usar la transformación es necesario generar las tres señales
monofásicas en desfase y balanceadas.

.. code:: python

   import ClarkePark
   import numpy as np
   import matplotlib.pyplot as plt

   end_time = 10/float(60)
   step_size = end_time/(1000)
   t = np.arange(0,end_time,step_size)
   wt = 2*np.pi*float(60)*t

   rad_angA = float(0)*np.pi/180
   rad_angB = float(240)*np.pi/180
   rad_angC = float(120)*np.pi/180

   A = (np.sqrt(2)*float(127))*np.sin(wt+rad_angA)
   B = (np.sqrt(2)*float(127))*np.sin(wt+rad_angB)
   C = (np.sqrt(2)*float(127))*np.sin(wt+rad_angC)

   alpha, beta, z = ClarkePark.abc_to_alphaBeta0(A,B,C)

Graficando se obtiene las señales de tensión (A, B, C)

.. figure:: https://i.ibb.co/59wxgbm/02.jpg
   :alt: 

Graficando el marco de referencia (α, *β*)

Transformación (ABC) - (dq0)
----------------------------

La transformación del marco ABC al sistema de referencia dq0,
implementando la misma señal se obtiene con

.. code:: python

   d, q, z = ClarkePark.abc_to_dq0(A, B, C, wt, delta)

Un sistema rotatorio puede ser analizado con la transformación de Park
generándose dos señales de valor constante en régimen permanente.

Transformación inversa (dq0) - (ABC)
------------------------------------

La transformación inversa de Park, ejes de referencia rotatorio dq0 a
componentes del dominio del tiempo, marco A, B, C.

.. code:: python

   a, b, c = ClarkePark.dq0_to_abc(d, q, z, wt, delta)

De un marco de referencia constante (dq0) puede ser cambiado al sistema
(ABC) de variables senoidales en el tiempo.

Implementaremos un sistema balanceado y aplicaremos el marco de
referencia constante (dq0) con las líneas siguientes :

.. code:: python

   import ClarkePark
   import numpy as np
   import matplotlib.pyplot as plt

   end_time = 3/float(60)
   step_size = end_time/(1000)
   delta=0
   t = np.arange(0,end_time,step_size)
   wt = 2*np.pi*float(60)*t

   rad_angA = float(0)*np.pi/180
   rad_angB = float(240)*np.pi/180
   rad_angC = float(120)*np.pi/180

   A = (np.sqrt(2)*float(127))*np.sin(wt+rad_angA)
   B = (np.sqrt(2)*float(127))*np.sin(wt+rad_angB)
   C = (np.sqrt(2)*float(127))*np.sin(wt+rad_angC)

   d, q, z = ClarkePark.abc_to_dq0(A, B, C, wt, delta)
   a, b, c = ClarkePark.dq0_to_abc(d, q, z, wt, delta)

Los resultados obtenidos en líneas anteriores son graficadas mediante

.. code:: python

   plt.figure(figsize=(8,3))
   plt.plot(t, a, label="A", color="royalblue")
   plt.plot(t, b, label="B", color="orangered")
   plt.plot(t, c, label="C" , color="forestgreen")
   plt.legend(['A','B','C'])
   plt.legend(ncol=3,loc=4)
   plt.ylabel("Tensión [Volts]")
   plt.xlabel("Tiempo [Segundos]")
   plt.title(" Sistema trifásico ABC")
   plt.grid('on')
   plt.show()

Finalmente se obtiene las señales del sistema trifásico ABC mediante la
transformación inversa dq0 al sistema ABC.

.. figure:: https://i.ibb.co/gtWbCj7/Figure-2.png
   :alt: 

Transformación marco (α, *β*) - (dq0)
-------------------------------------

La transformación inversa de Park, ejes de referencia rotatorio dq0 a
componentes del dominio del tiempo, marco A, B, C.

.. code:: python

   d, q, z = ClarkePark.alphaBeta0_to_dq0(alpha, beta, zero, wt, delta)

Si el marco de referencia estacionario ortogonal α, *β* es posible
obtener el marco de referencia rotatorio dq0. Usando el mismo bloque de
código de la transformación inversa y añadiendo la línea siguiente de
código.

.. code:: 

   alpha, beta, z = ClarkePark.abc_to_alphaBeta0(a,b,c)

Y cambiando de nuevo al nuevo sistema los resultados serán los mismos a
los mostrados en la transformación de marco de referencia rotatorio dq0.

.. code:: 

   d, q, z = ClarkePark.alphaBeta0_to_dq0(alpha, beta, z, wt, delta)

Referencias
-----------

[1] Kundur, P. (1994). *Power System Stability and Control.* McGraw-Hill
Education.

[2] J.C.DAS. (2016). *Understanding Symmetrical Components for Power
System Modeling.* Piscataway: IEEE Press Editorial Board.

.. |image1| image:: https://badge.fury.io/py/ClarkePark.svg
   :target: https://badge.fury.io/py/ClarkePark
.. |image2| image:: https://img.shields.io/badge/python-3 | 3.5 | 3.6 | 3.7 | 3.8 | 3.9-blue
   :target: https://pypi.org/project/ClarkePark/
.. |image3| image:: https://pepy.tech/badge/clarkepark
   :target: https://pepy.tech/project/clarkepark
.. |image4| image:: https://pepy.tech/badge/clarkepark/month
   :target: https://pepy.tech/project/clarkepark
.. |image5| image:: https://api.codeclimate.com/v1/badges/6abceb2a140780c13d17/maintainability
   :target: https://codeclimate.com/github/jacometoss/ClarkePark/maintainability
