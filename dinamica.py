# Importa el módulo math para usar funciones matemáticas como ceil (redondeo hacia arriba)
import math

# Define la función principal que resuelve el problema usando programación dinámica
def modciPD(red_social):
    # Obtiene el número de grupos en la red social
    n = len(red_social.grupos)
    # Obtiene el esfuerzo máximo disponible para moderar opiniones
    R_max = red_social.R_max

    # Crea una matriz dp donde dp[i][r] representa el menor conflicto posible 
    # usando los primeros i grupos con r unidades de esfuerzo
    dp = [[float('inf')] * (R_max + 1) for _ in range(n + 1)]
    
    # Crea una matriz decision que guarda cuántos agentes fueron moderados 
    # en cada estado para reconstruir la estrategia al final
    decision = [[-1] * (R_max + 1) for _ in range(n + 1)]

    # Caso base: con 0 grupos y 0 esfuerzo, el conflicto es 0
    dp[0][0] = 0

    # Itera sobre cada grupo (desde el primero hasta el último)
    for i in range(1, n + 1):
        # Toma el grupo actual (ajustando el índice porque dp empieza desde 1)
        grupo = red_social.grupos[i - 1]

        # Itera sobre cada posible cantidad de esfuerzo disponible
        for r in range(R_max + 1):

            # Prueba todas las cantidades posibles de agentes a moderar en este grupo
            for moderados in range(grupo.n + 1):
                # Calcula el esfuerzo requerido para moderar esta cantidad de agentes
                esfuerzo_moderacion = math.ceil(abs(grupo.op1 - grupo.op2) * grupo.rig * moderados)

                # Solo procede si el esfuerzo requerido no supera el disponible
                if esfuerzo_moderacion <= r:
                    # Calcula cuántos agentes quedan sin moderar en el grupo
                    agentes_no_moderados = grupo.n - moderados
                    
                    # Calcula el conflicto que generan los agentes no moderados
                    conflicto_actual = agentes_no_moderados * (grupo.op1 - grupo.op2) ** 2
                    
                    # Suma el conflicto actual con el conflicto mínimo de los grupos anteriores
                    total_conflicto = dp[i - 1][r - esfuerzo_moderacion] + conflicto_actual

                    # Si esta estrategia mejora el conflicto mínimo conocido, la guarda
                    if total_conflicto < dp[i][r]:
                        dp[i][r] = total_conflicto
                        decision[i][r] = moderados

    # Inicializa variables para guardar la mejor estrategia encontrada
    mejor_conflicto = float('inf')  # el menor conflicto encontrado
    mejor_estrategia = [0] * n      # cuántos agentes moderar en cada grupo
    mejor_esfuerzo = 0              # cuánto esfuerzo total se usó

    # Busca entre todos los posibles esfuerzos el que logre el menor conflicto final
    for r in range(R_max + 1):
        if dp[n][r] < mejor_conflicto:
            mejor_conflicto = dp[n][r]
            mejor_esfuerzo = r

    # Reconstruye la estrategia óptima recorriendo la matriz hacia atrás
    r = mejor_esfuerzo
    for i in range(n, 0, -1):
        # Recupera cuántos agentes fueron moderados en el grupo i-1
        moderados = decision[i][r]
        
        # Guarda esta decisión en la estrategia
        mejor_estrategia[i - 1] = moderados

        # Resta el esfuerzo que se usó en este grupo para retroceder correctamente
        esfuerzo_moderacion = math.ceil(
            abs(red_social.grupos[i - 1].op1 - red_social.grupos[i - 1].op2) *
            red_social.grupos[i - 1].rig * moderados
        )
        r -= esfuerzo_moderacion

    # Calcula el conflicto interno promedio (dividiendo entre el número de grupos)
    mejor_conflicto = dp[n][mejor_esfuerzo] / n

    # Devuelve una tupla con la estrategia óptima, el esfuerzo total y el conflicto interno final
    return (mejor_estrategia, mejor_esfuerzo, mejor_conflicto)
