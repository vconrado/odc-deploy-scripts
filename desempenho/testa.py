from desempenho import *
import  sys


options = {
            "cubo1": [8, 8, False, None, 16],
            "cubo2": [8, 8, False, ("2017-01-01", "2017-10-30"), 16],
            "scene1": [8, 8, False, "2017-01-13", 16],
            "scene2": [16, 16, False, "2017-01-13", 16],
            "ts1": [8, 8, True, None, 16],
            "ts2": [8, 8, True, ("2017-01-01", "2017-10-30"), 16]
}

columns = ["count", "prod", "data_loaded_B", "dif_time", "MB_s", "x_size", "y_size", "time_size", "x0", "xf", "y0", "yf"]


if len(sys.argv) < 3:
    print("Usage: {} label product_name teste_name".format(sys.argv[0]))
    print("Opções:")
    for op in options:
        print("\t{}".format(op))
    exit(1)

label = sys.argv[1]
product = sys.argv[2]
teste = sys.argv[3]

if teste not in options:
    print("A opção {} é invalida.".format(teste))
    exit(1)

print("Opção selecionada: {}".format(teste))

params = options[teste]

print("Parametros selecionados: ")
print("\tTest name: {}".format(teste))
print("\tX-Steps: {}".format(params[0]))
print("\tY-Steps: {}".format(params[1]))
print("\tTimeSeries: {}".format("True" if params[2] else "False"))
print("\tTime List: {}".format(params[3] if params[3] else "All"))
print("\tMaximo: {}".format(params[4] if params[4] else "Inf"))


print("Testando {}.{}.{}".format(label, product, teste))

gdf = test_func(teste, product, *params)
    
save_gdf(gdf, product, label,  teste, columns)
print("Done", sys.argv)

with open("/dados/")
