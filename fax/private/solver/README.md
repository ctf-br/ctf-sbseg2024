# Instruções para usar o solver

* Baixe o [spandsp do repositório git](https://github.com/freeswitch/spandsp). Este script foi testado com o commit 933d40db635d6b2717dc4ee9cb3f72be06b0e8ee.

* Compile o spandsp com `./configure --enable-tests && make -j8`. Se ele reclamar da ausência do utilitário `fax2tiff`, compile da versão 4.4.0 da libtiff, pois esse utilitário foi removido de versões mais recentes da libtiff.

* Adicione o diretório `tests` do spandsp ao PATH e execute `make` neste diretório.
