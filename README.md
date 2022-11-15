
# LAB DE TELEMATICA - P2

Este repositorio contiene un _VoIP Network Designer_ que se basa en un caso práctico donde una empresa ofrece servicio de VoIP a empresas a nivel nacional. Este servicio consiste en hosting de la PBX y acceso al Proveedor de Servicio VoIP(PROVOIP) mediante SIP TRUNK. Se quiere un diseño de red escalable capazde ofrecer los parámetros de QoE, QoS y GoS requeridos a las empresas cliente. Por eso el programa recibe como entradas las siguientes variables: 

### Llamadas: 

- Número de empresas cliente (Nc)
- Número de líneas (Nl)
- Tiempo por llamada (Tpll)
- Ancho de banda de reserva (BWres)
- Tipo de encapsulacion utilizada (Ethernet, Ethernet 802.1q, Ethernet q-in-q, PPPOE, PPPOE 802.1q)
- Se considerará el caso peor en cuanto a la probabilidad de que una línea realice una llamada durante la hora cargada

### QoE:

- Mean Opinion Score (MOS)

### QoS:

- Retardo total (Rt)
- Retardo de red (Rr)
- Jitter (J)
- Se considera el uso de RTP o cRTP
- Se considera sólo los retardos por Codecs, paquetización, buffer anti-jitter. Considere
un 10% el tiempo de compresión y de decompresión

### GoS:

- Probabilidad de bloqueo (Pb)

### Ancho de banda:

- Ancho de Banda SIPTRUNK (BWst)
