const mapa = document.getElementById('mapa');
const enlaces = document.querySelectorAll('.enlace-mapa');
const rutaCarpeta = 'mapas/';
const imagenOriginal = mapa.src;

enlaces.forEach(enlace => {
  enlace.addEventListener('mouseenter', () => {
    const nombreArchivo = enlace.getAttribute('data-img');

    mapa.src = `${rutaCarpeta}${nombreArchivo}`;
  });

  enlace.addEventListener('mouseleave', () => {
    mapa.src = imagenOriginal;
  });
});