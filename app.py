import pandas as pd
from flask import Flask, render_template_string

app = Flask(__name__)

# Leer el archivo CSV
df = pd.read_csv('catalog_products-15-10-2024.csv')

# Renombrar las columnas
df = df.rename(columns={'handleId': 'ID', 'fieldType': 'Type', 'productOptionDescription1': 'variaciones'})

# Ordenar el DataFrame por 'ID' y luego por 'Type' para asegurar que 'Product' aparezca antes que 'Variant'
df = df.sort_values(by=['ID', 'Type', 'productOptionType1'], ascending=[True, True, True])

# Guardar el DataFrame modificado en un nuevo archivo CSV
df.to_csv('catalog_products_modified.csv', index=False)

# Cambiar el Type a 'Variable' solo para los productos que comparten el mismo ID con algún 'Variant'
df.loc[(df['ID'].isin(df[df['Type'] == 'Variant']['ID'])) & (df['Type'] == 'Product'), 'Type'] = 'Variable'

# Crear filas para las variaciones
new_rows = []
for index, row in df.iterrows():
    if row['Type'] == 'Product' and pd.notna(row['variaciones']):
        variaciones = row['variaciones'].split(';')
        if len(variaciones) > 1:
            for variacion in variaciones:
                new_row = row.copy()
                new_row['Type'] = 'Variant'
                new_row['variaciones'] = variacion.strip()
                new_row['name'] = None  # Eliminar el valor de 'name' en las variantes
                new_row['productOptionType1'] = None  # Eliminar el valor de 'productOptionType1' en las variantes
                new_row['description'] = None  # Eliminar el valor de 'description' en las variantes
                new_row['productImageUrl'] = None  # Eliminar el valor de 'productImageUrl' en las variantes
                new_row['collection'] = None  # Eliminar el valor de 'collection' en las variantes
                new_row['price'] = None  # Eliminar el valor de 'price' en las variantes
                new_rows.append((index, new_row))

# Insertar las nuevas filas debajo de su producto padre
for index, new_row in sorted(new_rows, key=lambda x: x[0], reverse=True):
    df = pd.concat([df.iloc[:index + 1], pd.DataFrame([new_row]), df.iloc[index + 1:]]).reset_index(drop=True)

# Ordenar el DataFrame para que los productos y sus variantes estén juntos
df = df.sort_values(by=['ID', 'Type'], ascending=[True, True])

# Mostrar todas las columnas
df_hidden = df

# Función para aplicar estilos condicionales
def highlight_products(row):
    if row['Type'] == 'Variable':
        return ['background-color: lightyellow'] * len(row)
    return [''] * len(row)

# Aplicar estilos condicionales
styled_df = df_hidden.style.apply(highlight_products, axis=1)

# Convertir el DataFrame a HTML con estilos
table_html = styled_df.to_html()

# Definir la plantilla HTML
html_template = '''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
    <title>CSV Viewer</title>
    <style>
      .table-responsive {
        position: relative;
        width: 100%;
        padding-left: 100px;
        padding-right: 100px;
      }
      .table-responsive thead th {
        position: sticky;
        top: 0;
        background-color: white;
        z-index: 1;
      }
      .table td, .table th {
        padding: 0.25rem;
      }
    </style>
  </head>
  <body>
    <div class="container-fluid">
      <h1 class="mt-5">CSV Viewer</h1>
      <div class="table-responsive">
        {{ table_html | safe }}
      </div>
    </div>
  </body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(html_template, table_html=table_html)

if __name__ == '__main__':
    app.run(debug=True)