from PIL import Image
import importlib
import sys

def init():
    importlib.reload(sys)

def get_carrier_pic():
    return Image.open("carrier.png")

def get_carrier_pixels(carrier):
    return list(carrier.getdata())

def get_hindden_pic():
    return Image.open("hidden.png")

def get_hindden_pic_pixels(hindden_image):
    return list(hindden_image.getdata())

def encode(carrier, hidden_image):
    print("encode start")
    even_carrier = make_carrier_even(carrier)
    binary = get_hidden_data(hidden_image)

    if len(binary) > len(even_carrier.getdata()) * 4:
        raise Exception("Error : hidden's pixels are too large.")
    encoded_pixels = [(r+int(binary[index*4+0]),g+int(binary[index*4+1]),b+int(binary[index*4+2]),t+int(binary[index*4+3])) if index*4 < len(binary) else (r,g,b,t) for index,(r,g,b,t) in enumerate(list(even_carrier.getdata()))] 
    encoded_image = Image.new(even_carrier.mode, even_carrier.size)
    encoded_image.putdata(encoded_pixels)  
    print("encode done")
    return encoded_image


def make_carrier_even(carrier):
    even_pixels = [(r>>1<<1,g>>1<<1,b>>1<<1,t>>1<<1) for [r,g,b,t] in get_carrier_pixels(carrier)] 
    even_carrier = Image.new(carrier.mode, carrier.size) 
    even_carrier.putdata(even_pixels)  
    return even_carrier

def get_hidden_data(hidden_image):
    hidden_pixels = get_hindden_pic_pixels(hidden_image)

    str_pixels = ''
    for pixels_list in hidden_pixels :
        tmp = ','.join(str(e) for e in pixels_list)
        str_pixels = str_pixels + tmp + '.'

    str_pixels = str_pixels[0:len(str_pixels)-1]

    return ''.join(map(const_len_bin,bytearray(str_pixels, 'utf-8')))

def const_len_bin(int):
    binary = "0"*(8-(len(bin(int))-2))+bin(int).replace('0b','')  
    return binary

def decode(image,mode,size):
    print("deocde start")

    pixels = list(image.getdata())  
    binary = ''.join([str(int(r>>1<<1!=r))+str(int(g>>1<<1!=g))+str(int(b>>1<<1!=b))+str(int(t>>1<<1!=t)) for (r,g,b,t) in pixels]) # 提取图片中所有最低有效位中的数据
    end_index = get_end_index(binary)
    final_pixels = data_to_pixels(binary_to_string(binary[0:end_index]))

    decode_image = Image.new(mode,size)
    decode_image.putdata(final_pixels)

    print("decode done")
    return decode_image

def get_end_index(binary):
    double_null = binary.find('0000000000000000')
    end_index = double_null+(8-(double_null % 8)) if double_null%8 != 0 else double_null
    return end_index

def data_to_pixels(str_data):
    str_pixels = str_data.split('.') 
    
    final_pixels = []
    for str_pixel in str_pixels :   
        each_pixel = []
        rgbt = str_pixel.split(',')   
        for index in rgbt :    
            each_pixel.append(int(index))
        final_pixels.append(tuple(each_pixel))

    return final_pixels

def binary_to_string(binary):
    index = 0
    string = []
    fun = lambda x, i: x[0:8]
   
    while index + 1 < len(binary):        
        chartype = binary[index:].index('0') 
        if chartype == 0:
            chartype = 1        
        length = chartype*8
        
        for i in range(chartype):            
            ascode = int(binary[index+i*8:index+i*8+8],2)
            string.append(chr(ascode))
        index += length        
            
    return ''.join(string)

def get_decode_info():
    #decode_image = get_hindden_pic()
    decode_image = get_carrier_pic()
    return decode_image.mode,decode_image.size

def main():
    init()
    #藏
    #encode(get_carrier_pic(),get_hindden_pic()).save('encoded.png')
    #讀
    mode,size = get_decode_info()
    decode(Image.open("encoded.png"),mode,size).save("result.png")


main()
