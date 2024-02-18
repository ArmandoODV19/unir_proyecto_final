### script de trabajo

# leyendo el archivo y almacenándolo en df
# Especifica el parámetro quotechar para evitar que las comillas sean tratadas como delimitadores
df = pd.read_csv("/datasets/20240103_PLCCupMachineL4.csv", sep="[|,]", quotechar='"')

df = pd.read_csv("/datasets/20240103_PLCCupMachineL4.csv", sep="[|,]", quotechar='"')
    
# Elimina las comillas de los nombres de las columnas
df.columns = df.columns.str.strip('"') 

df.info()

# Convertir la columna 'RegDate' a tipo de datos de fecha y hora
df['RegDate'] = pd.to_datetime(df['RegDate'])

# Formatear la columna 'RegDate' según el formato deseado
df['RegDate'] = df['RegDate'].dt.strftime('%d/%m/%Y %I:%M:%S %p')

print(df.columns)

# Define una función para convertir a minúsculas
def convertir_a_minusculas(columna):
    return columna.lower()
# Aplica la función de conversión a minúsculas a los nombres de las columnas
df.rename(columns=convertir_a_minusculas, inplace=True)
# comprobando el resultado: la lista de los nombres de las columnas
print(df.columns)

# calculando valores ausentes
print(df.isna().sum())

# contando duplicado 
print(df.duplicated().sum())

# eliminando duplicados
df = df.reset_index(drop=True) 

# inspeccionando los nombres de productype
df_date = df['regdate'].describe()
print(df_date)

# inspeccionando los nombres de productype
df_type = df['producttype'].unique()
df_type.sort()
print(df_type)

# Contar el numero de productos generados
conteo_productos = df.groupby('producttype').size().reset_index(name='Count')print(conteo_productos)
# Analizar la distribución de categorías en variables categóricas
sns.countplot(x='producttype', data=df)
plt.title('Distribución de Tipos de Producto')
plt.xticks(rotation=45)
plt.show()

# Visualizar la distribución de algunas variables numéricas
sns.histplot(df['shootxmin'], bins=20, kde=True)
plt.title('Distribución de Disparos por Minuto')
plt.show()

sns.histplot(df['itemxmin'], bins=20, kde=True)
plt.title('Distribución de Cantidad de Productos por Minuto')
plt.show()

# Explorar la correlación entre variables numéricas
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Matriz de Correlación')
plt.show()

# Explorar la relación entre variables utilizando un gráfico de dispersión
sns.scatterplot(x='shootxmin', y='itemxmin', data=df)
plt.title('Relación entre Disparos por Minuto y Cantidad de Productos por Minuto')
plt.show()

# Cambiar el formato de la fecha
df['date'] = pd.to_datetime(df['date'], format="%d/%m/%Y")
# Group by 'date' and calculate max(itemxmin)
summary_result = df.groupby('date').agg(maximo=('itemxmin', 'max')).reset_index()

# Ordenar por fecha
summary_result = summary_result.sort_values(by='date')

# graficando
plt.plot(summary_result['date'], summary_result['maximo'])
plt.xlabel('Fecha')
plt.ylabel('ItemxMin')
plt.show()

# Calcular media, mediana, desviacion, varianza
summary_statistics = summary_result.agg(media=('maximo', 'mean'),
                                        mediana=('maximo', 'median'),
                                        desviacion=('maximo', 'std'),
                                        varianza=('maximo', 'var')).reset_index()
print(summary_statistics)

# Group by 'date' and calculate max(caminspection)
summary_result = df.groupby('date').agg(maximo=('ItemxMin', 'max')).reset_index()

# Ordenar por fecha
summary_result = summary_result.sort_values(by='date')

# graficando
plt.plot(summary_result['date'], summary_result['maximo'])
plt.xlabel('Fecha')
plt.ylabel('CamInspection')
plt.show()

# Calcular media, mediana, desviacion, varianza
summary_statistics = summary_result.agg(media=('maximo', 'mean'),
                                        mediana=('maximo', 'median'),
                                        desviacion=('maximo', 'std'),
                                        varianza=('maximo', 'var')).reset_index()
print(summary_statistics)

# Group by 'date' and calculate max(suctiontap)
summary_result = df.groupby('date').agg(maximo=(suctiontap', 'max')).reset_index()

# Ordenar por fecha
summary_result = summary_result.sort_values(by='date')

# graficando
plt.plot(summary_result['date'], summary_result['maximo'])
plt.xlabel('Fecha')
plt.ylabel('suctiontap')
plt.show()

# Calcular media, mediana, desviacion, varianza
summary_statistics = summary_result.agg(media=('maximo', 'mean'),
                                        mediana=('maximo', 'median'),
                                        desviacion=('maximo', 'std'),
                                        varianza=('maximo', 'var')).reset_index()

print(summary_statistics)

df_diablo = nissin[nissin['ProductType'] == 'DIABLO']
df_camaron = nissin[nissin['ProductType'] == 'HS CAMARON']

# Seleccionando variables de trabajo
df_camaron_variables = df_camaron[['CamInspection', 'suctionTap', 'StopBlock', 
                                                                     'StampVerification', 'InterferenceError', 'ErrorCalentador', 
                                                                     'OkProduction']]

# Calcular matriz de correlacion
correlaciones_camaron = df_camaron_variables.corr()

# Graficar matriz de correlacion
plt.figure(figsize=(10, 8))
sns.set(style="white")  
sns.heatmap(correlaciones_camaron, annot=True, cmap="coolwarm", linewidths=.5)
plt.show()

# Generando modelo de regresión

X = df_camaron_variables.drop('OkProduction', axis=1)
y = df_camaron_variables['OkProduction']

X = sm.add_constant(X)
modelo_lineal_camaron = sm.OLS(y, X).fit()
print(modelo_lineal_camaron.summary())
print(modelo_lineal_camaron.conf_int())

# Seleccionando variables de trabajo
df_diablo_variables = df_diablo[['CamInspection', 'suctionTap', 'StopBlock', 
                                                                     'StampVerification', 'InterferenceError', 'ErrorCalentador', 
                                                                     'OkProduction']]

# Calcular matriz de correlacion
correlaciones_diablo = df_diablo_variables.corr()

# Graficar matriz de correlacion
plt.figure(figsize=(10, 8))
sns.set(style="white")  
sns.heatmap(correlaciones_diablo, annot=True, cmap="coolwarm", linewidths=.5)
plt.show()

# Generando modelo de regresión
X = df_diablo_variables.drop('OkProduction', axis=1)
y = df_diablo_variables['OkProduction']
X = sm.add_constant(X)
modelo_lineal_diablo = sm.OLS(y, X).fit()
print(modelo_lineal_diablo.summary())
print(modelo_lineal_diablo.conf_int())

# Seleccionando variables de interes
df_camaron_prediccion = df_camaron[['CamInspection', 'StampVerification', 'InterferenceError', 'OkProduction']]
# Dividiendo el conjunto de datos
train_camaron, test_camaron = train_test_split(df_camaron_prediccion, test_size=0.2, random_state=42)

# Definiendo variables
X_train = train_camaron.drop('OkProduction', axis=1)
y_train = train_camaron['OkProduction']
# Generar modelo
X_train = sm.add_constant(X_train)
# Entrenando modelo
modelo_entrenamiento_camaron = sm.OLS(y_train, X_train).fit()
# Resumen de modelo
print(modelo_entrenamiento_camaron.summary())
# Realizar evaluación con datos de prueba
X_test = test_camaron.drop('OkProduction', axis=1)
y_test = test_camaron['OkProduction']
X_test = sm.add_constant(X_test)
# realizando predicción
pred_camaron = modelo_entrenamiento_camaron.predict(X_test)

# Evaluando el modelo
rmse_val = np.sqrt(mean_squared_error(y_test, pred_camaron))
print(f"RMSE: {rmse_val}")
r2_test = r2_score(y_test, pred_camaron)
print(f"R-squared: {r2_test}")

# Seleccionando variables de interes
df_diablo_prediccion = df_diablo[['suctionTap', 'StampVerification', 'OkProduction']]
# Dividiendo el conjunto de datos
train_diablo, test_diablo = train_test_split(df_diablo_prediccion, test_size=0.2, random_state=42)

# Definiendo variables
X_train = train_diablo.drop('OkProduction', axis=1)
y_train = train_diablo['OkProduction']
# Generar modelo
X_train = sm.add_constant(X_train)
# Entrenando modelo
modelo_entrenamiento_diablo = sm.OLS(y_train, X_train).fit()
# Resumen de modelo
print(modelo_entrenamiento_diablo.summary())



