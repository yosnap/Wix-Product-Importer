# Una ves generado el CSV

1. Importar el CSV generado en GoogleSheets
2. Crear la colulmna para la imagen destacada y extraer la primera imagen de la columna de la galería con la fórmula: =INDEX(SPLIT(G2; ";"); 1)
3. Copiar y pegar los datos de la imagen destacada como valores
4. Mover los IDs padres de las variaciones a nueva columna "Parent Temporal" usando la fórmula: =IF(C2="Variant"; A2; "")
5. Copiar y pegar los datos del Parent SKU como valores
6. Agrega una columna auxiliar (por ejemplo, columna E).

En la celda E2, escribe la siguiente fórmula para verificar si la columna "Variaciones" (por ejemplo, columna D) tiene más de un valor: =IF(AND(C2="Product", LEN(D2) - LEN(SUBSTITUTE(D2, ";", "")) > 0), "Variable", C2)
