# civilas_web
Repositorio de la solución web y de backend del proyecto de reportes de crímenes civilas

## Tabla de contenidos

[Arquitectura](#Arquitectura)  



###### Problema identificado

Si bien cada uno de nosotros conoce su barrio, sabe de los problemas que tiene o de qué lugares evitar por razones de seguridad, esto no se puede traducir a la ciudad en general, por lo que una herramienta que permita a los usuarios conocer la situación de criminalidad en distintos barrios de la ciudad puede ser muy útil a la hora de estar preparado y alerta cuando se visita una zona que no se conoce.

###### Solución

La intención de este proyecto es proveer de una plataforma donde miembros de la ciudadanía puedan reportar crímenes cometidos, el usuario introducirá la localización del siniestro y el tipo de siniestro (robo, asalto, detonación de arma de fuego, etc). Los siniestros reportados se guardarán en la base de datos, una vez teniendo esta información los usuarios podrán seleccionar un punto del mapa y el programa les devolverá las estadísticas de crimen en la zona,  para esto una vez obtenida las coordenadas indicadas por el usuario se consultaron los crímenes cometidos en un área de 1000 metros a la redonda.

A lo que espera llegar con esto es una vez teniendo una base de datos lo suficientemente grande la información recabada pueda funcionar como un indicador real y dinámico de la situación de seguridad en la ciudad y podría funcionar como una herramienta libre de ataduras de gobierno e intereses externos al ser una herramienta creada y mantenida por la comunidad.

<a name="Arquitectura"/>
###### Arquitectura

Este proyecto está desarrollado en Django. Django es un framework fullstack escrito en python. Nuestra base de datos es una base de datos de PostgreSQL que cuenta con la función extra de Postgis, esto nos permite realizar los queries geográficos que son necesarios para poder traer los crímenes realizados alrededor de una zona en la que busque el usuario.

Este es el diagrama de la aplicación:

<img width="442" alt="image" src="https://user-images.githubusercontent.com/57050096/117603275-47fc9880-b118-11eb-83eb-39dd7940f55f.png">

