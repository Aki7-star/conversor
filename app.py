from flask import Flask, request, jsonify, render_template_string
from decimal import Decimal, getcontext
from waitress import serve

app = Flask(__name__)

getcontext().prec = 100000000  # Puedes aumentar la precisión

# Funciones de conversión (ya existentes)
def convertir_longitud(valor, unidad_origen, unidad_destino):
    unidades_a_metros = {
        'nm': Decimal ('1e-9'), 'µm': Decimal ('1e-6'), 'mm': Decimal ('0.001'), 
        'cm': Decimal ('0.01'), 'dm': Decimal ('0.1'), 'm': Decimal ('1'),
        'dam': Decimal ('10'), 'hm': Decimal ('100'), 'km': Decimal ('1000'), 
        'Mm': Decimal ('1e6'), 'Gm': Decimal ('1e9'), 'UA': Decimal ('149597870700'),
        'ly': Decimal ('9.461e15'), 'pc': Decimal ('3.086e16'), 'in': Decimal ('0.0254'), 
        'ft': Decimal ('0.3048'), 'yd': Decimal ('0.9144'), 'mi': Decimal ('1609.34')
    }
    valor = Decimal(str(valor))
    valor_metros = valor * unidades_a_metros[unidad_origen]
    return str(valor_metros / unidades_a_metros[unidad_destino])

def convertir_masa(valor, unidad_origen, unidad_destino):
    unidades_a_gramos = {
        'ng': Decimal ('1e-9'), 'µg': Decimal ('1e-6'), 'mg': Decimal ('0.001'), 
        'cg': Decimal ('0.01'), 'dg': Decimal ('0.1'), 'g': Decimal ('1'),
        'dag': Decimal ('10'), 'hg': Decimal ('100'), 'kg': Decimal ('1000'), 
        't': Decimal ('1e6'), 'oz': Decimal ('28.3495'), 'lb': Decimal ('453.592'),
        'st': Decimal ('6350.29318'), 'ton': Decimal ('907184.74')
    }
    valor = Decimal(str(valor))
    valor_gramos = valor * unidades_a_gramos[unidad_origen]
    return str(valor_gramos / unidades_a_gramos[unidad_destino])

def convertir_temperatura(valor, unidad_origen, unidad_destino):
    if unidad_origen == unidad_destino:
        return valor
    if unidad_origen == 'C':
        if unidad_destino == 'F':
            return valor * 9/5 + 32
        elif unidad_destino == 'K':
            return valor + 273.15
    if unidad_origen == 'F':
        if unidad_destino == 'C':
            return (valor - 32) * 5/9
        elif unidad_destino == 'K':
            return (valor - 32) * 5/9 + 273.15
    if unidad_origen == 'K':
        if unidad_destino == 'C':
            return valor - 273.15
        elif unidad_destino == 'F':
            return (valor - 273.15) * 9/5 + 32

def convertir_volumen(valor, unidad_origen, unidad_destino):
    unidades_a_litros = {
        'nl': Decimal ('1e-9'), 'µl': Decimal ('1e-6'), 'ml': Decimal ('0.001'), 
        'cl': Decimal ('0.01'), 'dl': Decimal ('0.1'), 'l': Decimal ('1'),
        'dal': Decimal ('10'), 'hl': Decimal ('100'), 'kl': Decimal ('1000'), 
        'Ml': Decimal ('1e6'), 'Gl': Decimal ('1e9'), 'nm3': Decimal ('1e-9'), 
        'µm3': Decimal ('1e-6'), 'mm3': Decimal ('1e-3'),'cm3': Decimal ('0.001'),
        'dm3': Decimal ('1'), 'm3': Decimal ('1000'), 'gal': Decimal ('3.78541'), 
        'pt': Decimal ('0.473176'), 'qt': Decimal ('0.946353')
    }
    valor = Decimal(str(valor))
    valor_litros = valor * unidades_a_litros[unidad_origen]
    return str(valor_litros / unidades_a_litros[unidad_destino])

def convertir_tiempo(valor, unidad_origen, unidad_destino):
    unidades_a_segundos = {
        'ns': Decimal ('1e-9'), 'µs': Decimal ('1e-6'), 'ms': Decimal ('0.001'), 
        's': Decimal ('1'), 'min': Decimal ('60'), 'h': Decimal ('3600'),
        'd': Decimal ('86400'), 'sem': Decimal ('604800'), 'mes': Decimal ('2592000'), 
        'año': Decimal ('31536000'), 'decada': Decimal ('315360000'), 'siglo': Decimal ('3153600000'), 
        'milenio': Decimal ('31536000000')
    }
    valor = Decimal(str(valor))
    valor_segundos = valor * unidades_a_segundos[unidad_origen]
    return str(valor_segundos / unidades_a_segundos[unidad_destino])

def convertir_velocidad(valor, unidad_origen, unidad_destino):
    unidades_a_metros_por_segundo = {
        'm/s': Decimal ('1'), 'km/h': Decimal ('0.278'), 'nudos': Decimal ('0.514'), 
        'ft/s': Decimal ('0.3048'), 'km/s': Decimal ('1000')
    }
    valor = Decimal(str(valor))
    valor_metros_por_segundo = valor * unidades_a_metros_por_segundo[unidad_origen]
    return str(valor_metros_por_segundo / unidades_a_metros_por_segundo[unidad_destino])

def convertir_datos(valor, unidad_origen, unidad_destino):
    unidades_a_bits = {
        'b': Decimal ('1'), 
        'B': Decimal ('8'), 
        'kb': Decimal ('1000'),
        'kB': Decimal ('8000'),
        'Mb': Decimal ('1000000'), 
        'MB': Decimal ('8000000'),
        'Gb': Decimal ('1000000000'),
        'GB': Decimal ('8000000000'),
        'Tb': Decimal ('1000000000000'),
        'TB': Decimal ('8000000000000'),
        'Pb': Decimal ('1000000000000000'),
        'PB': Decimal ('8000000000000000'),
        'Eb': Decimal ('1000000000000000000'),
        'EB': Decimal ('8000000000000000000'),
        'Zb': Decimal ('1000000000000000000000'),
        'ZB': Decimal ('8000000000000000000000'),
        'Yb': Decimal ('1000000000000000000000000'),
        'YB': Decimal ('8000000000000000000000000'),
        'Rb': Decimal ('1000000000000000000000000000'),
        'RB': Decimal ('8000000000000000000000000000'),
        'Qb': Decimal ('1000000000000000000000000000000'),
        'QB': Decimal ('8000000000000000000000000000000')
    }
    valor = Decimal(str(valor))
    valor_bits = valor * unidades_a_bits[unidad_origen]
    return str(valor_bits / unidades_a_bits[unidad_destino])

def convertir_energía(valor, unidad_origen, unidad_destino):
    unidades_a_julios = {
        'J': Decimal ('1'), 'KJ': Decimal ('1000'), 'cal': Decimal ('4.4184'), 
        'Kcal': Decimal ('4184'), 'Wh': Decimal ('3600'), 'KWh': Decimal ('3600000'),
        'eV': Decimal ('1.60218e-19'), 'BTU': Decimal ('1055.06'), 'erg': Decimal ('1e-7')
    }
    valor = Decimal(str(valor))
    valor_julios =  valor * unidades_a_julios[unidad_origen]
    return str(valor_julios / unidades_a_julios[unidad_destino])

def convertir_fuerza(valor, unidad_origen, unidad_destino):
    unidades_a_newtons = {
        'N': Decimal ('1'), 'KN': Decimal ('1000'), 'dyn': Decimal ('1e-5'), 
        'lbf': Decimal ('4.44822'), 'Kgf': Decimal ('9.80665')
    }
    valor = Decimal(str(valor))
    valor_newtons =  valor * unidades_a_newtons[unidad_origen]
    return str(valor_newtons / unidades_a_newtons[unidad_destino])

def convertir_area(valor, unidad_origen, unidad_destino):
    unidades_a_metros_cuadrados = {
        'nm2': Decimal ('1e-18'), 'µm2': Decimal ('1e-12'), 'mm2': Decimal ('1e-6'), 
        'cm2': Decimal ('1e-4'), 'dm2': Decimal ('0.01'), 'm2': Decimal ('1'), 
        'dam2': Decimal ('100'), 'hm2': Decimal ('10000'), 'km2': Decimal ('1e6'), 
        'Mm2': Decimal ('1e12'), 'Gm2': Decimal ('1e18'), 'UA2': Decimal ('2.29568e22'), 
        'in2': Decimal ('0.00064516'), 'ft2': Decimal ('0.092903'), 'yd2': Decimal ('0.836127'), 
        'mi2': Decimal ('2589988.11'), 'ac': Decimal ('4046.86'), 'ly2': Decimal ('8.467e31'), 
        'pc2': Decimal ('9.869e34'), 'ha': Decimal ('10000') 
    }
    valor = Decimal(str(valor))
    valor_metros_cuadrados = valor * unidades_a_metros_cuadrados[unidad_origen]
    return str(valor_metros_cuadrados / unidades_a_metros_cuadrados[unidad_destino])

def convertir_presión(valor, unidad_origen, unidad_destino):
    unidades_a_pascales = {
        'mmH2O': Decimal ('9.80665'), 'Torr': Decimal ('133.322'), 'hPa': Decimal ('100'),
        'mbar': Decimal ('100'), 'kPa': Decimal ('1000'), 'at': Decimal ('98066.5'),
        'atm': Decimal ('101325'), 'bar': Decimal ('100000'), 'MPa': Decimal ('1000000')
    }
    valor = Decimal(str(valor))
    valor_pascales = valor * unidades_a_pascales[unidad_origen]
    return str(valor_pascales / unidades_a_pascales[unidad_destino])

def convertir_tetravolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_cuarta = {
        'nm4': Decimal ('1e-36'), 'µm4': Decimal ('1e-24'), 'mm4': Decimal ('1e-12'), 
        'cm4': Decimal ('1e-8'), 'dm4': Decimal ('1e-4'), 'm4': Decimal ('1'), 
        'dam4': Decimal ('1e4'), 'hm4': Decimal ('1e8'), 'km4': Decimal ('1e12'), 
        'Mm4': Decimal ('1e24'), 'Gm4': Decimal ('1e36'), 'UA4': Decimal ('5.229e44')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_cuarta = valor * unidades_a_metros_a_la_cuarta[unidad_origen]
    return str(valor_metros_a_la_cuarta / unidades_a_metros_a_la_cuarta[unidad_destino])

def convertir_pentavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_quinta = {
        'nm5': Decimal ('1e-45'), 'µm5': Decimal ('1e-30'), 'mm5': Decimal ('1e-15'), 
        'cm5': Decimal ('1e-10'), 'dm5': Decimal ('1e-5'), 'm5': Decimal ('1'), 
        'dam5': Decimal ('1e5'),'hm5': Decimal ('1e10'), 'km5': Decimal ('1e15'), 
        'Mm5': Decimal ('1e30'), 'Gm5': Decimal ('1e45'), 'UA5': Decimal ('7.812e55')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_quinta = valor * unidades_a_metros_a_la_quinta[unidad_origen]
    return str(valor_metros_a_la_quinta / unidades_a_metros_a_la_quinta[unidad_destino])

def convertir_hexavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_sexta = {
        'nm6': Decimal ('1e-54'), 'µm6': Decimal ('1e-36'), 'mm6': Decimal ('1e-18'), 
        'cm6': Decimal ('1e-12'), 'dm6': Decimal ('1e-6'), 'm6': Decimal ('1'), 
        'dam6': Decimal ('1e6'), 'hm6': Decimal ('1e12'), 'km6': Decimal ('1e18'), 
        'Mm6': Decimal ('1e36'), 'Gm6': Decimal ('1e54'), 'UA6': Decimal ('1.5625e66')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_sexta = valor * unidades_a_metros_a_la_sexta[unidad_origen]
    return str(valor_metros_a_la_sexta / unidades_a_metros_a_la_sexta[unidad_destino])

def convertir_heptavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_septima = {
        'nm7': Decimal ('1e-63'), 'µm7': Decimal ('1e-42'), 'mm7': Decimal ('1e-21'), 
        'cm7': Decimal ('1e-14'), 'dm7': Decimal ('1e-7'), 'm7': Decimal ('1'), 
        'dam7': Decimal ('1e7'), 'hm7': Decimal ('1e14'), 'km7': Decimal ('1e21'), 
        'Mm7': Decimal ('1e42'), 'Gm7': Decimal ('1e63'), 'UA7': Decimal ('2.4414e77')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_septima = valor * unidades_a_metros_a_la_septima[unidad_origen]
    return str(valor_metros_a_la_septima / unidades_a_metros_a_la_septima[unidad_destino])

def convertir_octavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_octava = {
        'nm8': Decimal ('1e-72'), 'µm8': Decimal ('1e-48'), 'mm8': Decimal ('1e-24'), 
        'cm8': Decimal ('1e-16'), 'dm8': Decimal ('1e-8'), 'm8': Decimal ('1'), 
        'dam8': Decimal ('1e8'), 'hm8': Decimal ('1e16'), 'km8': Decimal ('1e24'), 
        'Mm8': Decimal ('1e48'), 'Gm8': Decimal ('1e72'), 'UA8': Decimal ('3.8147e88')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_octava = valor * unidades_a_metros_a_la_octava[unidad_origen]
    return str(valor_metros_a_la_octava / unidades_a_metros_a_la_octava[unidad_destino])

def convertir_nonavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_novena = {
        'nm9': Decimal ('1e-81'), 'µm9': Decimal ('1e-54'), 'mm9': Decimal ('1e-27'), 
        'cm9': Decimal ('1e-18'), 'dm9': Decimal ('1e-9'), 'm9': Decimal ('1'), 
        'dam9': Decimal ('1e9'), 'hm9': Decimal ('1e18'), 'km9': Decimal ('1e27'), 
        'Mm9': Decimal ('1e54'), 'Gm9': Decimal ('1e81'), 'UA9': Decimal ('7.6294e99')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_novena = valor * unidades_a_metros_a_la_novena[unidad_origen]
    return str(valor_metros_a_la_novena / unidades_a_metros_a_la_novena[unidad_destino])

def convertir_decavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decima = {
        'nm10': Decimal ('1e-90'),  'µm10': Decimal ('1e-60'), 'mm10': Decimal ('1e-30'), 
        'cm10': Decimal ('1e-20'), 'dm10': Decimal ('1e-10'), 'm10': Decimal ('1'), 
        'dam10': Decimal ('1e10'), 'hm10': Decimal ('1e20'), 'km10': Decimal ('1e30'), 
        'Mm10': Decimal ('1e60'), 'Gm10': Decimal ('1e90'), 'UA10': Decimal ('1.5259e110')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_decima = valor * unidades_a_metros_a_la_decima[unidad_origen]
    return str(valor_metros_a_la_decima / unidades_a_metros_a_la_decima[unidad_destino])

def convertir_undecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decimoprimera = {
        'nm11': Decimal ('1e-99'), 'µm11': Decimal ('1e-66'), 'mm11': Decimal ('1e-33'), 
        'cm11': Decimal ('1e-22'), 'dm11': Decimal ('1e-11'), 'm11': Decimal ('1'), 
        'dam11': Decimal ('1e11'), 'hm11': Decimal ('1e22'), 'km11': Decimal ('1e33'), 
        'Mm11': Decimal ('1e66'), 'Gm11': Decimal ('1e99'), 'UA11': Decimal ('3.0518e121')

    }
    valor = Decimal(str(valor))
    valor_metros_a_la_decimoprimera = valor * unidades_a_metros_a_la_decimoprimera[unidad_origen]
    return str(valor_metros_a_la_decimoprimera / unidades_a_metros_a_la_decimoprimera[unidad_destino])

def convertir_dodecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decimosegunda = {
        'nm12': Decimal ('1e-108'), 'µm12': Decimal ('1e-72'), 'mm12': Decimal ('1e-36'), 
        'cm12': Decimal ('1e-24'), 'dm12': Decimal ('1e-12'), 'm12': Decimal ('1'), 
        'dam12': Decimal ('1e12'), 'hm12': Decimal ('1e24'), 'km12': Decimal ('1e36'), 
        'Mm12': Decimal ('1e72'), 'Gm12': Decimal ('1e108'), 'UA12': Decimal ('6.1035e132')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_decimosegunda = valor * unidades_a_metros_a_la_decimosegunda[unidad_origen]
    return str(valor_metros_a_la_decimosegunda / unidades_a_metros_a_la_decimosegunda[unidad_destino])

def convertir_tridecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decimotercera = {
        'nm13': Decimal ('1e-117'), 'µm13': Decimal ('1e-78'), 'mm13': Decimal ('1e-39'), 
        'cm13': Decimal ('1e-26'), 'dm13': Decimal ('1e-13'), 'm13': Decimal ('1'), 
        'dam13': Decimal ('1e13'), 'hm13': Decimal ('1e26'), 'km13': Decimal ('1e39'), 
        'Mm13': Decimal ('1e78'), 'Gm13': Decimal ('1e117'), 'UA13': Decimal ('1.2207e143')
    }
    valor = Decimal(str(valor)) 
    valor_metros_a_la_decimotercera = valor * unidades_a_metros_a_la_decimotercera[unidad_origen]
    return str(valor_metros_a_la_decimotercera / unidades_a_metros_a_la_decimotercera[unidad_destino])

def convertir_tetradecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decimocuarta = {
        'nm14': Decimal ('1e-126'), 'µm14': Decimal ('1e-84'), 'mm14': Decimal ('1e-42'), 
        'cm14': Decimal ('1e-28'), 'dm14': Decimal ('1e-14'), 'm14': Decimal ('1'), 
        'dam14': Decimal ('1e14'), 'hm14': Decimal ('1e28'), 'km14': Decimal ('1e42'), 
        'Mm14': Decimal ('1e84'), 'Gm14': Decimal ('1e126'), 'UA14': Decimal ('2.4414e154')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_decimocuarta = valor * unidades_a_metros_a_la_decimocuarta[unidad_origen]
    return str(valor_metros_a_la_decimocuarta / unidades_a_metros_a_la_decimocuarta[unidad_destino])

def convertir_pentadecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decimoquinta = {
        'nm15': Decimal ('1e-135'), 'µm15': Decimal ('1e-90'), 'mm15': Decimal ('1e-45'), 
        'cm15': Decimal ('1e-30'), 'dm15': Decimal ('1e-15'), 'm15': Decimal ('1'), 
        'dam15': Decimal ('1e15'), 'hm15': Decimal ('1e30'), 'km15': Decimal ('1e45'), 
        'Mm15': Decimal ('1e90'), 'Gm15': Decimal ('1e135'), 'UA15': Decimal  ('4.8828e165')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_decimoquinta = valor * unidades_a_metros_a_la_decimoquinta[unidad_origen]
    return str(valor_metros_a_la_decimoquinta / unidades_a_metros_a_la_decimoquinta[unidad_destino])

def convertir_hexadecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decimosexta = {
        'nm16': Decimal ('1e-144'), 'µm16': Decimal ('1e-96'), 'mm16': Decimal ('1e-48'), 
        'cm16': Decimal ('1e-32'), 'dm16': Decimal ('1e-16'), 'm16': Decimal ('1'), 
        'dam16': Decimal ('1e16'), 'hm16': Decimal ('1e32'), 'km16': Decimal ('1e48'), 
        'Mm16': Decimal ('1e96'), 'Gm16': Decimal ('1e144'), 'UA16': Decimal ('9.7656e176')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_decimosexta = valor * unidades_a_metros_a_la_decimosexta[unidad_origen]
    return str(valor_metros_a_la_decimosexta / unidades_a_metros_a_la_decimosexta[unidad_destino])

def convertir_heptadecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decimoséptima = {
        'nm17': Decimal ('1e-153'), 'µm17': Decimal ('1e-102'), 'mm17': Decimal ('1e-51'), 
        'cm17': Decimal ('1e-34'), 'dm17': Decimal ('1e-17'), 'm17': Decimal ('1'),
        'dam17': Decimal ('1e17'), 'hm17': Decimal ('1e34'), 'km17': Decimal ('1e51'),
        'Mm17': Decimal ('1e102'), 'Gm17': Decimal ('1e153'), 'UA17': Decimal ('1.9531e187')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_decimoséptima = valor * unidades_a_metros_a_la_decimoséptima[unidad_origen]
    return str(valor_metros_a_la_decimoséptima / unidades_a_metros_a_la_decimoséptima[unidad_destino])

def convertir_octadecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decimoctava = {
        'nm18': Decimal ('1e-162'), 'µm18': Decimal ('1e-108'), 'mm18': Decimal ('1e-54'),
        'cm18': Decimal ('1e-36'), 'dm18': Decimal ('1e-18'), 'm18': Decimal ('1'),
        'dam18': Decimal ('1e18'), 'hm18': Decimal ('1e36'), 'km18': Decimal ('1e54'),
        'Mm18': Decimal ('1e108'), 'Gm18': Decimal ('1e162'), 'UA18': Decimal ('3.9062e198')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_decimoctava = valor * unidades_a_metros_a_la_decimoctava[unidad_origen]
    return str(valor_metros_a_la_decimoctava / unidades_a_metros_a_la_decimoctava[unidad_destino])

def convertir_nonadecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_decimonovena = {
        'nm19': Decimal ('1e-171'), 'µm19': Decimal ('1e-114'), 'mm19': Decimal ('1e-57'),
        'cm19': Decimal ('1e-38'), 'dm19': Decimal ('1e-19'), 'm19': Decimal ('1'),
        'dam19': Decimal ('1e19'), 'hm19': Decimal ('1e38'), 'km19': Decimal ('1e57'),
        'Mm19': Decimal ('1e114'), 'Gm19': Decimal ('1e171'), 'UA19': Decimal ('7.8125e208')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_decimonovena = valor * unidades_a_metros_a_la_decimonovena[unidad_origen]
    return str(valor_metros_a_la_decimonovena / unidades_a_metros_a_la_decimonovena[unidad_destino])

def convertir_idecavolumen(valor, unidad_origen, unidad_destino):
    unidades_a_metros_a_la_vigésima = {
        'nm20': Decimal ('1e-180'), 'µm20': Decimal ('1e-120'), 'mm20': Decimal ('1e-60'),
        'cm20': Decimal ('1e-40'), 'dm20': Decimal ('1e-20'), 'm20': Decimal ('1'),
        'dam20': Decimal ('1e20'), 'hm20': Decimal ('1e40'), 'km20': Decimal ('1e60'),
        'Mm20': Decimal ('1e120'), 'Gm20': Decimal ('1e180'), 'UA20': Decimal ('1.5625e220')
    }
    valor = Decimal(str(valor))
    valor_metros_a_la_vigésima = valor * unidades_a_metros_a_la_vigésima[unidad_origen]
    return str(valor_metros_a_la_vigésima / unidades_a_metros_a_la_vigésima[unidad_destino])



@app.route("/")
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8" />
<title>Conversor de Unidades</title>
<style>
  body {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: linear-gradient(135deg, #43cea2 0%, #185a9d 100%);
    min-height: 100vh;
    margin: 0;
    padding: 0;
  }
  .container {
    background: rgba(255,255,255,0.95);
    max-width: 480px;
    margin: 40px auto 0 auto;
    padding: 32px 28px 24px 28px;
    border-radius: 18px;
    box-shadow: 0 8px 32px rgba(60,60,120,0.18);
    animation: fadein 1.2s;
  }
                                  
    h1 {
        text-align: center;
  } 
  label, select, input[type="number"], button {
    display: block;
    width: 80%;           
    margin-left: auto;    
    margin-right: auto;
    margin-bottom: 12px;
    box-sizing: border-box;
  }
  select, input[type="number"] {
    padding: 8px 10px;
    border-radius: 7px;
    border: 1px solid #bdbdbd;
    font-size: 1rem;
    background: #f7f7fa;
    transition: border 0.2s;
  }
  select:focus, input[type="number"]:focus {
    border: 1.5px solid #185a9d;
    outline: none;
  }
  button {
    width: 80%;
    background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
    color: #fff;
    border: none;
    border-radius: 7px;
    padding: 12px 0;
    font-size: 1.1rem;
    font-weight: bold;
    margin-top: 10px;
    cursor: pointer;
    box-shadow: 0 2px 8px rgba(100,100,180,0.10);
    transition: background 0.2s, transform 0.1s;
  }
  button:hover {
    background: linear-gradient(90deg, #43cea2 0%, #185a9d 100%);
    transform: scale(1.03);
  }
  #resultado {
    margin-top: 24px;
    background: #f3f0fa;
    color: #4b3fa7;
    border-radius: 10px;
    padding: 18px 12px;
    font-size: 1.15rem;
    min-height: 32px;
    box-shadow: 0 1px 8px rgba(120,80,200,0.07);
    word-break: break-all;
    white-space: pre-wrap;
    max-width: 100%;
    overflow-wrap: break-word;
    text-align: center;
    font-family: 'Fira Mono', 'Consolas', monospace;
    letter-spacing: 0.5px;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
  }
  .footer {
    text-align: center;
    color: #fff;
    margin-top: 40px;
    font-size: 0.98rem;
    opacity: 0.85;
    letter-spacing: 0.5px;
  }
  @media (max-width: 600px) {
    .container { padding: 16px 4vw; }
    h1 { font-size: 1.3rem; }
    #resultado { font-size: 1rem; }
  }
</style>
</head>
<body>
  <h1>Conversor de Unidades</h1>

  <label for="tipo">Tipo de conversión:</label>
  <select id="tipo" required>
    <option value="" disabled selected>Selecciona tipo</option>
    <option value="Longitud">Longitud</option>
    <option value="Masa">Masa</option>
    <option value="Temperatura">Temperatura</option>
    <option value="Volumen">Volumen</option>
    <option value="Tiempo">Tiempo</option>
    <option value="Velocidad">Velocidad</option>
    <option value="Datos">Datos</option>
    <option value="Energía">Energía</option>
    <option value="Fuerza">Fuerza</option>
    <option value="Área">Área</option>
    <option value="Presión">Presión</option>
    <option value="Tetravolumen">Tetravolumen</option>
    <option value="Pentavolumen">Pentavolumen</option>
    <option value="Hexavolumen">Hexavolumen</option>
    <option value="Heptavolumen">Heptavolumen</option>
    <option value="Octavolumen">Octavolumen</option>
    <option value="Nonavolumen">Nonavolumen</option>
    <option value="Decavolumen">Decavolumen</option>
    <option value="Undecavolumen">Undecavolumen</option>
    <option value="Dodecavolumen">Dodecavolumen</option>
    <option value="Tridecavolumen">Tridecavolumen</option>
    <option value="Tetradecavolumen">Tetradecavolumen</option>
    <option value="Pentadecavolumen">Pentadecavolumen</option>
    <option value="Hexadecavolumen">Hexadecavolumen</option>
    <option value="Heptadecavolumen">Heptadecavolumen</option>
    <option value="Octadecavolumen">Octadecavolumen</option>
    <option value="Nonadecavolumen">Nonadecavolumen</option>
    <option value="Idecavolumen">Idecavolumen</option>
    </select>

  <label for="valor">Valor:</label>
  <input type="number" id="valor" step="any" required />

  <label for="origen">Unidad origen:</label>
  <select id="origen" required></select>

  <label for="destino">Unidad destino:</label>
  <select id="destino" required></select>

  <button id="convertir">Convertir</button>

  <h2 id="resultado"></h2>

<script>
  const unidades = {
    "Longitud": ["nm", "µm", "mm", "cm", "dm", "m", "dam", "hm", "km", "Mm", "Gm", "UA", "ly", "pc", "in", "ft", "yd", "mi"],
    "Masa": ["ng", "µg", "mg", "cg", "dg", "g", "dag", "hg", "kg", "t", "oz", "lb", "st", "ton"],
    "Temperatura": ["C", "F", "K"],
    "Volumen": ["nl", "µl", "ml", "cl", "dl", "l", "dal", "hl", "kl", "Ml", "Gl", "nm3", "µm3", "mm3", "cm3", "dm3", "m3", "gal", "pt", "gt"],
    "Tiempo": ["ns", "µs", "ms", "s", "min", "h", "d", "sem", "mes", "año", "decada", "siglo", "milenio"],
    "Velocidad": ["m/s", "km/h", "nudos", "ft/s", "km/s"],
    "Datos": ["b","B", "kb", "kB", "Mb", "MB", "Gb", "GB", "Tb", "TB", "Pb", "PB", "Eb", "EB", "Zb", "ZB", "Yb", "YB", "Rb", "RB", "Qb", "QB"],
    "Energía": ["J", "KJ", "cal", "Kcal", "Wh", "KWh", "eV", "BUT", "erg"],
    "Fuerza": ["N", "KN", "dyn", "lbf", "Kgf"],
    "Área": ["nm2", "µm2", "mm2", "cm2", "dm2", "m2", "dam2", "hm2", "km2", "Mm2", "Gm2", "UA2", "ha", "ac", "mi2", "ft2", "yd2", "in2", "pc2", "ly2"],
    "Presión": ["mmH2O", "Torr", "hPa", "mbar", "kPa", "at", "atm", "bar", "MPa"],
    "Tetravolumen": ["nm4", "µm4", "mm4", "cm4", "dm4", "m4", "dam4", "hm4", "km4", "Mm4", "Gm4", "UA4"],
    "Pentavolumen": ["nm5", "µm5", "mm5", "cm5", "dm5", "m5", "dam5", "hm5", "km5", "Mm5", "Gm5", "UA5"],
    "Hexavolumen": ["nm6", "µm6", "mm6", "cm6", "dm6", "m6", "dam6", "hm6", "km6", "Mm6", "Gm6", "UA6"],
    "Heptavolumen": ["nm7", "µm7", "mm7", "cm7", "dm7", "m7", "dam7", "hm7", "km7", "Mm7", "Gm7", "UA7"],
    "Octavolumen": ["nm8", "µm8", "mm8", "cm8", "dm8", "m8", "dam8", "hm8", "km8", "Mm8", "Gm8", "UA8"],
    "Nonavolumen": ["nm9", "µm9", "mm9", "cm9", "dm9", "m9", "dam9", "hm9", "km9", "Mm9", "Gm9", "UA9"],
    "Decavolumen": ["nm10", "µm10", "mm10", "cm10", "dm10", "m10", "dam10", "hm10", "km10", "Mm10", "Gm10", "UA10"],
    "Undecavolumen": ["nm11", "µm11", "mm11", "cm11", "dm11", "m11", "dam11", "hm11", "km11", "Mm11", "Gm11", "UA11"],
    "Dodecavolumen": ["nm12", "µm12", "mm12", "cm12", "dm12", "m12", "dam12", "hm12", "km12", "Mm12", "Gm12", "UA12"],
    "Tridecavolumen": ["nm13", "µm13", "mm13", "cm13", "dm13", "m13", "dam13", "hm13", "km13", "Mm13", "Gm13", "UA13"],
    "Tetradecavolumen": ["nm14", "µm14", "mm14", "cm14", "dm14", "m14", "dam14", "hm14", "km14", "Mm14", "Gm14", "UA14"],
    "Pentadecavolumen": ["nm15", "µm15", "mm15", "cm15", "dm15", "m15", "dam15", "hm15", "km15", "Mm15", "Gm15", "UA15"],   
    "Hexadecavolumen": ["nm16", "µm16", "mm16", "cm16", "dm16", "m16", "dam16", "hm16", "km16", "Mm16", "Gm16", "UA16"],
    "Heptadecavolumen": ["nm17", "µm17", "mm17", "cm17", "dm17", "m17", "dam17", "hm17", "km17", "Mm17", "Gm17", "UA17"],
    "Octadecavolumen": ["nm18", "µm18", "mm18", "cm18", "dm18", "m18", "dam18", "hm18", "km18", "Mm18", "Gm18", "UA18"],  
    "Nonadecavolumen": ["nm19", "µm19", "mm19", "cm19", "dm19", "m19", "dam19", "hm19", "km19", "Mm19", "Gm19", "UA19"],
    "Idecavolumen": ["nm20", "µm20", "mm20", "cm20", "dm20", "m20", "dam20", "hm20", "km20", "Mm20", "Gm20", "UA20"]                
  };

  const tipoSelect = document.getElementById('tipo');
  const origenSelect = document.getElementById('origen');
  const destinoSelect = document.getElementById('destino');
  const valorInput = document.getElementById('valor');
  const resultado = document.getElementById('resultado');
  const btnConvertir = document.getElementById('convertir');

  tipoSelect.addEventListener('change', () => {
    const tipo = tipoSelect.value;
    origenSelect.innerHTML = '';
    destinoSelect.innerHTML = '';
    if (tipo in unidades) {
      unidades[tipo].forEach(u => {
        origenSelect.innerHTML += `<option value="${u}">${u}</option>`;
        destinoSelect.innerHTML += `<option value="${u}">${u}</option>`;
      });
    }
  });

  btnConvertir.addEventListener('click', async () => {
    const valor = parseFloat(valorInput.value);
    if (isNaN(valor)) {
      alert('Ingresa un valor numérico válido');
      return;
    }
    const tipo = tipoSelect.value;
    const unidad_origen = origenSelect.value;
    const unidad_destino = destinoSelect.value;

    if (!tipo || !unidad_origen || !unidad_destino) {
      alert('Completa todos los campos');
      return;
    }

    try {
      const res = await fetch('/convertir', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({valor, tipo, unidad_origen, unidad_destino})
      });
      const data = await res.json();
      if(data.error) {
        resultado.textContent = 'Error: ' + data.error;
      } else {
        resultado.textContent = `Resultado: ${data.resultado} ${unidad_destino}`;
      }
    } catch (e) {
      resultado.textContent = 'Error al conectar con el servidor';
    }
  });
</script>

</body>
</html>
    """)

@app.route("/convertir", methods=["POST"])
def convertir():
    data = request.get_json()
    valor = data.get("valor")
    tipo = data.get("tipo")
    unidad_origen = data.get("unidad_origen")
    unidad_destino = data.get("unidad_destino")

    try:
        valor = float(valor)
    except (TypeError, ValueError):
        return jsonify({"error": "Valor no válido"})

    try:
        if tipo == "Longitud":
            resultado = convertir_longitud(valor, unidad_origen, unidad_destino)
        elif tipo == "Masa":
            resultado = convertir_masa(valor, unidad_origen, unidad_destino)
        elif tipo == "Temperatura":
            resultado = convertir_temperatura(valor, unidad_origen, unidad_destino)
        elif tipo == "Volumen":
            resultado = convertir_volumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Tiempo":
            resultado = convertir_tiempo(valor, unidad_origen, unidad_destino)
        elif tipo == "Velocidad":
            resultado = convertir_velocidad(valor, unidad_origen, unidad_destino)
        elif tipo == "Datos":
            resultado = convertir_datos(valor, unidad_origen, unidad_destino)
        elif tipo == "Energía":
            resultado = convertir_energía(valor, unidad_origen, unidad_destino)
        elif tipo == "Fuerza":
            resultado = convertir_fuerza(valor, unidad_origen, unidad_destino)
        elif tipo == "Área":
            resultado = convertir_area(valor, unidad_origen, unidad_destino)
        elif tipo == "Presión":
            resultado = convertir_presión(valor, unidad_origen, unidad_destino)
        elif tipo == "Tetravolumen":
            resultado = convertir_tetravolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Pentavolumen":
            resultado = convertir_pentavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Hexavolumen": 
            resultado = convertir_hexavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Heptavolumen":  
            resultado = convertir_heptavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Octavolumen":
            resultado = convertir_octavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Nonavolumen":
            resultado = convertir_nonavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Decavolumen":
            resultado = convertir_decavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Undecavolumen":
            resultado = convertir_undecavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Dodecavolumen":
            resultado = convertir_dodecavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Tridecavolumen":
            resultado = convertir_tridecavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Tetradecavolumen":
            resultado = convertir_tetradecavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Pentadecavolumen":
            resultado = convertir_pentadecavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Hexadecavolumen":
            resultado = convertir_hexadecavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Heptadecavolumen":
            resultado = convertir_heptadecavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Octadecavolumen":
            resultado = convertir_octadecavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Nonadecavolumen":
            resultado = convertir_nonadecavolumen(valor, unidad_origen, unidad_destino)
        elif tipo == "Idecavolumen":
            resultado = convertir_idecavolumen(valor, unidad_origen, unidad_destino)
        else:
            return jsonify({"error": "Tipo de conversión no soportado"})

        # Convierte el resultado a string si es tipo mpf (o cualquier objeto no serializable)
        if hasattr(resultado, '__class__') and resultado.__class__.__name__ == 'mpf':
            resultado = str(resultado)
        return jsonify({"resultado": resultado})
    except KeyError:
        return jsonify({"error": "Unidad no soportada para este tipo"})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    print("Servidor iniciado en http://localhost:5000")
    serve(app, host="0.0.0.0", port=5000)
