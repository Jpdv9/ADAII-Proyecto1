import math

def modciV(red_social):

    n = len(red_social.grupos)
    estrategia = [0] * n
    esfuerzo_total = 0

    
    # Calcular Ganancia
    ganancias = []
    i = 0
    while i < len(red_social.grupos):
        grupo = red_social.grupos[i]

        if grupo.n > 0:
            beneficio = abs(grupo.op1 - grupo.op2) * grupo.rig
            costo = math.ceil(beneficio) 

            if costo > 0:
             ganancias.append((beneficio / costo, i, beneficio, costo))
        i += 1

    # Ordenaos ganancia/efuerzo
    ganancias.sort(reverse=True)

    for ganancia_unidad, i, beneficio, costo in ganancias:
        grupo = red_social.grupos[i]

        for k in range(1, grupo.n + 1):
            incremento_esfuerzo = math.ceil(abs(grupo.op1 - grupo.op2) * grupo.rig * k)
            
            if esfuerzo_total + incremento_esfuerzo <= red_social.R_max:
                estrategia[i] = k
                esfuerzo_total += incremento_esfuerzo
            else:
                break 

    
    nueva_red = red_social.aplicar_estrategia(estrategia)
    
    conflicto = nueva_red.calcular_conflicto_interno()
    return (estrategia, esfuerzo_total, conflicto)
