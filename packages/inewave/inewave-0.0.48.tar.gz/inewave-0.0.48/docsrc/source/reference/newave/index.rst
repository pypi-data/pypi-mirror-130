.. _newave:

NEWAVE
=======


A estrutura do *inewave* padroniza os objetos de interface existentes para cada um dos três módulos desenvolvidos. 
A interface com o NEWAVE segue o padrão de implementar modelos para armazenar cada uma das informações existentes
nos arquivos de entrada e saída, além de classes utilitárias para gerenciar com a leitura e interpretação das informações
dos arquivos, bem como na geração de novos arquivos.

Classes são nomeadas em ``CamelCase``, enquanto funções, métodos e variáveis recebem seus nomes em ``snake_case``.


Básico da interface NEWAVE
----------------------------

É recomendado que a importação seja feita sempre de forma a utilizar somente os objetos que serão de fato necessários para 
o estudo em questão. Desta forma, é permitido importar ``inewave.newave`` ou utilizar o `wildcard` ``*``. mas não recomendado.

A importação recomendada é, por exemplo::

    >>> from inewave.newave.dger import DGer
    >>> from inewave.nwlistop.mediasmerc import MediasMerc

Para a leitura do arquivo `pmo.dat`::

    >>> from inewave.newave.pmo import PMO
    >>>
    >>> diretorio = "/home/usuario/..."
    >>> pmo = PMO.le_arquivo(diretorio)
    <inewave.newave.pmo.PMO object at 0x000001BC7663B340>

Para a leitura dos arquivos `cmarg00x.out`::

    >>> from inewave.nwlistop.cmarg00 import LeituraCmarg00
    >>>
    >>> diretorio = "/home/usuario/..."
    >>> leitor = LeituraCmarg00(diretorio)
    >>> leitor.le_arquivos()
    {'SUDESTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692820>,
    'SUL': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692790>,
    'NORDESTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692910>,
    'NORTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692970>}
    >>> leitor.cmargs
    {'SUDESTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692820>,
    'SUL': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692790>,
    'NORDESTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692910>,
    'NORTE': <inewave.nwlistop.modelos.cmarg00.Cmarg00 object at 0x000001BC76692970>}

Arquivos
---------

.. toctree::
   :maxdepth: 2

   arquivos/dger
   arquivos/adterm
   arquivos/cadic
   arquivos/curva
   arquivos/re
   arquivos/sistema
   arquivos/patamar
   arquivos/pmo
   arquivos/confhd
   arquivos/dsvagua
   arquivos/vazpast
   arquivos/eafpast
   arquivos/parp
